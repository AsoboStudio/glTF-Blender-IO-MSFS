# Copyright 2021-2022 The glTF-Blender-IO-MSFS authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bpy
from bpy.types import Material
#from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty, EnumProperty, FloatVectorProperty
#import os
from .msfs_properties import *


class MSFS_PT_material(bpy.types.Panel):
    bl_label = "MSFS Material Params"
    bl_idname = "MSFSMATERIAL_PT_props"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw(self, context):
        mat = context.active_object.active_material

        layout = self.layout
        
        if mat:
            box=layout.box()
            box.label(text="Material Mode",icon='MATERIAL')
            
            box.prop(mat, 'msfs_material_mode', text="Select")

            if mat.msfs_show_tint == True:
                subbox=box.box()
                subbox.label(text="Color multipliers",icon='COLOR')
                row = subbox.row()
                row.prop(mat, 'msfs_color_albedo_mix')
                row = subbox.row()
                row.prop(mat, 'msfs_color_emissive_mix')
                subbox.prop(mat, 'msfs_color_alpha_mix')
                subbox.prop(mat, 'msfs_color_base_mix')
                if mat.msfs_show_sss_color == True:
                    subbox.prop(mat, 'msfs_color_sss')

            if mat.msfs_show_glass_parameters == True:
                box = layout.box()
                box.label(text="Glass parameters:",icon='SHADING_RENDERED')
                box.prop(mat, 'msfs_glass_reflection_mask_factor')
                box.prop(mat, 'msfs_glass_deformation_factor')

            if mat.msfs_show_windshield_options == True:
                box = layout.box()
                box.label(text="Windshield Options", icon="MATFLUID")
                box.prop(mat, "msfs_rain_drop_scale")
                box.prop(mat, "msfs_wiper_1_state")
                box.prop(mat, "msfs_wiper_2_state")
                box.prop(mat, "msfs_wiper_3_state")
                box.prop(mat, "msfs_wiper_4_state")

            if mat.msfs_show_decal_parameters == True:
                box = layout.box()
                box.label(text="Decal per component blend factors:", icon='OUTLINER_OB_POINTCLOUD')
                row = box.row()
                row.prop(mat, 'msfs_decal_blend_factor_color')
                row.prop(mat, 'msfs_decal_blend_factor_roughness')
                row = box.row()
                row.prop(mat, 'msfs_decal_blend_factor_metal')
                row.prop(mat, 'msfs_decal_blend_factor_occlusion')
                row = box.row()
                row.prop(mat, 'msfs_decal_blend_factor_normal')
                row.prop(mat, 'msfs_decal_blend_factor_emissive')

            if mat.msfs_show_fresnel_parameters == True:
                box = layout.box()
                box.label(text="Fresnel parameters", icon='COLORSET_13_VEC')
                box.prop(mat, 'msfs_fresnel_factor')
                box.prop(mat, 'msfs_fresnel_opacity_bias')

            if mat.msfs_show_parallax_parameters == True:
                box = layout.box()
                box.label(text="Parallax parameters:",icon='MATERIAL')
                box.prop(mat,'msfs_parallax_scale')
                subbox = box.box()
                subbox.label(text="Room size")
                subbox.prop(mat,'msfs_parallax_room_size_x')
                subbox.prop(mat,'msfs_parallax_room_size_y')
                box.prop(mat,'msfs_parallax_room_number')
                box.prop(mat,'msfs_parallax_corridor')

            if mat.msfs_show_geo_decal_parameters == True:
                box = layout.box()
                box.label(text="Geo Decal Frosted blend factors:", icon='FREEZE')
                row = box.row()
                row.prop(mat, 'msfs_geo_decal_blend_factor_color')
                row.prop(mat, 'msfs_geo_decal_blend_factor_roughness')
                row = box.row()
                row.prop(mat, 'msfs_geo_decal_blend_factor_metal')
                row.prop(mat, 'msfs_geo_decal_blend_factor_blast_sys')
                row = box.row()
                row.prop(mat, 'msfs_geo_decal_blend_factor_normal')
                row.prop(mat, 'msfs_geo_decal_blend_factor_melt_sys')

            

            if (mat.msfs_show_blend_mode == True or mat.msfs_show_draworder == True or mat.msfs_show_no_cast_shadow == True or mat.msfs_show_double_sided == True or 
                mat.msfs_show_responsive_aa == True or mat.msfs_show_day_night_cycle):

                box = layout.box()
                box.label(text="Render Parameters",icon='NODE_MATERIAL')
                if mat.msfs_show_blend_mode == True:
                    box.prop(mat, 'msfs_blend_mode', text="Alpha mode:")
                if mat.msfs_show_draworder == True:
                    box.prop(mat, 'msfs_draw_order')
                if mat.msfs_show_no_cast_shadow == True:
                    box.prop(mat, 'msfs_no_cast_shadow')
                if mat.msfs_show_double_sided == True:
                    box.prop(mat, 'msfs_double_sided')
                if mat.msfs_show_responsive_aa == True:
                    box.prop(mat, 'msfs_responsive_aa')
                if mat.msfs_show_day_night_cycle == True:
                    box.prop(mat, 'msfs_day_night_cycle')

            if (mat.msfs_show_metallic == True or mat.msfs_show_normal == True or mat.msfs_show_alpha_cutoff == True or mat.msfs_show_detail_albedo == True or
                mat.msfs_show_detail_normal == True or mat.msfs_show_blend_threshold == True):

                box = layout.box()
                box.label(text="Material properties", icon='MATERIAL')
                if mat.msfs_show_metallic == True:
                    box.prop(mat, 'msfs_roughness_scale')
                    box.prop(mat, 'msfs_metallic_scale')
                if mat.msfs_show_normal == True:
                    box.prop(mat, 'msfs_normal_scale')
                if mat.msfs_show_alpha_cutoff == True:
                    box.prop(mat, 'msfs_alpha_cutoff')
                if mat.msfs_show_detail_albedo == True:
                    box.prop(mat, 'msfs_detail_uv_scale')
                    subbox = box.row()
                    subbox.label(text="Detail UV offset")
                    row = subbox.row()
                    row.prop(mat, 'msfs_detail_uv_offset_x')
                    row.prop(mat, 'msfs_detail_uv_offset_y')
                if mat.msfs_show_detail_normal == True:
                    box.prop(mat, 'msfs_detail_normal_scale')
                if mat.msfs_show_blend_threshold == True:
                    box.prop(mat, 'msfs_blend_threshold')

            if mat.msfs_show_pearl == True:
                box = layout.box()
                box.label(text="Pearlescent Options", icon="NODE_MATERIAL")
                box.prop(mat, "msfs_use_pearl_effect")
                box.prop(mat, "msfs_pearl_shift")
                box.prop(mat, "msfs_pearl_range")
                box.prop(mat, "msfs_pearl_brightness")

            if (mat.msfs_show_collision_material == True or mat.msfs_show_road_material == True):
                box= layout.box()
                box.label(text="Gameplay parameters", icon='GHOST_ENABLED')
                if mat.msfs_show_collision_material == True:
                    box.prop(mat, 'msfs_collision_material')
                if mat.msfs_show_road_material == True:
                    box.prop(mat, 'msfs_road_material')

            if (mat.msfs_show_ao_use_uv2 == True or mat.msfs_show_uv_clamp == True):
                box = layout.box()
                box.label(text="UV options", icon='UV')
                #if mat.msfs_show_ao_use_uv2 == True:   - removed by Asobo
                #    box.prop(mat, 'msfs_ao_use_uv2')
                subbox = box.box()
                row=subbox.row()
                row.label(text="UV offset")
                row.prop(mat,'msfs_uv_offset_u')
                row.prop(mat,'msfs_uv_offset_v')
                subbox = box.box()
                row=subbox.row()
                row.label(text="UV tiling")
                row.prop(mat,'msfs_uv_tiling_u')
                row.prop(mat,'msfs_uv_tiling_v')
                box.prop(mat, 'msfs_uv_rotation')
                if mat.msfs_show_uv_clamp == True:
                    subbox = box.box()
                    row=subbox.row()
                    row.label(text="UV clamp")
                    row.prop(mat,'msfs_uv_clamp_x')
                    row.prop(mat,'msfs_uv_clamp_y')
                    #row.prop(mat,'msfs_uv_clamp_z')    - removed by Asobo, probably because it never made sense in the first place.

            if (mat.msfs_show_albedo == True or mat.msfs_show_metallic == True or mat.msfs_show_normal == True or mat.msfs_show_emissive == True or mat.msfs_show_detail_albedo == True or 
                mat.msfs_show_detail_metallic == True or mat.msfs_show_detail_normal == True or mat.msfs_show_blend_mask == True or mat.msfs_show_anisotropic_direction == True or
                mat.msfs_show_clearcoat == True or mat.msfs_show_behind_glass == True or mat.msfs_show_wiper_mask == True):

                box = layout.box()
                box.label(text="Texture maps",icon='TEXTURE')
                if mat.msfs_show_albedo == True:
                    box.label(text = "Albedo:")
                    box.template_ID(mat, "msfs_albedo_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_metallic == True:
                    box.label(text = "Metallic:")
                    box.label(text="(Occlusion(R),Roughness(G),Metallic(B))")
                    box.template_ID(mat, "msfs_metallic_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_normal == True:
                    box.label(text = "Normal:")
                    box.template_ID(mat, "msfs_normal_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_emissive == True:
                    box.label(text = "Emissive:")
                    box.template_ID(mat, "msfs_emissive_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_albedo == True:
                    box.label(text = "Detail Albedo:")
                    if mat.msfs_material_mode == 'windshield':
                        box.label(text="(Scratches (R), Fingerprints(B))")
                    box.template_ID(mat, "msfs_detail_albedo_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_metallic == True:
                    box.label(text = "Detail Metallic:")
                    if mat.msfs_material_mode == 'geo_decal':
                        box.label(text="(Melt Pattern(R),Roughness(G),Metallic(B))")
                    else:
                        box.label(text="(Occlusion(R),Roughness(G),Metallic(B))")
                    box.template_ID(mat, "msfs_detail_metallic_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_normal == True:
                    if mat.msfs_material_mode == 'windshield':
                        box.label(text = "Icing Normal:")
                    else:
                        box.label(text = "Detail Normal:")
                    box.template_ID(mat, "msfs_detail_normal_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_blend_mask == True:
                    box.label(text = "Blend Mask:")
                    box.template_ID(mat, "msfs_blend_mask_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_anisotropic_direction == True:
                    box.label(text=  "Anisotropic direction (RG):")
                    box.template_ID(mat, "msfs_anisotropic_direction_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_clearcoat == True:
                    box.label(text=  "Clearcoat amount (R), Clearcoat rough(G):")
                    box.template_ID(mat, "msfs_clearcoat_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_behind_glass == True:
                    box.label(text = "Behind glass Albedo:")
                    box.template_ID(mat, "msfs_behind_glass_texture", new="image.new", open = "image.open")
                if mat.msfs_show_wiper_mask == True:
                    box.label(text = "Wiper Mask (RG):")
                    box.template_ID(mat, "msfs_wiper_mask_texture", new="image.new", open = "image.open")



