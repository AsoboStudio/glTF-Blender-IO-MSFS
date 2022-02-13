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

    def draw_prop(self, mat, ui_parent, prop, text=None, icon=None): 
        # Due to how values are enabled to have a keyframe, we have to toggle the use_property_decorate to True and then change it back once we're done
        if prop.animated and mat.msfs_material_mode.value == prop.animated_on_type:
            ui_parent.use_property_decorate = True

        if icon:
            ui_parent.prop(prop, "value", text=text, icon=icon)
        else:
            ui_parent.prop(prop, "value", text=text)

        ui_parent.use_property_decorate = False

    def draw(self, context):
        mat = context.active_object.active_material

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        if mat:
            box = layout.box()
            box.label(text="Material Mode", icon='MATERIAL')

            self.draw_prop(mat, box, mat.msfs_material_mode, text="Select")

            if mat.msfs_show_tint:
                box = layout.box()
                box.label(text="Color multipliers", icon='COLOR')

                self.draw_prop(mat, box, mat.msfs_color_albedo_mix)
                self.draw_prop(mat, box, mat.msfs_color_emissive_mix)

                if mat.msfs_show_sss_color:
                    self.draw_prop(mat, box, mat.msfs_color_sss)

            if mat.msfs_show_glass_parameters:
                box = layout.box()
                box.label(text="Glass parameters",icon='SHADING_RENDERED')

                self.draw_prop(mat, box, mat.msfs_glass_reflection_mask_factor)
                self.draw_prop(mat, box, mat.msfs_glass_deformation_factor)

            if mat.msfs_show_windshield_options:
                box = layout.box()
                box.label(text="Windshield Options", icon="MATFLUID")

                self.draw_prop(mat, box, mat.msfs_rain_drop_scale)
                self.draw_prop(mat, box, mat.msfs_wiper_1_state)
                self.draw_prop(mat, box, mat.msfs_wiper_2_state)
                self.draw_prop(mat, box, mat.msfs_wiper_3_state)
                self.draw_prop(mat, box, mat.msfs_wiper_4_state)

            if mat.msfs_show_decal_parameters:
                box = layout.box()
                box.label(text="Decal per component blend factors", icon='OUTLINER_OB_POINTCLOUD')

                row = box.row()
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_color)
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_roughness)

                row = box.row()
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_metal)
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_occlusion)

                row = box.row()
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_normal)
                self.draw_prop(mat, row, mat.msfs_decal_blend_factor_emissive)

            if mat.msfs_show_fresnel_parameters:
                box = layout.box()
                box.label(text="Fresnel parameters", icon='COLORSET_13_VEC')

                self.draw_prop(mat, box, mat.msfs_fresnel_factor)
                self.draw_prop(mat, box, mat.msfs_fresnel_opacity_bias)

            if mat.msfs_show_parallax_parameters:
                box = layout.box()
                box.label(text="Parallax parameters",icon='MATERIAL')

                self.draw_prop(mat, box, mat.msfs_parallax_scale)

                subbox = box.box()
                subbox.label(text="Room size")
                self.draw_prop(mat, subbox, mat.msfs_parallax_room_size_x)
                self.draw_prop(mat, subbox, mat.msfs_parallax_room_size_y)

                self.draw_prop(mat, box, mat.msfs_parallax_room_number)
                self.draw_prop(mat, box, mat.msfs_parallax_corridor)

            if mat.msfs_show_geo_decal_parameters:
                box = layout.box()
                box.label(text="Geo Decal Frosted blend factors", icon='FREEZE')
                row = box.row()
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_color)
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_roughness)

                row = box.row()
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_metal)
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_blast_sys)

                row = box.row()
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_normal)
                self.draw_prop(mat, row, mat.msfs_geo_decal_blend_factor_melt_sys)

            if (mat.msfs_show_blend_mode or mat.msfs_show_draworder or mat.msfs_show_no_cast_shadow or mat.msfs_show_double_sided or 
                mat.msfs_show_responsive_aa or mat.msfs_show_day_night_cycle):
                box = layout.box()
                box.label(text="Render Parameters",icon='NODE_MATERIAL')

                if mat.msfs_show_blend_mode:
                    self.draw_prop(mat, box, mat.msfs_blend_mode, text="Alpha mode")
                if mat.msfs_show_draworder:
                    self.draw_prop(mat, box, mat.msfs_draw_order)
                if mat.msfs_show_no_cast_shadow:
                    self.draw_prop(mat, box, mat.msfs_no_cast_shadow)
                if mat.msfs_show_double_sided:
                    self.draw_prop(mat, box, mat.msfs_double_sided)
                if mat.msfs_show_responsive_aa:
                    self.draw_prop(mat, box, mat.msfs_responsive_aa)
                if mat.msfs_show_day_night_cycle:
                    self.draw_prop(mat, box, mat.msfs_day_night_cycle)

            if (mat.msfs_show_metallic or mat.msfs_show_normal or mat.msfs_show_alpha_cutoff or mat.msfs_show_detail_albedo or
                mat.msfs_show_detail_normal or mat.msfs_show_blend_threshold):
                box = layout.box()
                box.label(text="Material properties", icon='MATERIAL')

                if mat.msfs_show_metallic:
                    self.draw_prop(mat, box, mat.msfs_roughness_scale)
                    self.draw_prop(mat, box, mat.msfs_metallic_scale)
                if mat.msfs_show_normal:
                    self.draw_prop(mat, box, mat.msfs_normal_scale)
                if mat.msfs_show_alpha_cutoff:
                    self.draw_prop(mat, box, mat.msfs_alpha_cutoff)
                if mat.msfs_show_detail_albedo:
                    self.draw_prop(mat, box, mat.msfs_detail_uv_scale)

                    row = box.row()
                    row.label(text="Detail UV offset")
                    column = row.column()
                    self.draw_prop(mat, column, mat.msfs_detail_uv_offset_x)
                    self.draw_prop(mat, column, mat.msfs_detail_uv_offset_y)
                if mat.msfs_show_detail_normal:
                    self.draw_prop(mat, box, mat.msfs_detail_normal_scale)
                if mat.msfs_show_blend_threshold:
                    self.draw_prop(mat, box, mat.msfs_blend_threshold)
                if mat.msfs_show_emissive:
                    self.draw_prop(mat, box, mat.msfs_emissive_scale)

            if mat.msfs_show_pearl:
                box = layout.box()
                box.label(text="Pearlescent Options", icon="NODE_MATERIAL")

                self.draw_prop(mat, box, mat.msfs_use_pearl_effect)
                self.draw_prop(mat, box, mat.msfs_pearl_shift)
                self.draw_prop(mat, box, mat.msfs_pearl_range)
                self.draw_prop(mat, box, mat.msfs_pearl_brightness)

            if (mat.msfs_show_collision_material or mat.msfs_show_road_material):
                box= layout.box()
                box.label(text="Gameplay parameters", icon='GHOST_ENABLED')
                if mat.msfs_show_collision_material:
                    self.draw_prop(mat, box, mat.msfs_collision_material)
                if mat.msfs_show_road_material:
                    self.draw_prop(mat, box, mat.msfs_road_material)

            if (mat.msfs_show_ao_use_uv2 or mat.msfs_show_uv_clamp):
                box = layout.box()
                box.label(text="UV options", icon='UV')

                row = box.row()
                row.label(text="UV Offset")
                column = row.column()
                self.draw_prop(mat, column, mat.msfs_uv_offset_u, text="U")
                self.draw_prop(mat, column, mat.msfs_uv_offset_v, text="V")

                row = box.row()
                row.label(text="UV Tiling")
                column = row.column()
                self.draw_prop(mat, column, mat.msfs_uv_tiling_u)
                self.draw_prop(mat, column, mat.msfs_uv_tiling_v)

                self.draw_prop(mat, box, mat.msfs_uv_rotation)

                if mat.msfs_show_uv_clamp:
                    row = box.row()
                    row.label(text="UV Clamp")
                    column = row.column()
                    self.draw_prop(mat, column, mat.msfs_uv_clamp_x)
                    self.draw_prop(mat, column, mat.msfs_uv_clamp_y)

            if (mat.msfs_show_albedo or mat.msfs_show_metallic or mat.msfs_show_normal or mat.msfs_show_emissive or mat.msfs_show_detail_albedo or 
                mat.msfs_show_detail_metallic or mat.msfs_show_detail_normal or mat.msfs_show_blend_mask or mat.msfs_show_anisotropic_direction or
                mat.msfs_show_clearcoat or mat.msfs_show_behind_glass or mat.msfs_show_wiper_mask):

                box = layout.box()
                box.label(text="Texture maps",icon='TEXTURE')
                if mat.msfs_show_albedo:
                    box.label(text = "Albedo")
                    box.template_ID(mat, "msfs_albedo_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_metallic:
                    box.label(text = "Metallic")
                    box.label(text="(Occlusion(R),Roughness(G),Metallic(B))")
                    box.template_ID(mat, "msfs_metallic_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_normal:
                    box.label(text = "Normal")
                    box.template_ID(mat, "msfs_normal_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_emissive:
                    box.label(text = "Emissive")
                    box.template_ID(mat, "msfs_emissive_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_albedo:
                    box.label(text = "Detail Albedo")
                    if mat.msfs_material_mode == 'windshield':
                        box.label(text="(Scratches (R), Fingerprints(B))")
                    box.template_ID(mat, "msfs_detail_albedo_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_metallic:
                    box.label(text = "Detail Metallic")
                    if mat.msfs_material_mode == 'geo_decal':
                        box.label(text="(Melt Pattern(R),Roughness(G),Metallic(B))")
                    else:
                        box.label(text="(Occlusion(R),Roughness(G),Metallic(B))")
                    box.template_ID(mat, "msfs_detail_metallic_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_detail_normal:
                    if mat.msfs_material_mode == 'windshield':
                        box.label(text = "Icing Normal")
                    else:
                        box.label(text = "Detail Normal")
                    box.template_ID(mat, "msfs_detail_normal_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_blend_mask:
                    box.label(text = "Blend Mask")
                    box.template_ID(mat, "msfs_blend_mask_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_anisotropic_direction:
                    box.label(text=  "Anisotropic direction (RG)")
                    box.template_ID(mat, "msfs_anisotropic_direction_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_clearcoat:
                    box.label(text=  "Clearcoat amount (R), Clearcoat rough(G)")
                    box.template_ID(mat, "msfs_clearcoat_texture", new = "image.new", open = "image.open")
                if mat.msfs_show_behind_glass:
                    box.label(text = "Behind glass Albedo")
                    box.template_ID(mat, "msfs_behind_glass_texture", new="image.new", open = "image.open")
                if mat.msfs_show_wiper_mask:
                    box.label(text = "Wiper Mask (RG)")
                    box.template_ID(mat, "msfs_wiper_mask_texture", new="image.new", open = "image.open")
