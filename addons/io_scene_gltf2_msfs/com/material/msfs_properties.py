# glTF-Blender-IO-MSFS
# Copyright (C) 2020-2022 The glTF-Blender-IO-MSFS authors

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
from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty, EnumProperty, FloatVectorProperty, PointerProperty

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

def getMaterial(mat):
        if mat.msfs_material_mode == 'msfs_standard':
          return MSFS_Standard(mat)
        if mat.msfs_material_mode == 'msfs_anisotropic':
          return MSFS_Anisotropic(mat)
        if mat.msfs_material_mode == 'msfs_sss':
          return MSFS_SSS(mat)  
        if mat.msfs_material_mode == 'msfs_glass':
          return MSFS_Glass(mat)  
        if mat.msfs_material_mode == 'msfs_decal':
          return MSFS_Decal(mat)  
        if mat.msfs_material_mode == 'msfs_clearcoat':
          return MSFS_Clearcoat(mat)  
        if mat.msfs_material_mode == 'msfs_env_occluder':
          return MSFS_EnvOccluder(mat)  
        if mat.msfs_material_mode == 'msfs_fake_terrain':
          return MSFS_FakeTerrain(mat)
        if mat.msfs_material_mode == 'msfs_fresnel':
          return MSFS_Fresnel(mat)
        if mat.msfs_material_mode == 'msfs_windshield':
          return MSFS_Windshield(mat)
        if mat.msfs_material_mode == 'msfs_porthole':
          return MSFS_PortHole(mat)
        if mat.msfs_material_mode == 'msfs_parallax':
          return MSFS_Parallax(mat)
        if mat.msfs_material_mode == 'msfs_geo_decal':
          return MSFS_GeoDecal(mat) 
        if mat.msfs_material_mode == 'msfs_hair':
          return MSFS_Hair(mat)
        if mat.msfs_material_mode == 'msfs_invisible':
          return MSFS_Invisible(mat) 
class MSFS_LI_material():

    # Use this function to update the shader node tree
    def switch_msfs_material(self,context):
        mat = context.active_object.active_material
        msfs_mat = None
        if mat.msfs_material_mode == 'msfs_standard':
            msfs_mat = MSFS_Standard(mat,buildTree = True)
            print("Switched to msfs_standard material.")
        elif mat.msfs_material_mode == 'msfs_anisotropic':
            msfs_mat =MSFS_Anisotropic(mat,buildTree = True)
            print("Switched to msfs_anisotropic material.")
        elif mat.msfs_material_mode == 'msfs_sss':
            msfs_mat = MSFS_SSS(mat,buildTree = True)
            print("Switched to msfs_sss material.")
        elif mat.msfs_material_mode == 'msfs_glass':
            msfs_mat = MSFS_Glass(mat,buildTree = True)
            print("Switched to msfs_glass material.")
        elif mat.msfs_material_mode == 'msfs_decal':
            msfs_mat = MSFS_Decal(mat,buildTree = True)
            print("Switched to msfs_decal material.")
        elif mat.msfs_material_mode == 'msfs_clearcoat':
            msfs_mat = MSFS_Clearcoat(mat,buildTree = True)
            print("Switched to msfs_clearcoat material.")
        elif mat.msfs_material_mode == 'msfs_env_occluder':
            msfs_mat = MSFS_EnvOccluder(mat,buildTree = True)
            print("Switched to msfs_env_occluder material.")
        elif mat.msfs_material_mode == 'msfs_fake_terrain':
            msfs_mat = MSFS_FakeTerrain(mat,buildTree = True)
            print("Switched to msfs_fake_terrain material.")
        elif mat.msfs_material_mode == 'msfs_fresnel':
            msfs_mat = MSFS_Fresnel(mat,buildTree = True)
            print("Switched to msfs_fresnel material.")
        elif mat.msfs_material_mode == 'msfs_windshield':
            msfs_mat = MSFS_Windshield(mat,buildTree = True)            
            print("Switched to msfs_windshield material.")
        elif mat.msfs_material_mode == 'msfs_porthole':
            msfs_mat = MSFS_PortHole(mat,buildTree = True)
            print("Switched to msfs_porthole material.")
        elif mat.msfs_material_mode == 'msfs_parallax':
            msfs_mat = MSFS_Parallax(mat,buildTree = True)
            print("Switched to msfs_parallax material.")
        elif mat.msfs_material_mode == 'msfs_geo_decal':
            msfs_mat = MSFS_GeoDecal(mat,buildTree = True)
            print("Switched to msfs_geo_decal material.")
        elif mat.msfs_material_mode == 'msfs_hair':
            msfs_mat = MSFS_Hair(mat,buildTree = True)
            print("Switched to msfs_hair material.")
        elif mat.msfs_material_mode == 'msfs_invisible':
            msfs_mat = MSFS_Invisible(mat,buildTree = True)
            print("Switched to msfs_invisible material.")
        else:
            msfs_mat = MSFS_Material(mat)
            msfs_mat.revertToPBRShaderTree()
            print("Switched to non-sim material.")
            return 

    

    def match_base_color_tex(self, context):
        msfs = getMaterial(self)
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setBaseColorTex(self.msfs_albedo_texture)
                  

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
        blendColorMapNode.inputs[0].default_value = 0 if mat.msfs_detail_albedo_texture==None else 1 

    def match_detail_comp(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        detailCompTex = nodes.get(MSFS_ShaderNodes.detailCompTex.value)
        blendCompMapNode =  nodes.get(MSFS_ShaderNodes.blendCompMap.value)  
        if not detailCompTex or not blendCompMapNode:
            return
        detailCompTex.image = mat.msfs_detail_metallic_texture
        blendCompMapNode.inputs[0].default_value = 0 if mat.msfs_detail_metallic_texture==None else 1  

    def match_detail_normal(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        detailNormalTex = nodes.get(MSFS_ShaderNodes.detailNormalTex.value)
        blendNormalMapNode =  nodes.get(MSFS_ShaderNodes.blendNormalMap.value)
        if not detailNormalTex:
            return
        detailNormalTex.image = mat.msfs_detail_normal_texture
        blendNormalMapNode.inputs[0].default_value = 0 if mat.msfs_detail_normal_texture==None else 1  

    def match_blend_mask(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        blendTex = nodes.get(MSFS_ShaderNodes.blendMaskTex.value)
        if not blendTex:
            return
        blendTex.image = mat.msfs_blend_mask_texture
        if mat.msfs_material_mode == 'msfs_standard':
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
        msfs_mat = MSFS_Material(self)
        msfs_mat.setBlendMode(self.msfs_blend_mode)
        

    #Update functions for the "tint" parameters:
    def match_base_color(self, context):
        msfs = getMaterial(self)
        msfs.setBaseColor(self.msfs_color_albedo_mix)

    def match_emissive_color(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        nodeEmissiveColorRGB = nodes.get(MSFS_ShaderNodes.emissiveColor.value)
        if not nodeEmissiveColorRGB:
            return
        emissiveValue = nodeEmissiveColorRGB.outputs[0].default_value
        emissiveValue[0]= mat.msfs_color_emissive_mix[0]
        emissiveValue[1]= mat.msfs_color_emissive_mix[1]
        emissiveValue[2]= mat.msfs_color_emissive_mix[2]

    def match_emissive_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        emissiveScale =nodes.get(MSFS_ShaderNodes.emissiveScale.value)
        if not emissiveScale:
            return
        emissiveScale.outputs[0].default_value =  mat.msfs_emissive_scale

    def match_metallic_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node = nodes.get(MSFS_ShaderNodes.metallicScale.value)
        if node:
            node.outputs[0].default_value =  mat.msfs_metallic_scale

    def match_roughness_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node =nodes.get(MSFS_ShaderNodes.roughnessScale.value)
        if node:
            node.outputs[0].default_value =  mat.msfs_roughness_scale

    def match_normal_scale(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        node = nodes.get(MSFS_ShaderNodes.normalScale.value)
        if node:
            node.outputs[0].default_value =  mat.msfs_normal_scale

    def update_color_sss(self, context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs.get("Subsurface Color").default_value = mat.msfs_color_sss

    def update_double_sided(self, context):
        mat = context.active_object.active_material
        mat.use_backface_culling = not mat.msfs_double_sided

    def match_alpha_cutoff(self,context):
        mat = context.active_object.active_material
        mat.alpha_threshold = mat.msfs_alpha_cutoff

    def match_detail_uv(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        detailUvScaleNode = nodes.get(MSFS_ShaderNodes.detailUVScale.value)
        detailUvOffsetUNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetU.value)
        detailUvOffsetVNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetV.value)
        detailNormalScaleNode = nodes.get(MSFS_ShaderNodes.detailNormalScale.value)
        if detailUvScaleNode and detailUvOffsetUNode and detailUvOffsetVNode and detailNormalScaleNode:
            detailUvScaleNode.outputs[0].default_value =  mat.msfs_detail_uv_scale
            detailUvOffsetUNode.outputs[0].default_value =  mat.msfs_detail_uv_offset_x
            detailUvOffsetVNode.outputs[0].default_value =  mat.msfs_detail_uv_offset_y
            detailNormalScaleNode.outputs[0].default_value =  mat.msfs_detail_normal_scale
        


    # Main material mode, in accordance with MSFS material shaders:
    Material.msfs_material_mode =  bpy.props.EnumProperty(items=(('NONE',"Disabled",""),
                                                                ('msfs_standard', "MSFS Standard",""),
                                                                ('msfs_anisotropic', "MSFS Anisotropic",""),
                                                                ('msfs_sss', "MSFS Subsurface Scattering",""),
                                                                ('msfs_glass', "MSFS Glass",""),
                                                                ('msfs_decal', "MSFS Decal",""),
                                                                ('msfs_clearcoat', "MSFS Clearcoat",""),
                                                                ('msfs_env_occluder', "MSFS Environment Occluder",""),
                                                                ('msfs_fake_terrain', "MSFS Fake Terrain",""),
                                                                ('msfs_fresnel', "MSFS Fresnel Blending",""),
                                                                ('msfs_windshield', "MSFS Windshield",""),
                                                                ('msfs_porthole', "MSFS Porthole",""),
                                                                ('msfs_parallax', "MSFS Parallax",""),
                                                                ('msfs_geo_decal', "MSFS Geo Decal Frosted",""),
                                                                ('msfs_hair', "MSFS Hair",""),
                                                                ('msfs_invisible', "MSFS Invisible",""),), default='NONE',update=switch_msfs_material,)

    # Some flags to control the visibility of all of the paramters in the UI. 
    # Note: they don't control the actualy material parameters, only whether or 
    # not those parameters are being displayed. 
    Material.msfs_show_tint = bpy.props.BoolProperty(name="show_tint",default=False)
    Material.msfs_show_sss_color = bpy.props.BoolProperty(name="show_sss_color",default=False)

    Material.msfs_show_glass_parameters = bpy.props.BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_windshield_options = bpy.props.BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_decal_parameters = bpy.props.BoolProperty(name="show_decal_parameters",default=False)
    Material.msfs_show_fresnel_parameters = bpy.props.BoolProperty(name="show_fresnel_parameters",default=False)
    Material.msfs_show_parallax_parameters = bpy.props.BoolProperty(name="show_parallax_parameters",default=False)
    Material.msfs_show_geo_decal_parameters = bpy.props.BoolProperty(name="show_geo_decal_parameters",default=False)

    Material.msfs_show_albedo = bpy.props.BoolProperty(name="show_albedo",default=False)
    Material.msfs_show_metallic = bpy.props.BoolProperty(name="show_metallic",default=False)
    Material.msfs_show_normal = bpy.props.BoolProperty(name="show_normal",default=False)
    Material.msfs_show_emissive = bpy.props.BoolProperty(name="show_emissive",default=False)
    Material.msfs_show_detail_albedo = bpy.props.BoolProperty(name="show_detail_albedo",default=False)
    Material.msfs_show_detail_metallic = bpy.props.BoolProperty(name="show_detail_metallic",default=False)
    Material.msfs_show_detail_normal = bpy.props.BoolProperty(name="show_detail_normal",default=False)
    Material.msfs_show_blend_mask = bpy.props.BoolProperty(name="show_blend_mask",default=False)
    Material.msfs_show_anisotropic_direction = bpy.props.BoolProperty(name="show_anisotropic_direction",default=False)
    Material.msfs_show_clearcoat = bpy.props.BoolProperty(name="show_clearcoat",default=False)
    Material.msfs_show_behind_glass = bpy.props.BoolProperty(name="show_behind_glass",default=False)
    Material.msfs_show_wiper_mask = bpy.props.BoolProperty(name="show_wiper_mask",default=False)

    Material.msfs_show_blend_mode = bpy.props.BoolProperty(name="show_blend_mode",default=False)

    Material.msfs_show_draworder = bpy.props.BoolProperty(name="show_draworder",default=False)
    Material.msfs_show_no_cast_shadow = bpy.props.BoolProperty(name="show_no_cast_shadow",default=False)
    Material.msfs_show_double_sided = bpy.props.BoolProperty(name="show_double_sided",default=False)
    Material.msfs_show_responsive_aa = bpy.props.BoolProperty(name="show_responsive_aa",default=False)
    Material.msfs_show_day_night_cycle = bpy.props.BoolProperty(name="show_day_night_cycle",default=False)

    Material.msfs_show_collision_material = bpy.props.BoolProperty(name="show_collision_material",default=False)
    Material.msfs_show_road_material = bpy.props.BoolProperty(name="show_road_material",default=False)

    Material.msfs_show_ao_use_uv2 = bpy.props.BoolProperty(name="show_ao_use_uv2",default=False)
    Material.msfs_show_uv_clamp = bpy.props.BoolProperty(name="show_uv_clamp",default=False)

    Material.msfs_show_alpha_cutoff = bpy.props.BoolProperty(name="show_alpha_cutoff",default=False)
    Material.msfs_show_blend_threshold = bpy.props.BoolProperty(name="show_blend_threshold",default=False)
    Material.msfs_show_pearl = bpy.props.BoolProperty(name="show_pearl",default=False)

    # MSFS Material properties
    # The following variables are written into the glTF file when exporting.
    #Color blends:
    Material.msfs_color_albedo_mix = bpy.props.FloatVectorProperty(name="Albedo Color", subtype='COLOR', min=0.0, max=1.0,size=4,default=[1.0,1.0,1.0,1.0], description="The color value set here will be mixed in with the albedo value of the material.",update=match_base_color)
    Material.msfs_color_emissive_mix = bpy.props.FloatVectorProperty(name="Emissive Color", subtype='COLOR', min=0.0, max=1.0, size=4,default=[0.0,0.0,0.0,0.0], description="The color value set here will be mixed in with the emissive value of the material.", update=match_emissive_color)
    # Material.msfs_color_alpha_mix = bpy.props.FloatProperty(name="Alpha multiplier", min=0, max=1, default=1, description="The alpha value set here will be mixed in with the Alpha value of the texture.",update=update_color_alpha_mix)
    # Material.msfs_color_base_mix = bpy.props.FloatProperty(name="Albedo Color Mix", min=0, max=1, default=1, description="Mix factor for the Albedo Color with the Albedo Texture.",update=update_color_base_mix)
    Material.msfs_color_sss = bpy.props.FloatVectorProperty(name="SSS Color", subtype='COLOR',min=0.0, max=1.0,size=4, default=[1.0,1.0,1.0,1.0], description = "Use the color picker to set the color of the subsurface scattering.",update=update_color_sss)
    # Windshield
    Material.msfs_rain_drop_scale = FloatProperty(
        name="Rain Drop Scale",
        min=0.0,
        max=100.0,
        default=1.0
    )
    Material.msfs_wiper_1_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )
    Material.msfs_wiper_2_state = FloatProperty(
        name="Wiper 2 State",
        min=0.0,
        max=1.0,
        default=0.0
    )  # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible
    Material.msfs_wiper_3_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )
    Material.msfs_wiper_4_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )

    #Glass parameters:
    Material.msfs_glass_reflection_mask_factor = bpy.props.FloatProperty(name="Reflection mask factor", min=0.0,max=1.0,default=1.0)
    Material.msfs_glass_deformation_factor = bpy.props.FloatProperty(name = "Deformation factor", min=0.0, max=1.0,default=0.0)

    #Pearl
    

    Material.msfs_use_pearl_effect = BoolProperty(
        name="Use Pearl Effect",
        default=False
    )
    Material.msfs_pearl_shift = FloatProperty(
        name="Color Shift",
        min=-999.0,
        max=999.0,
        default=0.0
    )
    Material.msfs_pearl_range = FloatProperty(
        name="Color Range",
        min=-999.0,
        max=999.0,
        default=0.0
    )
    Material.msfs_pearl_brightness = FloatProperty(
        name="Color Brightness",
        min=-1.0,
        max=1.0,
        default=0.0
    )

    #Decal parameters:
    Material.msfs_decal_blend_factor_color = bpy.props.FloatProperty(name="Color", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_metal = bpy.props.FloatProperty(name="Metal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_normal = bpy.props.FloatProperty(name="Normal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_roughness = bpy.props.FloatProperty(name="Roughness", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_occlusion = bpy.props.FloatProperty(name="Occlusion", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_emissive = bpy.props.FloatProperty(name="Emissive", min=0.0,max=1.0,default=1.0)

    #Fresnel parameters:
    Material.msfs_fresnel_factor = bpy.props.FloatProperty(name="Fresnel factor", min=0.0,max=1.0,default=1.0)
    Material.msfs_fresnel_opacity_bias = bpy.props.FloatProperty(name="Fresnel opacity bias", min=0.0,max=1.0,default=1.0)

    #Parallax parameters:
    Material.msfs_parallax_scale = bpy.props.FloatProperty(name="Scale", min=0.0,max=1.0,default=0.0)
    Material.msfs_parallax_room_size_x = bpy.props.FloatProperty(name="X", min=0.0,default=0.5)
    Material.msfs_parallax_room_size_y = bpy.props.FloatProperty(name="Y", min=0.0,default=0.5)
    Material.msfs_parallax_room_number = bpy.props.FloatProperty(name="Rm number XY", min=0.0,default=1.0)
    Material.msfs_parallax_corridor = bpy.props.BoolProperty(name="Corridor", default=False)

    #Geo Decal Frosted parameters:
    Material.msfs_geo_decal_blend_factor_color = bpy.props.FloatProperty(name="Color", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_metal = bpy.props.FloatProperty(name="Metal", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_normal = bpy.props.FloatProperty(name="Normal", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_roughness = bpy.props.FloatProperty(name="Roughness", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_blast_sys = bpy.props.FloatProperty(name="Blast Sys.", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_melt_sys = bpy.props.FloatProperty(name="Melt Sys", min=0.0,max=1.0,default=1.0)

    #Textures:
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

    #Alpha mode:
    Material.msfs_blend_mode = bpy.props.EnumProperty(name="Blend mode",items=(('OPAQUE',"Opaque","Creates a fully non-transparent material."),
                                                                               ('MASKED',"Masked","This blend mode uses the alpha map to mask off parts of the material, but only if the alpha value exceeds the value set in the alpha cutoff parameter."),
                                                                               ('BLEND',"Blend","This blend mode uses the alpha map to gradually blend in the material. Use this for materials like glass."),
                                                                               ('DITHER',"Dither","Weird blend mode. But works well for hair. No visible effect in Blender."),), 
                                                                               default='OPAQUE',update=switch_msfs_blendmode)
    
    #Render parameters:
    Material.msfs_draw_order = bpy.props.IntProperty(name="Draw order",default = 0, min = 0)
    Material.msfs_no_cast_shadow = bpy.props.BoolProperty(name="No cast shadow",default=False)
    Material.msfs_double_sided = bpy.props.BoolProperty(name="Double sided",default=False,update=update_double_sided)
    Material.msfs_responsive_aa = bpy.props.BoolProperty(name="Responsive AA", default=False,description="")
    Material.msfs_day_night_cycle = bpy.props.BoolProperty(name="Day/Night cycle", default=False)

    #Gameplay parameters:
    Material.msfs_collision_material = bpy.props.BoolProperty(name="Collision material",default=False)
    Material.msfs_road_material = bpy.props.BoolProperty(name="Road material",default=False)

    #UV options:
    
    Material.msfs_uv_offset_u = FloatProperty(
        name="U",
        min=-10.0,
        max=10.0,
        default=0.0
    )
    Material.msfs_uv_offset_v = FloatProperty(
        name="V",
        min=-10.0,
        max=10.0,
        default=0.0
    )
    Material.msfs_uv_tiling_u = FloatProperty(
        name="U",
        min=-10.0,
        max=10.0,
        default=1.0
    )
    Material.msfs_uv_tiling_v = FloatProperty(
        name="V",
        min=-10.0,
        max=10.0,
        default=1.0
    )
    Material.msfs_uv_rotation = FloatProperty(
        name="UV Rotation",
        min=-360.0,
        max=360.0,
        default=0.0
    )
    Material.msfs_ao_use_uv2 = bpy.props.BoolProperty(name="AO use UV2",default=False)
    Material.msfs_uv_clamp_x = bpy.props.BoolProperty(name="X",default=False)
    Material.msfs_uv_clamp_y = bpy.props.BoolProperty(name="Y",default=False)
    Material.msfs_uv_clamp_z = bpy.props.BoolProperty(name="Z",default=False)

    #Material parameters
    Material.msfs_roughness_scale = bpy.props.FloatProperty(name="Roughness scale",min=0,max=1,default=1, update = match_roughness_scale)
    Material.msfs_metallic_scale = bpy.props.FloatProperty(name="Metallic scale",min=0,max=1,default=1, update = match_metallic_scale)
    Material.msfs_emissive_scale = bpy.props.FloatProperty(name="Emissive scale",min=0,max=1,default=1, update = match_emissive_scale)
    Material.msfs_normal_scale = bpy.props.FloatProperty(name="Normal scale",min=0,default=1,update=match_normal_scale)
    Material.msfs_alpha_cutoff = bpy.props.FloatProperty(name="Alpha cutoff",min=0,max=1,default=0.1,update=match_alpha_cutoff)
    Material.msfs_detail_uv_scale = bpy.props.FloatProperty(name="Detail UV scale",min=0,default=1,update=match_detail_uv)
    Material.msfs_detail_uv_offset_x = bpy.props.FloatProperty(name="X",min=-1,max=1,default=0,update=match_detail_uv)
    Material.msfs_detail_uv_offset_y = bpy.props.FloatProperty(name="Y",min=-1,max=1,default=0,update=match_detail_uv)
    Material.msfs_detail_normal_scale = bpy.props.FloatProperty(name="Detail normal scale",min=0,max=1,default=1, update = match_detail_uv)
    Material.msfs_blend_threshold = bpy.props.FloatProperty(name="Blend threshold",min=0,max=1,default=0.1)


