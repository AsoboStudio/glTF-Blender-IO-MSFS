# glTF-Blender-IO-MSFS
# Copyright (C) 2020-2021 The glTF-Blender-IO-MSFS authors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bpy
from bpy.types import Material, Image
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, FloatVectorProperty, PointerProperty

from .msfs_material import *
from .msfs_material_standard import *
from .msfs_material_anisotropic import *
from .msfs_material_clearcoat import *
from .msfs_material_decal import *
from .msfs_material_envoccluder import *
from .msfs_material_faketerrain import *
from .msfs_material_fresnel import *
from .msfs_material_glass import *
from .msfs_material_hair import *
from .msfs_material_sss import *
from .msfs_material_invisible import *
from .msfs_material_geodecal import *
from .msfs_material_porthole import *
from .msfs_material_windshield import *
from .msfs_material_parallax import *
class MSFS_LI_material():

    # Use this function to update the shader node tree
    def switch_msfs_material(self,context):
        mat = context.active_object.active_material
        msfs_mat = None
        if mat.msfs_material_mode.value == 'msfs_standard':
            msfs_mat = MSFS_Standard(mat)
            print("Switched to msfs_standard material.")
        elif mat.msfs_material_mode.value == 'msfs_anisotropic':
            msfs_mat =MSFS_Anisotropic(mat)
            print("Switched to msfs_anisotropic material.")
        elif mat.msfs_material_mode.value == 'msfs_sss':
            msfs_mat = MSFS_SSS(mat)
            print("Switched to msfs_sss material.")
        elif mat.msfs_material_mode.value == 'msfs_glass':
            msfs_mat = MSFS_Glass(mat)
            print("Switched to msfs_glass material.")
        elif mat.msfs_material_mode.value == 'msfs_decal':
            msfs_mat = MSFS_Decal(mat)
            print("Switched to msfs_decal material.")
        elif mat.msfs_material_mode.value == 'msfs_clearcoat':
            msfs_mat = MSFS_Clearcoat(mat)
            print("Switched to msfs_clearcoat material.")
        elif mat.msfs_material_mode.value == 'msfs_env_occluder':
            msfs_mat = MSFS_EnvOccluder(mat)
            print("Switched to msfs_env_occluder material.")
        elif mat.msfs_material_mode.value == 'msfs_fake_terrain':
            msfs_mat = MSFS_FakeTerrain(mat)
            print("Switched to msfs_fake_terrain material.")
        elif mat.msfs_material_mode.value == 'msfs_fresnel':
            msfs_mat = MSFS_Fresnel(mat)
            print("Switched to msfs_fresnel material.")
        elif mat.msfs_material_mode.value == 'msfs_windshield':
            msfs_mat = MSFS_Windshield(mat)            
            print("Switched to msfs_windshield material.")
        elif mat.msfs_material_mode.value == 'msfs_porthole':
            msfs_mat = MSFS_PortHole(mat)
            print("Switched to msfs_porthole material.")
        elif mat.msfs_material_mode.value == 'msfs_parallax':
            msfs_mat = MSFS_Parallax(mat)
            print("Switched to msfs_parallax material.")
        elif mat.msfs_material_mode.value == 'msfs_geo_decal':
            msfs_mat = MSFS_GeoDecal(mat)
            print("Switched to msfs_geo_decal material.")
        elif mat.msfs_material_mode.value == 'msfs_hair':
            msfs_mat = MSFS_Hair(mat)
            print("Switched to msfs_hair material.")
        elif mat.msfs_material_mode.value == 'msfs_invisible':
            msfs_mat = MSFS_Invisible(mat)
            print("Switched to msfs_invisible material.")
        else:
            msfs_mat = MSFS_Material(mat)
            print("Switched to non-sim material.")

        msfs_mat.buildShaderTree()

    def match_base_color_tex(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        base_color_tex = nodes.get(MSFS_ShaderNodes.baseColorTex.value)
        if not base_color_tex:
            return
        base_color_tex.image = mat.msfs_albedo_texture

    def match_comp_tex(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        comp_tex = nodes.get(MSFS_ShaderNodes.compTex.value)
        if not comp_tex:
            return
        comp_tex.image = mat.msfs_metallic_texture

    def match_normal_tex(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        normalTex = nodes.get(MSFS_ShaderNodes.normalTex.value)
        if not normalTex:
            return
        normalTex.image = mat.msfs_normal_texture

    def match_emissive_tex(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        emissiveTex = nodes.get(MSFS_ShaderNodes.emissiveTex.value)
        if not emissiveTex:
            return
        emissiveTex.image = mat.msfs_emissive_texture

    def match_detail_color(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        detailColorTex = nodes.get(MSFS_ShaderNodes.detailColorTex.value)
        blendColorMapNode =  nodes.get(MSFS_ShaderNodes.blendColorMap.value)
        if not detailColorTex or not blendColorMapNode:
            return
        detailColorTex.image = mat.msfs_detail_albedo_texture
        blendColorMapNode.inputs[0].default_value = 0 if mat.msfs_detail_albedo_texture == None else 1

    def match_detail_comp(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        detailCompTex = nodes.get(MSFS_ShaderNodes.detailCompTex.value)
        blendCompMapNode =  nodes.get(MSFS_ShaderNodes.blendCompMap.value)  
        if not detailCompTex or not blendCompMapNode:
            return
        detailCompTex.image = mat.msfs_detail_metallic_texture
        blendCompMapNode.inputs[0].default_value = 0 if mat.msfs_detail_metallic_texture == None else 1

    def match_detail_normal(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        detailNormalTex = nodes.get(MSFS_ShaderNodes.detailNormalTex.value)
        blendNormalMapNode =  nodes.get(MSFS_ShaderNodes.blendNormalMap.value)
        if not detailNormalTex:
            return
        detailNormalTex.image = mat.msfs_detail_normal_texture
        blendNormalMapNode.inputs[0].default_value = 0 if mat.msfs_detail_normal_texture == None else 1

    def match_blend_mask(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        blendTex = nodes.get(MSFS_ShaderNodes.blendMaskTex.value)
        if not blendTex:
            return
        blendTex.image = mat.msfs_blend_mask_texture
        if mat.msfs_material_mode.value == 'msfs_standard':
            msfs_mat = MSFS_Standard(mat)
            msfs_mat = msfs_mat.toggleVertexBlendMapMask(mat.msfs_blend_mask_texture is None)


    def match_anisotropic_direction(self,context):
        mat = context.activate_object.active_material
        if mat.node_tree.nodes.get("anisotropic_direction", None) != None:
            mat.node_tree.nodes["anisotropic_direction"].image = mat.msfs_anisotropic_direction_texture
            mat.node_tree.nodes["anisotropic_direction"].image.colorspace_settings.name = 'Non-Color'

    def match_clearcoat(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        clearcoat = nodes.get("clearcoat")
        clearcoat_sep = nodes.get("clearcoat_sep")
        bsdf_node = nodes.get("bsdf")

        if clearcoat != None:
            mat.node_tree.nodes["clearcoat"].image = mat.msfs_clearcoat_texture
            mat.node_tree.nodes["clearcoat"].image.colorspace_settings.name = 'Non-Color'
            if (clearcoat_sep != None and bsdf_node != None):
                if mat.msfs_clearcoat_texture.name != "":
                    links.new(clearcoat_sep.outputs["R"],bsdf_node.inputs["Clearcoat"])
                    links.new(clearcoat_sep.outputs["G"],bsdf_node.inputs["Clearcoat Roughness"])
                else:
                    l = bsdf_node.inputs["Clearcoat"].links[0]
                    links.remove(l)                
                    l = bsdf_node.inputs["Clearcoat Roughness"].links[0]
                    links.remove(l)

    def match_behind_glass(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        #Try to generate the links:
        albedo_detail_mix = nodes.get("albedo_detail_mix")
        behind_glass = nodes.get("behind_glass")

        if behind_glass != None:
            mat.node_tree.nodes["behind_glass"].image = mat.msfs_behind_glass_texture
            if mat.msfs_behind_glass_texture.name != "":
                # Create the link:
                if (behind_glass != None and albedo_detail_mix != None):
                    links.new(behind_glass.outputs["Color"], albedo_detail_mix.inputs["Color2"])
            else:
                #unlink the separator:
                if (behind_glass != None and albedo_detail_mix != None):
                    l = albedo_detail_mix.inputs["Color2"].links[0]
                    links.remove(l)                

    def match_wiper_mask(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links


    def switch_msfs_blendmode(self, context):
        mat = context.active_object.active_material
        msfs_mat = MSFS_Material(mat)
        if mat.msfs_blend_mode.value == 'BLEND':
            msfs_mat.makeAlphaBlend()
        elif mat.msfs_blend_mode.value == 'MASKED':
            msfs_mat.makeMasked()
        elif mat.msfs_blend_mode.value == 'DITHER':
            msfs_mat.makeDither()
        else:
            msfs_mat.makeOpaque()

    #Update functions for the "tint" parameters:
    def set_base_color(self, value):
        mat = self.id_data
        nodes = mat.node_tree.nodes
        nodeColorRGB = nodes.get(MSFS_ShaderNodes.baseColorRGB.value)
        if not nodeColorRGB:
            return
        colorValue=nodeColorRGB.outputs[0].default_value
        colorValue[0] = value[0]
        colorValue[1] = value[1]
        colorValue[2] = value[2]
        nodes.get(MSFS_ShaderNodes.baseColorA.value).outputs[0].default_value = value[3]

        self["value"] = value

    def get_base_color(self):
        return self.get("value", [1.0, 1.0, 1.0, 1.0])

    def set_emissive_color(self, value):
        mat = self.id_data
        nodes = mat.node_tree.nodes
        nodeEmissiveColorRGB = nodes.get(MSFS_ShaderNodes.emissiveColor.value)
        if not nodeEmissiveColorRGB:
            return
        emissiveValue = nodeEmissiveColorRGB.outputs[0].default_value
        emissiveValue[0] = value[0]
        emissiveValue[1] = value[1]
        emissiveValue[2] = value[2]

        self["value"] = value

    def get_emissive_color(self):
        return self.get("value", [0.0, 0.0, 0.0, 0.0])

    def match_emissive_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        emissiveScale =nodes.get(MSFS_ShaderNodes.emissiveScale.value)
        if not emissiveScale:
            return
        emissiveScale.outputs[0].default_value = mat.msfs_emissive_scale.value

    def match_metallic_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node = nodes.get(MSFS_ShaderNodes.metallicScale.value)
        if node:
            node.outputs[0].default_value = mat.msfs_metallic_scale.value

    def match_roughness_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node =nodes.get(MSFS_ShaderNodes.roughnessScale.value)
        if node:
            node.outputs[0].default_value = mat.msfs_roughness_scale.value

    def match_normal_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node = nodes.get(MSFS_ShaderNodes.normalScale.value)
        if node:
            node.outputs[0].default_value = mat.msfs_normal_scale.value

    def update_color_sss(self, context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs.get("Subsurface Color").default_value = mat.msfs_color_sss.value

    def update_double_sided(self, context):
        mat = context.active_object.active_material
        mat.use_backface_culling = not mat.msfs_double_sided.value

    def match_alpha_cutoff(self,context):
        mat = context.active_object.active_material
        mat.alpha_threshold = mat.msfs_alpha_cutoff.value

    def match_detail_uv(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        detailUvScaleNode = nodes.get(MSFS_ShaderNodes.detailUVScale.value)
        detailUvOffsetUNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetU.value)
        detailUvOffsetVNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetV.value)
        detailNormalScaleNode = nodes.get(MSFS_ShaderNodes.detailNormalScale.value)
        if detailUvScaleNode and detailUvOffsetUNode and detailUvOffsetVNode and detailNormalScaleNode:
            detailUvScaleNode.outputs[0].default_value = mat.msfs_detail_uv_scale.value
            detailUvOffsetUNode.outputs[0].default_value = mat.msfs_detail_uv_offset_x.value
            detailUvOffsetVNode.outputs[0].default_value = mat.msfs_detail_uv_offset_y.value
            detailNormalScaleNode.outputs[0].default_value = mat.msfs_detail_normal_scale.value

    def create_material_property_group(value, animated=False):
        # To make it easier to enable certain material properties to be animated, we need to create a custom property group class with the value and animated property
        property_group = type(
            "MaterialPropertyGroup",
            (bpy.types.PropertyGroup,),
            {
                "__annotations__": {
                    "value": value,
                    "animated": BoolProperty(default=animated)
                }
            }
        )

        bpy.utils.register_class(property_group)

        return PointerProperty(type=property_group)     


    # Some flags to control the visibility of all of the paramters in the UI. 
    # Note: they don't control the actualy material parameters, only whether or 
    # not those parameters are being displayed. 
    Material.msfs_show_tint = BoolProperty(name="show_tint",default=False)
    Material.msfs_show_sss_color = BoolProperty(name="show_sss_color",default=False)

    Material.msfs_show_glass_parameters = BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_windshield_options = BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_decal_parameters = BoolProperty(name="show_decal_parameters",default=False)
    Material.msfs_show_fresnel_parameters = BoolProperty(name="show_fresnel_parameters",default=False)
    Material.msfs_show_parallax_parameters = BoolProperty(name="show_parallax_parameters",default=False)
    Material.msfs_show_geo_decal_parameters = BoolProperty(name="show_geo_decal_parameters",default=False)

    Material.msfs_show_albedo = BoolProperty(name="show_albedo",default=False)
    Material.msfs_show_metallic = BoolProperty(name="show_metallic",default=False)
    Material.msfs_show_normal = BoolProperty(name="show_normal",default=False)
    Material.msfs_show_emissive = BoolProperty(name="show_emissive",default=False)
    Material.msfs_show_detail_albedo = BoolProperty(name="show_detail_albedo",default=False)
    Material.msfs_show_detail_metallic = BoolProperty(name="show_detail_metallic",default=False)
    Material.msfs_show_detail_normal = BoolProperty(name="show_detail_normal",default=False)
    Material.msfs_show_blend_mask = BoolProperty(name="show_blend_mask",default=False)
    Material.msfs_show_anisotropic_direction = BoolProperty(name="show_anisotropic_direction",default=False)
    Material.msfs_show_clearcoat = BoolProperty(name="show_clearcoat",default=False)
    Material.msfs_show_behind_glass = BoolProperty(name="show_behind_glass",default=False)
    Material.msfs_show_wiper_mask = BoolProperty(name="show_wiper_mask",default=False)

    Material.msfs_show_blend_mode = BoolProperty(name="show_blend_mode",default=False)

    Material.msfs_show_draworder = BoolProperty(name="show_draworder",default=False)
    Material.msfs_show_no_cast_shadow = BoolProperty(name="show_no_cast_shadow",default=False)
    Material.msfs_show_double_sided = BoolProperty(name="show_double_sided",default=False)
    Material.msfs_show_responsive_aa = BoolProperty(name="show_responsive_aa",default=False)
    Material.msfs_show_day_night_cycle = BoolProperty(name="show_day_night_cycle",default=False)

    Material.msfs_show_collision_material = BoolProperty(name="show_collision_material",default=False)
    Material.msfs_show_road_material = BoolProperty(name="show_road_material",default=False)

    Material.msfs_show_ao_use_uv2 = BoolProperty(name="show_ao_use_uv2",default=False)
    Material.msfs_show_uv_clamp = BoolProperty(name="show_uv_clamp",default=False)

    Material.msfs_show_alpha_cutoff = BoolProperty(name="show_alpha_cutoff",default=False)
    Material.msfs_show_blend_threshold = BoolProperty(name="show_blend_threshold",default=False)
    Material.msfs_show_pearl = BoolProperty(name="show_pearl",default=False)

    # MSFS Material properties
    # The following variables are written into the glTF file when exporting.

    # Main material mode, in accordance with MSFS material shaders:
    Material.msfs_material_mode = create_material_property_group(
        EnumProperty(
            items=(
                ("NONE", "Disabled", ""),
                ("msfs_standard", "MSFS Standard", ""),
                ("msfs_anisotropic", "MSFS Anisotropic", ""),
                ("msfs_sss", "MSFS Subsurface Scattering", ""),
                ("msfs_glass", "MSFS Glass", ""),
                ("msfs_decal", "MSFS Decal", ""),
                ("msfs_clearcoat", "MSFS Clearcoat", ""),
                ("msfs_env_occluder", "MSFS Environment Occluder", ""),
                ("msfs_fake_terrain", "MSFS Fake Terrain", ""),
                ("msfs_fresnel", "MSFS Fresnel Blending", ""),
                ("msfs_windshield", "MSFS Windshield", ""),
                ("msfs_porthole", "MSFS Porthole", ""),
                ("msfs_parallax", "MSFS Parallax", ""),
                ("msfs_geo_decal", "MSFS Geo Decal Frosted", ""),
                ("msfs_hair", "MSFS Hair", ""),
                ("msfs_invisible", "MSFS Invisible", ""),
            ),
            default="NONE",
            update=switch_msfs_material,
        ), animated=False
    )

    # Color blends:
    Material.msfs_color_albedo_mix = create_material_property_group(
        FloatVectorProperty(
            name="Albedo Color",
            subtype="COLOR",
            min=0.0,
            max=1.0,
            size=4,
            default=[1.0, 1.0, 1.0, 1.0],
            description="The color value set here will be mixed in with the albedo value of the material.",
            set=set_base_color,
            get=get_base_color,
        ), animated=True
    )
    Material.msfs_color_emissive_mix = create_material_property_group(
        FloatVectorProperty(
            name="Emissive Color",
            subtype="COLOR",
            min=0.0,
            max=1.0,
            size=4,
            default=[0.0, 0.0, 0.0, 0.0],
            description="The color value set here will be mixed in with the emissive value of the material.",
            set=set_emissive_color,
            get=get_emissive_color,
        ), animated=True
    )
    Material.msfs_color_sss = create_material_property_group(
        FloatVectorProperty(
            name="SSS Color",
            subtype="COLOR",
            min=0.0,
            max=1.0,
            size=4,
            default=[1.0, 1.0, 1.0, 1.0],
            description="Use the color picker to set the color of the subsurface scattering.",
            update=update_color_sss,
        ), animated=False
    )

    # Windshield
    Material.msfs_rain_drop_scale = create_material_property_group(
        FloatProperty(
            name="Rain Drop Scale", min=0.0, max=100.0, default=1.0
        ), animated=False
    )
    Material.msfs_wiper_1_state = create_material_property_group(
        FloatProperty(
            name="Wiper 1 State", min=0.0, max=1.0, default=0.0
        ), animated=False
    )
    Material.msfs_wiper_2_state = create_material_property_group(
        FloatProperty(
            name="Wiper 2 State", min=0.0, max=1.0, default=0.0
        ), animated=False
    )  
    # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible
    Material.msfs_wiper_3_state = create_material_property_group(
        FloatProperty(
            name="Wiper 1 State", min=0.0, max=1.0, default=0.0
        ), animated=False
    )
    Material.msfs_wiper_4_state = create_material_property_group(
        FloatProperty(
            name="Wiper 1 State", min=0.0, max=1.0, default=0.0
        ), animated= False
    )

    # Glass parameters:
    Material.msfs_glass_reflection_mask_factor = create_material_property_group(
        FloatProperty(
            name="Reflection mask factor", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_glass_deformation_factor = create_material_property_group(
        FloatProperty(
            name="Deformation factor", min=0.0, max=1.0, default=0.0
        ), animated=False
    )

    # Pearl

    Material.msfs_use_pearl_effect = create_material_property_group(
        BoolProperty(
            name="Use Pearl Effect", default=False
        ), animated=False
    )
    Material.msfs_pearl_shift = create_material_property_group(
        FloatProperty(
            name="Color Shift", min=-999.0, max=999.0, default=0.0
        ), animated=False
    )
    Material.msfs_pearl_range = create_material_property_group(
        FloatProperty(
            name="Color Range", min=-999.0, max=999.0, default=0.0
        ), animated=False
    )
    Material.msfs_pearl_brightness = create_material_property_group(
        FloatProperty(
            name="Color Brightness", min=-1.0, max=1.0, default=0.0
        ), animated=False
    )

    # Decal parameters:
    Material.msfs_decal_blend_factor_color = create_material_property_group(
        FloatProperty(
            name="Color", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_decal_blend_factor_metal = create_material_property_group(
        FloatProperty(
            name="Metal", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_decal_blend_factor_normal = create_material_property_group(
        FloatProperty(
            name="Normal", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_decal_blend_factor_roughness = create_material_property_group(
        FloatProperty(
            name="Roughness", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_decal_blend_factor_occlusion = create_material_property_group(
        FloatProperty(
            name="Occlusion", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_decal_blend_factor_emissive = create_material_property_group(
        FloatProperty(
            name="Emissive", min=0.0, max=1.0, default=1.0
        ), animated=False
    )

    # Fresnel parameters:
    Material.msfs_fresnel_factor = create_material_property_group(
        FloatProperty(
            name="Fresnel factor", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_fresnel_opacity_bias = create_material_property_group(
        FloatProperty(
            name="Fresnel opacity bias", min=0.0, max=1.0, default=1.0
        ), animated=False
    )

    # Parallax parameters:
    Material.msfs_parallax_scale = create_material_property_group(
        FloatProperty(
            name="Scale", min=0.0, max=1.0, default=0.0
        ), animated=False
    )
    Material.msfs_parallax_room_size_x = create_material_property_group(
        FloatProperty(
            name="X", min=0.0, default=0.5
        ), animated=False
    )
    Material.msfs_parallax_room_size_y = create_material_property_group(
        FloatProperty(
            name="Y", min=0.0, default=0.5
        ), animated=False
    )
    Material.msfs_parallax_room_number = create_material_property_group(
        FloatProperty(
            name="Rm number XY", min=0.0, default=1.0
        ), animated=False
    )
    Material.msfs_parallax_corridor = create_material_property_group(
        BoolProperty(
            name="Corridor", default=False
        ), animated=False
    )

    # Geo Decal Frosted parameters:
    Material.msfs_geo_decal_blend_factor_color = create_material_property_group(
        FloatProperty(
            name="Color", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_geo_decal_blend_factor_metal = create_material_property_group(
        FloatProperty(
            name="Metal", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_geo_decal_blend_factor_normal = create_material_property_group(
        FloatProperty(
            name="Normal", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_geo_decal_blend_factor_roughness = create_material_property_group(
        FloatProperty(
            name="Roughness", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_geo_decal_blend_factor_blast_sys = create_material_property_group(
        FloatProperty(
            name="Blast Sys.", min=0.0, max=1.0, default=1.0
        ), animated=False
    )
    Material.msfs_geo_decal_blend_factor_melt_sys = create_material_property_group(
        FloatProperty(
            name="Melt Sys", min=0.0, max=1.0, default=1.0
        ), animated=False
    )

    # Textures:
    Material.msfs_albedo_texture = PointerProperty(type = Image, name = "Albedo map", update = match_base_color_tex)
    Material.msfs_metallic_texture = PointerProperty(type = Image, name = "Metallic map", update = match_comp_tex)
    Material.msfs_normal_texture = PointerProperty(type = Image, name = "Normal map", update = match_normal_tex)
    Material.msfs_emissive_texture = PointerProperty(type = Image, name = "Emissive map", update = match_emissive_tex)

    Material.msfs_detail_albedo_texture = PointerProperty(type = Image, name = "Detail Color map", update = match_detail_color)
    Material.msfs_detail_metallic_texture = PointerProperty(type = Image, name = "Detail Metallic map", update = match_detail_comp)
    Material.msfs_detail_normal_texture = PointerProperty(type = Image, name = "Detail Normal map", update = match_detail_normal)

    Material.msfs_blend_mask_texture = PointerProperty(type = Image, name = "Blend mask", update = match_blend_mask)

    Material.msfs_anisotropic_direction_texture = PointerProperty(type = Image, name = "Anisotropic direction (RG)", update = match_anisotropic_direction)
    Material.msfs_clearcoat_texture = PointerProperty(type = Image, name = "Clearcoat amount (R), Clearcoat rough (G)", update = match_clearcoat)
    Material.msfs_behind_glass_texture = PointerProperty(type = Image, name = "Behind glass Albedo map", update = match_behind_glass)
    Material.msfs_wiper_mask_texture = PointerProperty(type = Image, name = "Wiper mask (RG)", update = match_wiper_mask)

    # Alpha mode:
    Material.msfs_blend_mode = create_material_property_group(
        EnumProperty(
            name="Blend mode",
            items=(
                ("OPAQUE", "Opaque", "Creates a fully non-transparent material."),
                (
                    "MASKED",
                    "Masked",
                    "This blend mode uses the alpha map to mask off parts of the material, but only if the alpha value exceeds the value set in the alpha cutoff parameter.",
                ),
                (
                    "BLEND",
                    "Blend",
                    "This blend mode uses the alpha map to gradually blend in the material. Use this for materials like glass.",
                ),
                (
                    "DITHER",
                    "Dither",
                    "Weird blend mode. But works well for hair. No visible effect in Blender.",
                ),
            ),
            default="OPAQUE",
            update=switch_msfs_blendmode,
        ), animated=False
    )

    # Render parameters:
    Material.msfs_draw_order = create_material_property_group(
        IntProperty(
            name="Draw order", default=0, min=0
        ), animated=False
    )
    Material.msfs_no_cast_shadow = create_material_property_group(
        BoolProperty(
            name="No cast shadow", default=False
        ), animated=False
    )
    Material.msfs_double_sided = create_material_property_group(
        BoolProperty(
            name="Double sided", default=False, update=update_double_sided
        ), animated=False
    )
    Material.msfs_responsive_aa = create_material_property_group(
        BoolProperty(
            name="Responsive AA", default=False, description=""
        ), animated=False
    )
    Material.msfs_day_night_cycle = create_material_property_group(
        BoolProperty(
            name="Day/Night cycle", default=False
        ), animated=False
    )

    # Gameplay parameters:
    Material.msfs_collision_material = create_material_property_group(
        BoolProperty(
            name="Collision material", default=False
        ), animated=False
    )
    Material.msfs_road_material = create_material_property_group(
        BoolProperty(
            name="Road material", default=False
        ), animated=False
    )

    # UV options:

    Material.msfs_uv_offset_u = create_material_property_group(
        FloatProperty(
            name="U", min=-10.0, max=10.0, default=0.0
        ), animated=True
    )
    Material.msfs_uv_offset_v = create_material_property_group(
        FloatProperty(
            name="V", min=-10.0, max=10.0, default=0.0
        ), animated=True
    )
    Material.msfs_uv_tiling_u = create_material_property_group(
        FloatProperty(
            name="U", min=-10.0, max=10.0, default=1.0
        ), animated=True
    )
    Material.msfs_uv_tiling_v = create_material_property_group(
        FloatProperty(
            name="V", min=-10.0, max=10.0, default=1.0
        ), animated=True
    )
    Material.msfs_uv_rotation = create_material_property_group(
        FloatProperty(
            name="UV Rotation", min=-360.0, max=360.0, default=0.0
        ), animated=True
    )
    Material.msfs_ao_use_uv2 = create_material_property_group(
        BoolProperty(
            name="AO use UV2", default=False
        ), animated=False
    )
    Material.msfs_uv_clamp_x = create_material_property_group(
        BoolProperty(
            name="X", default=False
        ), animated=False
    )
    Material.msfs_uv_clamp_y = create_material_property_group(
        BoolProperty(
            name="Y", default=False
        ), animated=False
    )
    Material.msfs_uv_clamp_z = create_material_property_group(
        BoolProperty(
            name="Z", default=False
        ), animated=False
    )

    # Material parameters
    Material.msfs_roughness_scale = create_material_property_group(
        FloatProperty(
            name="Roughness scale", min=0, max=1, default=1, update=match_roughness_scale
        ), animated=True
    )
    Material.msfs_metallic_scale = create_material_property_group(
        FloatProperty(
            name="Metallic scale", min=0, max=1, default=1, update=match_metallic_scale
        ), animated=True
    )
    Material.msfs_emissive_scale = create_material_property_group(
        FloatProperty(
            name="Emissive scale", min=0, max=1, default=1, update=match_emissive_scale
        ), animated=False
    )
    Material.msfs_normal_scale = create_material_property_group(
        FloatProperty(
            name="Normal scale", min=0, default=1, update=match_normal_scale
        ), animated=False
    )
    Material.msfs_alpha_cutoff = create_material_property_group(
        FloatProperty(
            name="Alpha cutoff", min=0, max=1, default=0.1, update=match_alpha_cutoff
        ), animated=False
    )
    Material.msfs_detail_uv_scale = create_material_property_group(
        FloatProperty(
            name="Detail UV scale", min=0, default=1, update=match_detail_uv
        ), animated=False
    )
    Material.msfs_detail_uv_offset_x = create_material_property_group(
        FloatProperty(
            name="X", min=-1, max=1, default=0, update=match_detail_uv
        ), animated=False
    )
    Material.msfs_detail_uv_offset_y = create_material_property_group(
        FloatProperty(
            name="Y", min=-1, max=1, default=0, update=match_detail_uv
        ), animated=False
    )
    Material.msfs_detail_normal_scale = create_material_property_group(
        FloatProperty(
            name="Detail normal scale", min=0, max=1, default=1, update=match_detail_uv
        ), animated=False
    )
    Material.msfs_blend_threshold = create_material_property_group(
        FloatProperty(
            name="Blend threshold", min=0, max=1, default=0.1
        ), animated=False
    )