# glTF-Blender-IO-MSFS
# Copyright (C) 2022 The glTF-Blender-IO-MSFS authors

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
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw_prop(self, layout, mat, prop, enabled=True, visible=True, text=""):
        if visible:
            column = layout.column()
            if text:
                column.prop(mat, prop, text="")
            else:
                column.prop(mat, prop)

            column.enabled = enabled

    def draw_texture_prop(self, layout, mat, prop, enabled=True, visible=True, text=""):
        if visible:
            column = layout.column()
            if text:
                column.label(text=text)

            column.template_ID(mat, prop, new="image.new", open="image.open")
            column.enabled = enabled

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True

        mat = context.active_object.active_material

        if mat:
            self.draw_prop(layout, mat, "msfs_material_type")

            if mat.msfs_material_type != "NONE":
                self.draw_prop(layout, mat, "msfs_base_color_factor")
                self.draw_prop(
                    layout,
                    mat,
                    "msfs_emissive_factor",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_invisible", "msfs_environment_occluder"]
                    ),
                )

                # Alpha mode
                box = layout.box()
                box.label(text="Alpha Mode")
                box.enabled = mat.msfs_material_type in [
                    "msfs_standard",
                    "msfs_anisotropic",
                    "msfs_hair",
                    "msfs_sss",
                    "msfs_fresnel_fade",
                    "msfs_clearcoat",
                ]
                self.draw_prop(box, mat, "msfs_alpha_mode")

                # Render params
                box = layout.box()
                box.label(text="Render Parameters")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_draw_order_offset")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_no_cast_shadow",
                    enabled=(mat.msfs_material_type != "msfs_ghost"),
                )
                self.draw_prop(box, mat, "msfs_double_sided")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_day_night_cycle",
                    enabled=(mat.msfs_material_type == "msfs_standard"),
                )
                self.draw_prop(box, mat, "msfs_disable_motion_blur")

                # Gameplay params
                box = layout.box()
                box.label(text="Gameplay Parameters")
                box.enabled = mat.msfs_material_type != "msfs_environment_occluder"
                self.draw_prop(box, mat, "msfs_collision_material")
                self.draw_prop(box, mat, "msfs_road_collision_material")

                # UV options
                box = layout.box()
                box.label(text="UV Options")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_uv_offset_u")
                self.draw_prop(box, mat, "msfs_uv_offset_v")
                self.draw_prop(box, mat, "msfs_uv_tiling_u")
                self.draw_prop(box, mat, "msfs_uv_tiling_v")
                self.draw_prop(box, mat, "msfs_uv_rotation")

                # UV clamp
                box = layout.box()
                box.label(text="UV Clamp")
                box.enabled = mat.msfs_material_type != "msfs_environment_occluder"
                self.draw_prop(box, mat, "msfs_clamp_uv_x")
                self.draw_prop(box, mat, "msfs_clamp_uv_y")

                # General params
                box = layout.box()
                box.label(text="General Parameters")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_metallic_factor")
                self.draw_prop(box, mat, "msfs_roughness_factor")
                self.draw_prop(box, mat, "msfs_normal_scale")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_alpha_cutoff",
                    enabled=(
                        mat.msfs_material_type
                        in [
                            "msfs_standard",
                            "msfs_anisotropic",
                            "msfs_hair",
                            "msfs_sss",
                            "msfs_fresnel_fade",
                            "msfs_clearcoat",
                        ]
                        and mat.msfs_alpha_mode == "MASK"
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_scale",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_offset_u",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_offset_v",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_normal_scale",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_blend_threshold",
                    enabled=(
                        mat.msfs_material_type not in ["msfs_fresnel_fade", "msfs_sss"]
                        and mat.msfs_blend_mask_texture is not None
                    ),
                )
                # TODO: emissive multiplier?

                # Decal params
                if mat.msfs_material_type in [
                    "msfs_geo_decal",
                    "msfs_geo_decal_frosted",
                ]:
                    box = layout.box()
                    box.label(text="Decal Blend Factors")
                    box.enabled = mat.msfs_material_type in [
                        "msfs_geo_decal",
                        "msfs_geo_decal_frosted",
                    ]
                    self.draw_prop(box, mat, "msfs_base_color_blend_factor")
                    self.draw_prop(box, mat, "msfs_roughness_blend_factor")
                    self.draw_prop(box, mat, "msfs_metallic_blend_factor")
                    self.draw_prop(
                        box,
                        mat,
                        "msfs_occlusion_blend_factor",
                        text="Blast Sys Blend Factor"
                        if mat.msfs_material_type == "msfs_geo_decal_frosted"
                        else "",
                    )
                    self.draw_prop(box, mat, "msfs_normal_blend_factor")
                    self.draw_prop(
                        box,
                        mat,
                        "msfs_emissive_blend_factor",
                        text="Melt Sys Blend Factor"
                        if mat.msfs_material_type == "msfs_geo_decal_frosted"
                        else "",
                    )

                # SSS params - disabled for now
                # if mat.msfs_material_type in ["msfs_sss", "msfs_hair"]:
                #     box = layout.box()
                #     box.label(text="SSS Parameters")
                #     self.draw_prop(
                #         box, mat, "msfs_sss_color", enabled=False
                #     )

                # Glass params
                if mat.msfs_material_type == "msfs_glass":
                    box = layout.box()
                    box.label(text="Glass Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_glass"
                    self.draw_prop(box, mat, "msfs_glass_reflection_mask_factor")
                    self.draw_prop(box, mat, "msfs_glass_deformation_factor")

                # Parallax params
                if mat.msfs_material_type == "msfs_parallax":
                    box = layout.box()
                    box.label(text="Parallax Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_parallax"
                    self.draw_prop(box, mat, "msfs_parallax_scale")
                    self.draw_prop(box, mat, "msfs_parallax_room_size_x")
                    self.draw_prop(box, mat, "msfs_parallax_room_size_y")
                    self.draw_prop(box, mat, "msfs_parallax_room_number_xy")
                    self.draw_prop(box, mat, "msfs_parallax_corridor")

                # Fresnel params
                if mat.msfs_material_type == "msfs_fresnel_fade":
                    box = layout.box()
                    box.label(text="Fresnel Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_fresnel_fade"
                    self.draw_prop(box, mat, "msfs_fresnel_factor")
                    self.draw_prop(box, mat, "msfs_fresnel_opacity_offset")

                # Ghost params
                if mat.msfs_material_type == "msfs_ghost":
                    box = layout.box()
                    box.label(text="Ghost Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_ghost"
                    self.draw_prop(box, mat, "msfs_ghost_bias")
                    self.draw_prop(box, mat, "msfs_ghost_power")
                    self.draw_prop(box, mat, "msfs_ghost_scale")

                # Windshield params
                if mat.msfs_material_type == "msfs_windshield":
                    box = layout.box()
                    box.label(text="Windshield Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_windshield"
                    self.draw_prop(box, mat, "msfs_rain_drop_scale")
                    self.draw_prop(box, mat, "msfs_wiper_1_state")
                    self.draw_prop(box, mat, "msfs_wiper_2_state")
                    self.draw_prop(box, mat, "msfs_wiper_3_state", visible=False)
                    self.draw_prop(box, mat, "msfs_wiper_4_state", visible=False)

                # Pearl params
                if mat.msfs_material_type == "msfs_standard":
                    box = layout.box()
                    box.label(text="Pearl Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_standard"
                    self.draw_prop(box, mat, "msfs_use_pearl")
                    self.draw_prop(box, mat, "msfs_pearl_shift")
                    self.draw_prop(box, mat, "msfs_pearl_range")
                    self.draw_prop(box, mat, "msfs_pearl_brightness")

                # Overwrites for different material types. TODO: move to update material type
                # if mat.msfs_material_type == "msfs_windshield":
                #     mat.msfs_metallic_factor = 0.0
                # elif mat.msfs_material_type == "msfs_glass":
                #     mat.msfs_metallic_factor = 0.0
                # elif mat.msfs_material_type == "msfs_parallax":
                #     mat.msfs_alpha_mode = "MASK"
                # elif mat.msfs_material_type == "msfs_ghost":
                #     mat.msfs_no_cast_shadow = True
                #     mat.msfs_alpha_mode = "BLEND"

                if mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]:
                    box = layout.box()
                    box.label(text="Textures")

                    # In the 3DS Max exporter, the textures have different display names depending on material type and other properties used. We replicate that process here
                    base_color_tex_name = "Base Color"
                    occlusion_metallic_roughness_texture_name = (
                        "Occlusion (R), Roughness (G), Metallic (B)"
                    )
                    normal_texture_name = "Normal"
                    blend_mask_texture_name = "Blend Mask"
                    dirt_texture_name = "Clearcoat amount (R), Clearcoat rough (G)"
                    wetness_ao_texture_name = "Wetness AO"
                    emissive_texture_name = "Emissive"
                    detail_color_texture_name = "Secondary Color (RGB), Alpha (A)"
                    detail_occlusion_metallic_roughness_texture_name = (
                        "Secondary Occ (R), Rough (G), Metal (B)"
                    )
                    detail_normal_texture_name = "Secondary Normal"

                    if mat.msfs_blend_mask_texture is None:
                        detail_color_texture_name = "Detail Color (RGB), Alpha (A)"
                        detail_normal_texture_name = "Detail Normal"
                        detail_occlusion_metallic_roughness_texture_name = (
                            "Detail Occlusion (R), Roughness (G), Metallic (B)"
                        )

                    if mat.msfs_material_type == "msfs_windshield":
                        emissive_texture_name = "Secondary Details(A)"
                        wetness_ao_texture_name = "Wiper Mask (RG)"
                        detail_color_texture_name = (
                            "Details Scratch(R), Icing Mask(G), Fingerprints(B)"
                        )
                        detail_normal_texture_name = "Icing Normal (use DetailMap UV)"
                    elif mat.msfs_material_type == "msfs_geo_decal_frosted":
                        detail_occlusion_metallic_roughness_texture_name = (
                            "Melt pattern (R), Roughness (G), Metallic (B)"
                        )
                    elif mat.msfs_material_type == "msfs_parallax":
                        base_color_tex_name = "Front Glass Color"
                        normal_texture_name = "Front Glass Normal"
                        detail_color_texture_name = (
                            "Behind Glass Color (RGB), Alpha (A)"
                        )
                        emissive_texture_name = (
                            "Emissive Ins Window (RGB), offset Time (A)"
                        )
                    elif mat.msfs_material_type in ["msfs_anisotropic", "msfs_hair"]:
                        wetness_ao_texture_name = "Anisotropic direction (RG)"

                    self.draw_texture_prop(
                        box, mat, "msfs_base_color_texture", text=base_color_tex_name
                    )
                    self.draw_texture_prop(
                        box,
                        mat,
                        "msfs_occlusion_metallic_roughness_texture",
                        text=occlusion_metallic_roughness_texture_name,
                    )
                    self.draw_texture_prop(
                        box, mat, "msfs_normal_texture", text=normal_texture_name
                    )
                    self.draw_texture_prop(
                        box, mat, "msfs_emissive_texture", text=emissive_texture_name
                    )

                    if mat.msfs_material_type not in [
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_color_texture",
                            text=detail_color_texture_name,
                        )
                    if mat.msfs_material_type not in [
                        "msfs_parallax",
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_normal_texture",
                            text=detail_normal_texture_name,
                        )
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_occlusion_metallic_roughness_texture",
                            text=detail_occlusion_metallic_roughness_texture_name,
                        )
                    if mat.msfs_material_type not in [
                        "msfs_geo_decal_frosted",
                        "msfs_parallax",
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                        "msfs_ghost"
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_blend_mask_texture",
                            text=blend_mask_texture_name,
                        )
                    if mat.msfs_material_type in [
                        "msfs_winshield",
                        "msfs_anisotropic",
                        "msfs_hair",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_wetness_ao_texture",
                            text=wetness_ao_texture_name,
                        )
                    if mat.msfs_material_type == "msfs_clearcoat":
                        self.draw_texture_prop(
                            box, mat, "msfs_dirt_texture", text=dirt_texture_name
                        )
