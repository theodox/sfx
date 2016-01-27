"""
This module publishes all of the node type avaliable for use with shaderfx shaders.

Remember that these are for default ShaderFX networks - they won't work in a StingrayPBS node network
"""

from sfx import SFXNodeType


class Comparison(SFXNodeType):
    TYPE = "Comparison"
    ID = 20162


class IfElseBasic(SFXNodeType):
    TYPE = "If Else Basic"
    ID = 20163


class Time(SFXNodeType):
    TYPE = "Time"
    ID = 20086




class Light(SFXNodeType):
    TYPE = "Light"
    ID = 20152


class LightList(SFXNodeType):
    TYPE = "Light List"
    ID = 20153


class Add(SFXNodeType):
    TYPE = "Add"
    ID = 20026


class Clamp(SFXNodeType):
    TYPE = "Clamp"
    ID = 20044


class CrossProduct(SFXNodeType):
    TYPE = "Cross Product"
    ID = 20030


class Distance(SFXNodeType):
    TYPE = "Distance"
    ID = 20048


class Divide(SFXNodeType):
    TYPE = "Divide"
    ID = 20027


class DotProduct(SFXNodeType):
    TYPE = "Dot Product"
    ID = 20018


class Invert(SFXNodeType):
    TYPE = "Invert"
    ID = 20157


class Length(SFXNodeType):
    TYPE = "Length"
    ID = 20032


class Max(SFXNodeType):
    TYPE = "Max"
    ID = 20052


class Multiply(SFXNodeType):
    TYPE = "Multiply"
    ID = 20016


class Normalize(SFXNodeType):
    TYPE = "Normalize"
    ID = 20021


class Subtract(SFXNodeType):
    TYPE = "Subtract"
    ID = 20022


class View(SFXNodeType):
    TYPE = "View"
    ID = 20065


class ViewI(SFXNodeType):
    TYPE = "View I"
    ID = 20067


class ViewPrj(SFXNodeType):
    TYPE = "View Prj"
    ID = 20077


class World(SFXNodeType):
    TYPE = "World"
    ID = 20061


class WorldI(SFXNodeType):
    TYPE = "World I"
    ID = 20063


class WorldIT(SFXNodeType):
    TYPE = "World IT"
    ID = 20064



class Bool(SFXNodeType):
    TYPE = "Bool"
    ID = 20088


class Color(SFXNodeType):
    TYPE = "Color"
    ID = 20011


class Float(SFXNodeType):
    TYPE = "Float"
    ID = 20017


class Float2(SFXNodeType):
    TYPE = "Float2"
    ID = 20139


class Int(SFXNodeType):
    TYPE = "Int"
    ID = 20096


class VectorComponent(SFXNodeType):
    TYPE = "Vector Component"
    ID = 20108


class VectorConstruct(SFXNodeType):
    TYPE = "Vector Construct"
    ID = 20020


class String(SFXNodeType):
    TYPE = "String"
    ID = 20105



class Noise(SFXNodeType):
    TYPE = "Noise"
    ID = 20054


'''
Nodes below here are hand-tweaked, not generated. In the ShaderFX UI they look like individual nodes but they
are instantiated with the addNode flag and with a string name.
'''



class SFXGroupNodeType (SFXNodeType):
    GROUP = "groupname"

    @classmethod
    def group_id(cls):
        return "-".join((cls.TYPE, "Hw Shader Nodes", cls.GROUP)) + ".grp"


# ---- Patterns

class PatternNodeGroup(SFXGroupNodeType):
    GROUP = 'Patterns'


class Brick(PatternNodeGroup):
    TYPE = "Brick"
    ID = 40008


class CellularNoise(PatternNodeGroup):
    TYPE = "Cellular Noise"
    ID = 40013


class Checker2D(PatternNodeGroup):
    TYPE = "Checker 2D"
    ID = 40014

class SimplexNoise2D(PatternNodeGroup):
    TYPE = "Simplex Noise 2D"
    ID = 40063


class SimplexNoise3D(PatternNodeGroup):
    TYPE = "Simplex Noise 3D"
    ID = 40064


class VoronoiSmoothQuilez(PatternNodeGroup):
    TYPE = "VoronoiSmoothQuilez"
    ID = 40086


class WavyLines(PatternNodeGroup):
    TYPE = "WavyLines"
    ID = 40088

# --- Textures

class SFXTextureGroup(SFXGroupNodeType):
    GROUP = "Textures"


class CombineNormalMaps(SFXTextureGroup):
    TYPE = "Combine Normal Maps"
    ID = 40017


class DerivedNormalZMap(SFXTextureGroup):
    TYPE = "Derived Normal Z Map"
    ID = 40018


class FlipBook(SFXTextureGroup):
    TYPE = "Flip Book"
    ID = 40022


class LatLongUVs(SFXTextureGroup):
    TYPE = "LatLong UVs"
    ID = 40035


class MatCapUVs(SFXTextureGroup):
    TYPE = "MatCapUVs"
    ID = 40043


class PNAENDisplacementMap(SFXTextureGroup):
    TYPE = "PNAEN Displacement Map"
    ID = 40051


class ReflectionCubeMap(SFXTextureGroup):
    TYPE = "Reflection Cube Map"
    ID = 40054


class RefractionCubeMap(SFXTextureGroup):
    TYPE = "Refraction Cube Map"
    ID = 40056


class SphericalReflectionUVs(SFXTextureGroup):
    TYPE = "Spherical Reflection UVs"
    ID = 40066


class TextureMap(SFXTextureGroup):
    TYPE = "Texture Map"
    ID = 40071


class UVPanner(SFXTextureGroup):
    TYPE = "UV Panner"
    ID = 40074


class UVRotator(SFXTextureGroup):
    TYPE = "UV Rotator"
    ID = 40075

# ----  Inputs Common

class CommonInputGroup(SFXGroupNodeType):
    GROUP = "Inputs Common"


class CameraVector(CommonInputGroup):
    TYPE = "Camera Vector"
    ID = 40012


class LightVector(CommonInputGroup):
    TYPE = "Light Vector"
    ID = 40040


class ReflectionVector(CommonInputGroup):
    TYPE = "Reflection Vector"
    ID = 40055


class RefractionVector(CommonInputGroup):
    TYPE = "Refraction Vector"
    ID = 40057


class UVSet(CommonInputGroup):
    TYPE = "UV Set"
    ID = 40076


class VertexColor(CommonInputGroup):
    TYPE = "Vertex Color"
    ID = 40078


class VertexWorldBiNormal(CommonInputGroup):
    TYPE = "Vertex World BiNormal"
    ID = 40082


class VertexWorldPosition(CommonInputGroup):
    TYPE = "Vertex World Position"
    ID = 40084


class VertexWorldTangent(CommonInputGroup):
    TYPE = "Vertex World Tangent"
    ID = 40085


#----  Lighting groups

class LightingGroup(SFXGroupNodeType):
    GROUP = "Lighting"


class AmbientGroundSky(LightingGroup):
    TYPE = "Ambient Ground Sky"
    ID = 40001


class DesaturateColor(LightingGroup):
    TYPE = "Desaturate Color"
    ID = 40019


class Fresnel(LightingGroup):
    TYPE = "Fresnel"
    ID = 40024

# --- Various

class Bump(SFXGroupNodeType):
    TYPE = "Bump"
    ID = 40009
    GROUP = "Various"

class CameraDistanceTessellation(SFXGroupNodeType):
    TYPE = "Camera Distance Tessellation"
    ID = 40010
    GROUP = "Various"

# use this to regenerate the class names with SFXNodeType.generate_class_definitions
_KNOWN_SFX_NAMES = """Comparison
If Else Basic
Time
Camera Vector
Light Vector
Reflection Vector
Refraction Vector
UV Set
Vertex Color
Vertex World BiNormal
Vertex World Position
Vertex World Tangent
Ambient Ground Sky
Desaturate Color
Fresnel
Light
Light List
Add
Clamp
Cross Product
Distance
Divide
Dot Product
Invert
Length
Max
Multiply
Normalize
Subtract
View
View I
View Prj
World
World I
World IT
Brick
Cellular Noise
Checker 2D
Noise
Simplex Noise 2D
Simplex Noise 3D
VoronoiSmoothQuilez
WavyLines
Combine Normal Maps
Derived Normal Z Map
Flip Book
LatLong UVs
MatCapUVs
PNAEN Displacement Map
Reflection Cube Map
Refraction Cube Map
Spherical Reflection UVs
Texture Map
UV Panner
UV Rotator
Bool
Color
Float
Float2
Int
Vector Component
Vector Construct
Bump
Camera Distance Tessellation
String"""
