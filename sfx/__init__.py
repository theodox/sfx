from functools import partial

import maya.cmds as cmds


class SFXPropertyNotFound(AttributeError):
    pass


class SFXNodeType(object):
    """
    This class represents the magic name-id combo for different node types in shaderFX -- it's much easier to code if
    you don't need to remember the dozens of magic numbers which correspond to concrete node types.

    The node type numbers vary between vanilla shaderfx and StingrayPBS shaders (a given network will only support
    one or the other, depending on which node type is instantiated in Maya).  The concrete derived classes for the
    two node systems are in the pbsnode and sfxnode submodules.
    """
    NODE_TYPE = ''
    NODE_ID = -1

    SFX_NODE_TEMPLATE = """
    class {0} ({1}):
        TYPE = "{2}"
        ID = {3}
    """

    def __repr__(self):
        return "<%s: %s>" % (self.NODE_TYPE, self.NODE_ID)

    @classmethod
    def generate_class_definitions(cls, shader, node_list):
        """
        helper method which generates class definitions for known node types. These are stable within maya versions
        but may change between them. Requires a shader node to run.  Create a node, then pass in one of the string lists
        in the pbsnodes or sfxnodes modules to this -- it will spit out a the text of all the classes for your version
        of Maya.
        """
        class_def = []
        errors = []

        for item in node_list.split('\n'):
            try:
                classname = item.replace(" ", "")
                id_code = cmds.shaderfx(sfxnode=shader, getNodeTypeByClassName=item)
                class_def.append(cls.SFX_NODE_TEMPLATE.format(classname, cls.__name__, item, id_code))
            except:
                errors.append(item)

        return class_def, errors


class SFXPlugs(object):
    """
    A wrapper for an enumerated list of named plugs so you can write code like

            root = network.root
            network.connect(mult_node, mult_node.outputs.result, root, root.inputs.diffuse)

    Where 'results' represetns the 0th plug the multiply node's output side and 'diffuse' is the 3rd plug on the
    shader root's input side.

    SFXPlugs objects populate the  'inputs' and 'outputs' fields of graph nodes.
    """

    def __init__(self, node, plugs):
        def _safe_plug_name(p):
            result = p.lower().replace(" ", "_")
            if result.startswith("_"):
                result = result[1:]
            return result

        self.plugs = dict((_safe_plug_name(plug), (node, i)) for i, plug in enumerate(plugs))

    def __getattr__(self, item):
        return self.plugs[item]


class SFXNode(object):
    """
    Wraps a node inside a shaderfx shader for property queries and pythonic style.

    Usage:

    Create an SFXnode:

        node = SFXNode('sfx_shader', 4)
        # gets node index 1 in the network 'sfx_shader'

        print node.nodetype
        # 'Fresnel'
        # gets the display name of the wrapped node

        print node.properties:
        # { 'min': 'float', 'max': 'float', 'method': 'stringlist' }

        print node.min
        # 1.0
        # getting a named property returns its value.

        print node.i_dont_exist
        # SFXPropertyNotFound: no attribute named i_dont_exist
        # if property is not present, raise an AttributeError

        node.min = 2.0
        # sets the node value

        node.i_dont_exist = 999
        # MayaCommandError
        # setting an invalid value or property raises a MayaCommandError

    The indices for named inputs and outputs are stored in properties named 'inputs' and 'outpute', which have named
    members so you can write:

        network.connect( node1, node1.outputs.xyz,  node2, node2.inputs.color)

    which is just a convenient way of writing something like

        network.connect( node1, 0,  node2, 11)

    """
    __slots__ = ['cmd', 'index', 'node', '_cached_properties', 'nodetype', 'inputs', 'outputs', 'properties']

    def __init__(self, node, idx):
        self.cmd = partial(cmds.shaderfx, n=node)
        self.index = idx
        self.node = node
        self._cached_properties = dict((k, None) for k in self.cmd(lp=self.index))

        for k in self._cached_properties.keys():
            try:
                # note this has to be a STRING NOT A UNICODE
                # otherwise the __setattr__ hack will fail
                tt = str(self.cmd(gpt=(self.index, k)))
                self._cached_properties[k] = tt
            except RuntimeError:
                # these two properties on the MaterialVariable node
                # never report their type correctly in Maya2016
                # so this is a workaround
                if k == 'defaultvectwo':
                    self._cached_properties[k] = 'float2'
                    continue
                if k == 'defaultvectthree':
                    self._cached_properties[k] = 'float3'
                    continue

        input_count = self.cmd(gsc=(self.index, 0))
        input_plugs = [self.cmd(gsn=(self.index, 0, i)) for i in range(input_count)]
        output_count = self.cmd(gsc=(self.index, 1))
        output_plugs = [self.cmd(gsn=(self.index, 1, i)) for i in range(output_count)]
        self.inputs = SFXPlugs(self.index, input_plugs)
        self.outputs = SFXPlugs(self.index, output_plugs)

    @property
    def nodetype(self):
        """
        Return the node type of this node as a string
        """
        return self.cmd(getNodeClassName=self.index)

    @property
    def properties(self):
        """
        returns a dictionary of { property_name: property_type} for all properties in this node
        """
        return self._cached_properties

    def __getattr__(self, item):
        """
        Magic property getter
        """
        if item in self.__slots__:
            return object.__getattribute__(self, item)

        if item in self._cached_properties:
            return self.cmd(gpv=(self.index, item))
        raise SFXPropertyNotFound, 'no attribute named %s' % item

    def __setattr__(self, key, value):
        """
        Magic property setter
        """
        if key in self.__slots__:
            object.__setattr__(self, key, value)
            return
        if key in self._cached_properties:

            flag = 'edit_' + self._cached_properties[key]

            args = [self.index, key]
            if hasattr(value, '__iter__'):
                args.extend([i for i in value])
            else:
                args.append(value)
            flags = {flag: tuple(args)}
            self.cmd(**flags)

    def __repr__(self):
        return "<sfxNode '{0}' ({1})>".format(self.name, self.nodetype)


class SFXGroupNode(SFXNode):
    """
    Subclass that wraps nodes which are really groups (eg, 'Texture Map') and correctly handles the quirky way
    that outputs are managed. Group nodes do not correctly report the output values they display: those are
    delegated to a separate 'group end node' which is captured here.
    """
    __slots__ = ['cmd', 'index', 'node', '_cached_properties', 'nodetype', 'inputs', 'outputs', 'properties',
                 'end_node']

    def __init__(self, node, idx):
        super(SFXGroupNode, self).__init__(node, idx)
        self.end_node = SFXNode(node, self.cmd(getGroupEndUID=idx))
        self.outputs = self.end_node.outputs


class SFXNetwork(object):
    """
    Wraps a shaderFX node for queries

    Usage:

        network = SFXNetwork('shader')
        # create a network

        print network.root
        # <sfxNode UnlitBase (1)>
        # returns the rendering node in the network

        print network.nodes
        # { 1 : <sfxNode UnlitBase (1)>, 2: <sfxNode 'MaterialVariable' (2)> }
        # returns a dictionary of id: node for all nodes in this network.
        # note that the index numbers are not guaranteed to be continuous

        var_node_1 = self.nodes[2]
        #  <sfxNode 'MaterialVariable' (2)>
        # gets a node

        mult_node = network.add(pbsnodes.Multiply)
        # creates a Multiply node and adds it safto the network

        var_node_2 = network.add(pbsnodes.MaterialVariable)
        # creates a MaterialVariable node and adds it to the network

        network.connect(var_node.outputs.value, mult_node.inputs.A)
        # connect output 'value' of the first material variable to input A the multiply node
        mult_node.activesocket = 0
        mult_node.socketswizzlevalue = 'xyz'
        # set the swizzle to 'xyz' (ie, a float3)
        network.connect(var_node.outputs.result, mult_node.inputs.A)
        mult_node.activesocket = 1
        mult_node.socketswizzlevalue = 'xyz'
        # connect the second var to socket 1 of the multiply
        network.connect(mult_node.outputs.result, network.root.inputs.color)
        # connect the mult node to the color socket of the root


        print network.find_by_type(pbsnodes.MaterialVariable)
        # [ <sfxNode 'MaterialVariable' (2)>, <sfxNode 'MaterialVariable' (4)> ]
        # returns all nodes of the specified type in this network

        network.delete(var_node_1)
        # delete a node
        network.delete(2)
        # alternate syntax: delete node at index 2
    """

    def __init__(self, shader):
        self.shader = shader
        self.nodes = {}
        self.cmd = partial(cmds.shaderfx, n=self.shader)
        found = 0
        nodes = self.cmd(getNodeCount=True)
        for r in range(1, 7999):
            if found >= nodes:
                break
            # there appears to be no way to get a node list,
            # so we try random IDs until we have our count
            # we'll rarely get past 20 or so...
            try:
                result = None
                if self.cmd(isGroupStart=r):
                    result = SFXGroupNode(self.shader, r)
                else:
                    result = SFXNode(self.shader, r)

                if result.name:
                    self.nodes[result.index] = result
                found += 1
            except:
                pass

        root_index = self.cmd(rhw=True)
        self.root = SFXNode(self.shader, root_index)

    def add(self, node_klass, name=None):
        """
        Add a new node of type <node_klass> to the network, with the optional name.  <node_Klass> is either one of the
        SFXNodeType derivatives in the pbsnodes or sfxnodes submodules.
        """
        if hasattr(node_klass, 'group_id'):
            return self._add_group(node_klass, name)

        new_node_id = self.cmd(addNode=node_klass.ID)

        result = SFXNode(self.shader, new_node_id)
        if name:
            result.name = name
        self.nodes[result.index] = result
        return result

    def _add_group(self, node_klass, name=None):
        """
        adds a group node of type node_klass.  Only called from add()
        """
        new_node_id = self.cmd(addGroup=node_klass.group_id())
        result = SFXGroupNode(self.shader, new_node_id)
        if name:
            result.name = name
        self.nodes[result.index] = result
        return result

    def delete(self, node_or_id):
        """
        remove the specified node from the network.
        """
        if hasattr(node_or_id, 'index'):
            node_or_id = node_or_id.index

        del (self.nodes[node_or_id])
        self.cmd(deleteNode=node_or_id)

    def connect(self, start_plug, end_plug, swizzle=None):
        """
        connect two sockets, represented by SFXPlug tuples of (node, socket).  Ordinarily you'd call this like

            net.connect( node.outputs.plugname, other_node.inputs.plugname)

        but

            net.connect( (123, 1), (456, 0))

        will also work, connecting output 1 of node 123 to input 0 of node 456.

        If swizzle string is provided, set the receiving socket swizzle

        Plug names are always lower cased. In shaderFx networks they are enjambed, so that "Specular Color" becomes
        'specularcolor' and so on. In PBS networks spaces become underscores

        """
        node, plug = start_plug
        node2, plug2 = end_plug

        self.cmd(makeConnection=(node, plug, node2, plug2))
        if swizzle:
            node2.activesocket = plug2
            node2.socketswizzlevalue = swizzle

    def disconnect(self, start_plug, end_plug):
        """
        connect two sockets, represented by SFXPlug tuples of (node, socket).  Ordinarily you'd call this like

            net.disconnect( node.outputs.plugname, other_node.inputs.plugname)

        but

            net.disconnect( (123, 1), (456, 0))

        will also work

        """
        node, plug = start_plug
        node2, plug2 = end_plug
        self.cmd(breakConnection=(node, plug, node2, plug2))

    def find_by_name(self, name):
        return [i for i in self.nodes.values() if i.name == name]

    def find_by_type(self, type):
        # accepts either type string or SFXNodeType objects
        if hasattr(type, 'TYPE'):
            type = type.TYPE
        return [i for i in self.nodes.values() if i.nodetype == type]

    def get_inputs(self, node):
        # inputs are always single items
        results = self._get_connections(node, 0)
        return dict((k, v[0]) for k, v in results.items() if v)

    def get_outputs(self, node):
        # outputs can have multiple items
        return self._get_connections(node, 1)

    def _get_connections(self, node, direction):
        """
        An internal method to traverse and return the connections of a given plug. Returns the graph connections
        as a dictionary  { index : node } where <index> is the integer plug index and <node> is the node connected to that plug
        """
        results = {}
        if not hasattr(node, 'index'):
            node = self.nodes[node]
        socket_count = self.cmd(getSocketCount=(node.index, direction))
        for s in range(socket_count):
            conn = self.cmd(getConnectedNodeID=(node.index, direction, s, 0, 1))
            if conn:
                connection_count = self.cmd(getConnectedSocketCount=(node.index, direction, s))
                connections = [self.cmd(getConnectedNodeID=(node.index, direction, s, idx, 1)) for idx in
                               range(connection_count)]
                results[s] = [self.nodes[n] for n in connections]
        return results

    @classmethod
    def create(cls, name):
        """
        Create a new shader and return the ShaderNetwork that wraps it.
        """
        sfx_shader = cmds.shadingNode('ShaderfxShader', asShader=True, name=name)
        cmds.shaderfx(sfxnode=sfx_shader, initShaderAttributes=True)
        network = cls(sfx_shader)
        return network

    @classmethod
    def instantiate(cls, name, sfxfile):
        """
        create a new shader node from the supplied SFX file.  Note that sfx and stingray pbs files use the same SFX
        extension but are not cross-compatible- if you create a ShaderFX shader loading a StingrayPBS sfx file into it
        will fail silentyly and vice-versa.  It's a good idea to use a custom extension to prevent confusion.
        """
        network = cls.create(name)
        network.cmd(loadGraph=sfxfile)
        return network

    def layout(self):
        """
        Does a quick grid layout of this network
        It's not fancy, but it makes for eaiser visual debugging
        """
        V_SPACE = 100
        H_SPACE = -150

        def recurse_node(node, level=0):
            for each_node in self.get_inputs(node).values():

                for sub_node in recurse_node(each_node, level + 2):
                    yield sub_node
                yield level + 1, each_node
            yield level, node

        results = [i for i in recurse_node(self.root)]
        results.sort()
        results.reverse()
        last_lavel = -1
        vertical = 0
        for level, node in results:
            if level != last_lavel:
                vertical = 0
            else:
                vertical += 1
            last_lavel = level
            if node.posx == 0:
                node.posy = V_SPACE * vertical

            node.posx = min(node.posx, H_SPACE * (level + 1))
            node.collapsed = True

    def __repr__(self):
        return "<sfxNetwork '{0}'>".format(self.shader)


class StingrayPBSNetwork(SFXNetwork):
    """
    A variant of SFXNetwork that create a stingray network instead of a vanilla ShaderFX Network
    """

    @classmethod
    def create(cls, name):
        sfx_shader = cmds.shadingNode('StingrayPBS', asShader=True, name=name)
        cmds.shaderfx(sfxnode=sfx_shader, initShaderAttributes=True)
        network = cls(sfx_shader)
        return network
