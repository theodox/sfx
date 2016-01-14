__author__ = 'Steve Theodore'
"""
Basic unit tests for the sfx module. Usage:

   cd path/to/tests/and/sfx/module
   path/to/mayapy.exe  tests.py
"""

import unittest

import maya.cmds as cmds

import sfx.sfxnodes as sfxnodes
from sfx import SFXNetwork, SFXPropertyNotFound



class TestShaderFX(unittest.TestCase):
    def setUp(self):
        cmds.file(new=True, f=True)


class TestShaderFXNetwork(TestShaderFX):
    def test_sfx_create(self):
        new_network = SFXNetwork.create('example')
        assert cmds.ls('example') == ['example']
        assert cmds.nodeType('example') == 'ShaderfxShader'
        assert new_network.shader == 'example'

    def test_sfx_root(self):
        new_network = SFXNetwork.create('example')
        root_node = new_network.root
        assert root_node.nodetype == 'Hardware Shader'

    def test_find_by_name(self):
        new_network = SFXNetwork.create('example')
        assert len(new_network.find_by_name('SurfaceMaskCutoff')) == 1
        assert len(new_network.find_by_name('nonexistent')) == 0
        assert len(new_network.find_by_name('Color')) == 7

    def test_find_by_type(self):
        new_network = SFXNetwork.create('example')
        assert len(new_network.find_by_type(sfxnodes.Color)) == 26
        assert len(new_network.find_by_type(sfxnodes.DerivedNormalZMap)) == 0

    def test_node_dict(self):
        new_network = SFXNetwork.create('example')
        assert hasattr(new_network.nodes, 'keys')
        assert hasattr(new_network.nodes, 'values')
        assert hasattr(new_network.nodes, '__getitem__')
        assert hasattr(new_network.nodes, '__iter__')

    def test_new_node(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        assert new_node.nodetype == 'Color'
        assert new_network.find_by_name('added')

    def test_connect(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        target = new_network.find_by_name('TotalAmbientAndOpacity')[0]
        new_network.connect(new_node, new_node.outputs.rgb, target, target.inputs.xyz)
        connections = new_network.get_inputs(target)
        assert new_node in connections.values()

    def test_disconnect(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        target = new_network.find_by_name('TotalAmbientAndOpacity')[0]
        new_network.connect(new_node, new_node.outputs.rgb, target, target.inputs.xyz)
        new_network.disconnect(new_node, new_node.outputs.rgb, target, target.inputs.xyz)
        connections = new_network.get_inputs(target)
        assert new_node not in connections.values()

    def test_cmd(self):
        new_network = SFXNetwork.create('example')
        result = new_network.cmd(help=True)
        # this just ensures the 'cmd' is functional
        # and doesn't except


class TestSFXNode(TestShaderFX):
    def test_node_name(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        assert new_node.name == 'added'

    def test_node_name(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        assert new_node.name == 'added'

    def test_properties_dict(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        props = new_node.properties
        expected = {u'uigroup': 'string', u'socketdefaultvalue': 'string', u'semantic': 'string', u'color': 'float4',
                    u'global': 'bool', u'activesocketlabel': 'string', u'compoundassignment': 'bool',
                    u'exposetoui': 'bool', u'defineinheader': 'bool', u'group': 'int', u'uiorder': 'int',
                    u'note': 'string', u'width': 'int', u'version': 'float', u'hasbeenedited': 'bool',
                    u'collapsed': 'bool', u'helpaction': 'action', u'posx': 'float', u'posy': 'float',
                    u'previewswatch': 'int', u'name': 'string', u'activesocket': 'int', u'socketswizzlevalue': 'string'}

        for k, v in props.items():
            assert expected[k] == v

    def test_properties_getter_4(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        assert new_node.color == [0.5, 0.5, 0.5, 1.0]

    def test_properties_setter_4(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        new_node.color = [1, 0, 1, 0]
        assert new_node.color == [1, 0, 1, 0]

    def test_properties_getter_1(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        assert new_node.uiorder == 0

    def test_properties_setter_1(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        new_node.uiorder = 10
        assert new_node.uiorder == 10

    def test_cmd(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        result = new_node.cmd(help=True)
        # just proves cmd exists and doesn't except

    def test_asserts_on_bad_property(self):
        new_network = SFXNetwork.create('example')
        new_node = new_network.add(sfxnodes.Color, 'added')
        example = lambda: new_node.fred
        self.assertRaises(SFXPropertyNotFound, example)


if __name__ == '__main__':
    import maya.standalone

    maya.standalone.initialize()
    unittest.main()
