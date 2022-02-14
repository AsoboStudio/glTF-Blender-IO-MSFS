from bpy.types import Material
from bpy.props import FloatVectorProperty
from typing import Optional, Tuple
from io_scene_gltf2.io.com import gltf2_io


class AsoboMaterialGeometryDecal:

    SerializedName = "ASOBO_material_blend_gbuffer"

    def __init__(
        self,
        enabled: bool = True,
        baseColorBlendFactor: Optional[float] = 0.0,
        metallicBlendFactor: Optional[float] = 0.0,
        roughnessBlendFactor: Optional[float] = 0.0,
        normalBlendFactor: Optional[float] = 0.0,
        emissiveBlendFactor: Optional[float] = 0.0,
        occlusionBlendFactor: Optional[float] = 0.0,
    ):
        self.enabled = enabled
        self.baseColorBlendFactor = baseColorBlendFactor
        self.metallicBlendFactor = metallicBlendFactor
        self.roughnessBlendFactor = roughnessBlendFactor
        self.normalBlendFactor = normalBlendFactor
        self.emissiveBlendFactor = emissiveBlendFactor
        self.occlusionBlendFactor = occlusionBlendFactor


class AsoboMaterialGhostEffect:
    class Defaults:
        bias = 1.0
        scale = 1.0
        power = 1.0

    SerializedName = "ASOBO_material_ghost_effect"

    def __init__(
        self,
        bias: Optional[float] = Defaults.bias,
        scale: Optional[float] = Defaults.scale,
        power: Optional[float] = Defaults.power,
    ):
        self.bias = bias
        self.scale = scale
        self.power = power


class AsoboMaterialDrawOrder:
    class Defaults:
        drawOrderOffset = 0

    Serializedname = "ASOBO_material_draw_order"

    def __init__(self, drawOrderOffset: Optional[int] = Defaults.drawOrderOffset):
        self.drawOrderOffset = drawOrderOffset


class AsoboDayNightCycle:

    SerializedName = "ASOBO_material_day_night_switch"


class AsoboPearlescent:
    class Defaults:
        pearlShift = 0.0
        pearlRange = 0.0
        pearlBrightness = 0.0

    SerializedName = "ASOBO_material_pearlescent"

    def __init__(
        self,
        pearlShift: Optional[float] = Defaults.pearlShift,
        pearlRange: Optional[float] = Defaults.pearlRange,
        pearlBrightness: Optional[float] = Defaults.pearlBrightness,
    ):
        self.pearlShift = pearlShift
        self.pearlRange = pearlRange
        self.pearlBrightness = pearlBrightness


class AsoboAlphaModeDither:

    SerializedName = "ASOBO_material_alphamode_dither"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled


class AsoboMaterialInvisible:

    SerializedName = "ASOBO_material_invisible"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled


class AsoboMaterialEnvironmentOccluder:

    SerializedName = "ASOBO_material_environment_occluder"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled


class AsoboMaterialUVOptions:
    class Defaults:
        AOUseUV2 = False
        clampUVX = False
        clampUVY = False
        clampUVZ = False
        UVOffsetU = 0.0
        UVOffsetV = 0.0
        UVTilingU = 0.0
        UVTilingV = 0.0
        UVRotation = 0.0

    SerializedName = "ASOBO_material_UV_options"

    def __init__(
        self,
        UVOffsetU: float = Defaults.UVOffsetU,
        UVOffsetV: float = Defaults.UVOffsetV,
        UVTilingU: float = Defaults.UVTilingU,
        UVTilingV: float = Defaults.UVTilingV,
        UVRotation: float = Defaults.UVRotation,
        AOUseUV2: Optional[bool] = Defaults.AOUseUV2,
        clampUVX: Optional[bool] = Defaults.clampUVX,
        clampUVY: Optional[bool] = Defaults.clampUVY,
        clampUVZ: Optional[bool] = Defaults.clampUVZ,
    ):
        self.AOUseUV2 = AOUseUV2
        self.clampUVX = clampUVX
        self.clampUVY = clampUVY
        self.clampUVZ = clampUVZ
        self.UVOffsetU = UVOffsetU
        self.UVOffsetV = UVOffsetV
        self.UVTilingU = UVTilingU
        self.UVTilingV = UVTilingV
        self.UVRotation = UVRotation


class AsoboMaterialShadowOptions:
    class Defaults:
        noCastShadow = False

    SerializedName = "ASOBO_material_shadow_options"

    def __init__(self, noCastShadow: Optional[bool] = Defaults.noCastShadow):
        self.noCastShadow = noCastShadow


class AsoboMaterialResponsiveAAOptions:
    class Defaults:
        responsiveAA = False

    SerializedName = "ASOBO_material_antialiasing_options"

    def __init__(self, responsiveAA: Optional[bool] = Defaults.responsiveAA):
        self.responsiveAA = responsiveAA


# materials
class AsoboMaterialFakeTerrain:

    SerializedName = "ASOBO_material_fake_terrain"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled


class AsoboMaterialFresnelFade:
    class Defaults:
        fresnelFactor = 1.0
        fresnelOpacityOffset = 1.0

    SerializedName = "ASOBO_material_fresnel_fade"

    def __init__(
        self,
        fresnelFactor: Optional[float] = Defaults.fresnelFactor,
        fresnelOpacityOffset: Optional[float] = Defaults.fresnelOpacityOffset,
    ):
        self.fresnelFactor = fresnelFactor
        self.fresnelOpacityOffset = fresnelOpacityOffset


class AsoboMaterialDetail:
    class Defaults:
        UVScale = 1.0
        UVOffset = [0.0, 0.0]
        blendThreshold = 0.1
        NormalScale = 1.0

    SerializedName = "ASOBO_material_detail_map"

    def __init__(
        self,
        detailColorTexture: gltf2_io.Texture,
        detailNormalTexture: gltf2_io.Texture,
        detailMetalRoughAOTexture: gltf2_io.Texture,
        blendMaskTexture: gltf2_io.Texture,
        UVOffset: Tuple[float, float] = tuple(Defaults.UVOffset),
        UVScale: Optional[float] = Defaults.UVScaleV,
        blendThreshold: Optional[float] = Defaults.blendThreshold,
    ):
        self.UVScale = UVScale
        self.UVOffset = UVOffset
        self.blendThreshold = blendThreshold
        self.detailColorTexture = detailColorTexture
        self.detailNormalTexture = detailNormalTexture
        self.detailMetalRoughAOTexture = detailMetalRoughAOTexture
        self.blendMaskTexture = blendMaskTexture
        # TODO: NormalScale?


class AsoboSSS:
    class Defaults:
        SSSColor = [1.0, 1.0, 1.0, 1.0]

    SerializedName = "ASOBO_material_SSS"

    def __init__(
        self,
        opacityTexture: gltf2_io.Texture,
        SSSColor: tuple[float, float, float, float] = tuple(Defaults.SSSColor),
    ):
        self.SSSColor = SSSColor
        self.opacityTexture = opacityTexture


class AsoboAnisotropic:

    SerializedName = "ASOBO_material_anisotropic"

    def __init__(self, anisotropicTexture: gltf2_io.Texture):
        self.anisotropicTexture = anisotropicTexture


class AsoboWindshield:
    class Defaults:
        rainDropScale = 1.0
        wiper1State = 0.0
        wiper2State = 0.0
        wiper3State = 0.0
        wiper4State = 0.0

    SerializedName = "ASOBO_material_windshield_v2"

    def __init__(
        self,
        rainDropScale: Optional[float] = Defaults.rainDropScale,
        wiper1State: Optional[float] = Defaults.wiper1State,
        wiper2State: Optional[float] = Defaults.wiper2State,
        wiper3State: Optional[float] = Defaults.wiper3State,
        wiper4State: Optional[float] = Defaults.wiper4State,
    ):
        self.rainDropScale = rainDropScale
        self.wiper1State = wiper1State
        self.wiper2State = wiper2State
        self.wiper3State = wiper3State
        self.wiper4State = wiper4State


class AsoboClearCoat:

    SerializedName = "ASOBO_material_clear_coat"

    def __init__(self, dirtTexture: gltf2_io.Texture):
        self.dirtTexture = dirtTexture


class AsoboParallaxWindow:
    class Defaults:
        parallaxScale = 0.0
        roomSizeXScale = 1.0
        roomSizeYScale = 1.0
        roomNumberXY = 1.0
        corridor = False

    SerializedName = "ASOBO_material_parallax_window"

    def __init__(
        self,
        parallaxScale: Optional[float] = Defaults.parallaxScale,
        roomSizeXScale: Optional[float] = Defaults.roomSizeXScale,
        roomSizeYScale: Optional[float] = Defaults.roomSizeYScale,
        roomNumberXY: Optional[float] = Defaults.roomNumberXY,
        corridor: Optional[bool] = Defaults.corridor,
    ):
        self.parallaxScale = parallaxScale
        self.roomSizeXScale = roomSizeXScale
        self.roomSizeYScale = roomSizeYScale
        self.roomNumberXY = roomNumberXY
        self.corridor = corridor


class AsoboGlass:
    class Defaults:
        glassReflectionMaskFactor = 0.0
        glassDeformationFactor = 0.0

    SerializedName = "ASOBO_material_glass"

    def __init__(
        self,
        glassReflectionMaskFactor: Optional[float] = Defaults.glassReflectionMaskFactor,
        glassDeformationFactor: Optional[float] = Defaults.glassDeformationFactor,
    ):
        self.glassReflectionMaskFactor = glassReflectionMaskFactor
        self.glassDeformationFactor = glassDeformationFactor


class AsoboBaseMaterial:
    class Defaults:
        BaseColorFactor = [1.0, 1.0, 1.0, 1.0]
        EmissiveFactor = [0.0, 0.0, 0.0]
        MetallicFactor = 1.0
        RoughnessFactor = 1.0

        NormalScale = 1.0
        OcclusionStrength = 1.0

        AlphaMode = "OPAQUE"
        AlphaCutoff = 0.5
        DoubleSided = False

        # TODO: these are defined in 3ds max - maybe needed?
        # BaseColorBlendFactor = 1.0
        # MetallicBlendFactor = 1.0
        # RoughnessBlendFactor = 1.0
        # NormalBlendFactor = 1.0
        # EmissiveBlendFactor = 1.0
        # OcclusionBlendFactor = 1.0


# bpy things


class BlenderMaterialProperties:
    Material.base_color_factor = FloatVectorProperty(
        name="Base Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=AsoboBaseMaterial.Defaults.BaseColorFactor,
    )
    Material.emissive_factor = FloatVectorProperty(
        name="Emissive Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=3,
        default=AsoboBaseMaterial.Defaults.EmissiveFactor,
    )
    Material.sss_color = FloatVectorProperty(
        name="SSS Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=AsoboSSS.Defaults.SSSColor,
    )

    # TODO: add rest of properties, cleanup unneeded things, consolidate to common places, define animatable properties. add to dict and to class like in gltf2_io
