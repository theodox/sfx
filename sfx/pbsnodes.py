"""
This module publishes all of the node type avaliable for use with StingrayPBS shaders.

Remember that these are for StingrayPBS networks - they won't work in a ShaderFX node network
"""

from sfx import SFXNodeType


class VegetationBending(SFXNodeType):
    TYPE = "Vegetation Bending"
    ID = 20241


class ConstantScalar(SFXNodeType):
    TYPE = "Constant Scalar"
    ID = 20196


class ConstantVector2(SFXNodeType):
    TYPE = "Constant Vector2"
    ID = 20200


class ConstantVector3(SFXNodeType):
    TYPE = "Constant Vector3"
    ID = 20190


class ConstantVector4(SFXNodeType):
    TYPE = "Constant Vector4"
    ID = 20201


class ConstructVector2(SFXNodeType):
    TYPE = "Construct Vector2"
    ID = 20202


class ConstructVector3(SFXNodeType):
    TYPE = "Construct Vector3"
    ID = 20203


class ConstructVector4(SFXNodeType):
    TYPE = "Construct Vector4"
    ID = 20204


class EyeVector(SFXNodeType):
    TYPE = "Eye Vector"
    ID = 20214


class MaterialVariable(SFXNodeType):
    TYPE = "Material Variable"
    ID = 20185


class SunDirection(SFXNodeType):
    TYPE = "Sun Direction"
    ID = 20238


class Time(SFXNodeType):
    TYPE = "Time"
    ID = 20207


class Absolute(SFXNodeType):
    TYPE = "Absolute"
    ID = 20197


class Add(SFXNodeType):
    TYPE = "Add"
    ID = 20187


class Ceil(SFXNodeType):
    TYPE = "Ceil"
    ID = 20199


class Clamp(SFXNodeType):
    TYPE = "Clamp"
    ID = 20193


class Cosine(SFXNodeType):
    TYPE = "Cosine"
    ID = 20205


class CrossProduct(SFXNodeType):
    TYPE = "Cross Product"
    ID = 20206


class DDX(SFXNodeType):
    TYPE = "DDX"
    ID = 20208


class DDY(SFXNodeType):
    TYPE = "DDY"
    ID = 20209


class Distance(SFXNodeType):
    TYPE = "Distance"
    ID = 20211


class Divide(SFXNodeType):
    TYPE = "Divide"
    ID = 20212


class DotProduct(SFXNodeType):
    TYPE = "Dot Product"
    ID = 20213


class Floor(SFXNodeType):
    TYPE = "Floor"
    ID = 20216


class Fmod(SFXNodeType):
    TYPE = "Fmod"
    ID = 20217


class Fractional(SFXNodeType):
    TYPE = "Fractional"
    ID = 20188


class If(SFXNodeType):
    TYPE = "If"
    ID = 20189


class InterpolateSmooth(SFXNodeType):
    TYPE = "Interpolate Smooth"
    ID = 20230


class Invert(SFXNodeType):
    TYPE = "Invert"
    ID = 20220


class Length(SFXNodeType):
    TYPE = "Length"
    ID = 20221


class LinearInterpolate(SFXNodeType):
    TYPE = "Linear Interpolate"
    ID = 20184


class Max(SFXNodeType):
    TYPE = "Max"
    ID = 20240


class Multiply(SFXNodeType):
    TYPE = "Multiply"
    ID = 20186


class Normalize(SFXNodeType):
    TYPE = "Normalize"
    ID = 20222


class Power(SFXNodeType):
    TYPE = "Power"
    ID = 20192


class Reflect(SFXNodeType):
    TYPE = "Reflect"
    ID = 20226


class Refract(SFXNodeType):
    TYPE = "Refract"
    ID = 20227


class Sine(SFXNodeType):
    TYPE = "Sine"
    ID = 20229


class SquareRoot(SFXNodeType):
    TYPE = "Square Root"
    ID = 20231


class Subtract(SFXNodeType):
    TYPE = "Subtract"
    ID = 20182


class StandardBase(SFXNodeType):
    TYPE = "Standard Base"
    ID = 20176


class UnlitBase(SFXNodeType):
    TYPE = "Unlit Base"
    ID = 20242


class SampleCube(SFXNodeType):
    TYPE = "Sample Cube"
    ID = 20237


class SampleTexture(SFXNodeType):
    TYPE = "Sample Texture"
    ID = 20177


class ObjectToWorld(SFXNodeType):
    TYPE = "Object To World"
    ID = 20223


class TangentToWorld(SFXNodeType):
    TYPE = "Tangent To World"
    ID = 20195


class WorldToObject(SFXNodeType):
    TYPE = "World To Object"
    ID = 20236


class WorldToTangent(SFXNodeType):
    TYPE = "World To Tangent"
    ID = 20232


class BlendNormals(SFXNodeType):
    TYPE = "Blend Normals"
    ID = 20198


class Desaturation(SFXNodeType):
    TYPE = "Desaturation"
    ID = 20210


class Flipbook(SFXNodeType):
    TYPE = "Flipbook"
    ID = 20215


class Fresnel(SFXNodeType):
    TYPE = "Fresnel"
    ID = 20218


class HSVtoRGB(SFXNodeType):
    TYPE = "HSV to RGB"
    ID = 20219


class Panner(SFXNodeType):
    TYPE = "Panner"
    ID = 20224


class Parallax(SFXNodeType):
    TYPE = "Parallax"
    ID = 20183


class RGBtoHSV(SFXNodeType):
    TYPE = "RGB to HSV"
    ID = 20228


class Rotator(SFXNodeType):
    TYPE = "Rotator"
    ID = 20225


class Texcoord0(SFXNodeType):
    TYPE = "Texcoord 0"
    ID = 20178


class Texcoord1(SFXNodeType):
    TYPE = "Texcoord 1"
    ID = 20179


class Texcoord2(SFXNodeType):
    TYPE = "Texcoord 2"
    ID = 20180


class Texcoord3(SFXNodeType):
    TYPE = "Texcoord 3"
    ID = 20181


class VertexBinormal(SFXNodeType):
    TYPE = "Vertex Binormal"
    ID = 20235


class VertexColor0(SFXNodeType):
    TYPE = "Vertex Color 0"
    ID = 20191


class VertexPosition(SFXNodeType):
    TYPE = "Vertex Position"
    ID = 20233


class VertexTangent(SFXNodeType):
    TYPE = "Vertex Tangent"
    ID = 20234


class WorldNormal(SFXNodeType):
    TYPE = "World Normal"
    ID = 20194

# use this to regenerate the class names with SFXNodeType.generate_class_definitions
_KNOWN_PBS_NAMES = """Vegetation Bending
Constant Scalar
Constant Vector2
Constant Vector3
Constant Vector4
Construct Vector2
Construct Vector3
Construct Vector4
Eye Vector
Material Variable
Sun Direction
Time
Absolute
Add
Ceil
Clamp
Cosine
Cross Product
DDX
DDY
Distance
Divide
Dot Product
Floor
Fmod
Fractional
If
Interpolate Smooth
Invert
Length
Linear Interpolate
Max
Multiply
Normalize
Power
Reflect
Refract
Sine
Square Root
Subtract
Standard Base
Unlit Base
Sample Cube
Sample Texture
Object To World
Tangent To World
World To Object
World To Tangent
Blend Normals
Desaturation
Flipbook
Fresnel
HSV to RGB
Panner
Parallax
RGB to HSV
Rotator
Texcoord 0
Texcoord 1
Texcoord 2
Texcoord 3
Vertex Binormal
Vertex Color 0
Vertex Position
Vertex Tangent
World Normal"""