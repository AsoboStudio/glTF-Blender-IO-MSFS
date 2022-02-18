# glTF-Blender-IO-MSFS
# Copyright (C) 2021-2022 The glTF-Blender-IO-MSFS authors

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

import os
import bpy

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage
from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import gather_texture_info


class MSFSMaterial:
    bl_options = {"UNDO"}

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def export_image(blender_material, blender_image, export_settings):
        nodes = blender_material.node_tree.nodes
        links = blender_material.node_tree.links

        # Create a fake texture node temporarily (unfortunately this is the only solid way of doing this)
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = blender_image

        # Create shader to plug texture into
        shader_node = nodes.new("ShaderNodeBsdfDiffuse")
        link = links.new(shader_node.inputs[0], texture_node.outputs[0])

        # Gather texture info
        texture_info = gather_texture_info(shader_node.inputs[0], (shader_node.inputs[0],), export_settings)

        # Delete temp nodes
        links.remove(link)
        nodes.remove(shader_node)
        nodes.remove(texture_node)

        return texture_info

    @staticmethod
    def export(gltf2_material, blender_material, export_settings):
        # Set material type and related properties
        # Anisotropic
        if blender_material.msfs_material_mode.value == "msfs_anisotropic":
            gltf2_material.extensions["ASOBO_material_anisotropic"] = Extension(
                name="ASOBO_material_anisotropic",
                extension={
                    "enabled": True
                },
                required=False
            )

        # SSS, Hair
        elif blender_material.msfs_material_mode.value in ["msfs_sss", "msfs_hair"]:
            gltf2_material.extensions["ASOBO_material_SSS"] = Extension(
                name="ASOBO_material_SSS",
                extension={
                    "SSSColor": list(blender_material.msfs_color_sss.value)
                },
                required=False
            )

        # Hair
        elif blender_material.msfs_material_mode.value == "msfs_glass":
            gltf2_material.extensions["ASOBO_material_glass"] = Extension(
                name="ASOBO_material_glass",
                extension={
                    "glassReflectionMaskFactor": blender_material.msfs_glass_reflection_mask_factor.value,
                    "glassDeformationFactor": blender_material.msfs_glass_deformation_factor.value
                },
                required=False
            )

        # Decal
        elif blender_material.msfs_material_mode.value == "msfs_decal":
            gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = Extension(
                name="ASOBO_material_blend_gbuffer",
                extension={
                    "enabled": True,
                    "baseColorBlendFactor": blender_material.msfs_decal_blend_factor_color.value,
                    "metallicBlendFactor": blender_material.msfs_decal_blend_factor_metal.value,
                    "roughnessBlendFactor": blender_material.msfs_decal_blend_factor_roughness.value,
                    "normalBlendFactor": blender_material.msfs_decal_blend_factor_normal.value,
                    "emissiveBlendFactor": blender_material.msfs_decal_blend_factor_emissive.value,
                    "occlusionBlendFactor": blender_material.msfs_decal_blend_factor_occlusion.value,
                },
                required=False
            )

        # Clearcoat
        elif blender_material.msfs_material_mode.value == "msfs_clearcoat":
            gltf2_material.extensions["ASOBO_material_clear_coat"] = Extension(
                name="ASOBO_material_clear_coat",
                extension={
                    "dirtTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_clearcoat_texture.value, export_settings)
                },
                required=False
            )

        # Environment occluder
        elif blender_material.msfs_material_mode.value == "msfs_env_occluder":
            gltf2_material.extensions["ASOBO_material_environment_occluder"] = Extension(
                name="ASOBO_material_environment_occluder",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Fake terrain
        elif blender_material.msfs_material_mode.value == "msfs_fake_terrain":
            gltf2_material.extensions["ASOBO_material_fake_terrain"] = Extension(
                name="ASOBO_material_fake_terrain",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Fresnel
        elif blender_material.msfs_material_mode.value == "msfs_fresnel":
            gltf2_material.extensions["ASOBO_material_fresnel_fade"] = Extension(
                name="ASOBO_material_fresnel_fade",
                extension={
                    "fresnelFactor": blender_material.msfs_fresnel_factor.value,
                    "fresnelOpacityOffset": blender_material.msfs_fresnel_opacity_bias.value
                },
                required=False
            )

        # Windshield
        elif blender_material.msfs_material_mode.value == "msfs_windshield":
            if blender_material.msfs_rain_drop_scale.value > 0:
                gltf2_material.extensions["ASOBO_material_windshield_v2"] = Extension(
                    name="ASOBO_material_windshield_v2",
                    extension={
                        "rainDropScale": blender_material.msfs_rain_drop_scale.value,
                        "wiper1State": blender_material.msfs_wiper_1_state.value,
                        "wiper2State": blender_material.msfs_wiper_2_state.value,
                        "wiper3State": blender_material.msfs_wiper_3_state.value,
                        "wiper4State": blender_material.msfs_wiper_4_state.value
                    },
                    required=False
                )

            gltf2_material.extras["ASOBO_material_code"] = "Windshield"

        # Porthole
        elif blender_material.msfs_material_mode.value == "msfs_porthole":
            gltf2_material.extras["ASOBO_material_code"] = "Porthole"

        # Parallax
        elif blender_material.msfs_material_mode.value == "msfs_parallax":
            gltf2_material.extensions["ASOBO_material_parallax_window"] = Extension(
                name="ASOBO_material_parallax_window",
                extension={
                    "parallaxScale": blender_material.msfs_parallax_scale.value,
                    "roomSizeXScale": blender_material.msfs_parallax_room_size_x.value,
                    "roomSizeYScale": blender_material.msfs_parallax_room_size_y.value,
                    "roomNumberXY": blender_material.msfs_parallax_room_number.value,
                    "corridor": blender_material.msfs_parallax_corridor.value,
                    "behindWindowMapTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_behind_glass_texture, export_settings)
                },
                required=False
            )

        # Geo decal
        elif blender_material.msfs_material_mode.value == "msfs_geo_decal":
            gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = Extension(
                name="ASOBO_material_blend_gbuffer",
                extension={
                    "baseColorBlendFactor": blender_material.msfs_geo_decal_blend_factor_color.value,
                    "metallicBlendFactor": blender_material.msfs_geo_decal_blend_factor_metal.value,
                    "roughnessBlendFactor": blender_material.msfs_geo_decal_blend_factor_roughness.value,
                    "normalBlendFactor": blender_material.msfs_geo_decal_blend_factor_normal.value,
                    "emissiveBlendFactor": blender_material.msfs_geo_decal_blend_factor_melt_sys.value,
                    "occlusionBlendFactor": blender_material.msfs_geo_decal_blend_factor_blast_sys.value,
                },
                required=False
            )
            gltf2_material.extras["ASOBO_material_code"] = "GeoDecalFrosted"

        # Invisible
        elif blender_material.msfs_material_mode.value == "msfs_invisible":
            gltf2_material.extensions["ASOBO_material_invisible"] = Extension(
                name="ASOBO_material_invisible",
                extension={
                    "enabled": True
                },
                required=False
            )


        # Set blendmode
        if blender_material.msfs_show_blend_mode and blender_material.msfs_blend_mode.value == 'DITHER':
            gltf2_material.extensions["ASOBO_material_alphamode_dither"] = Extension(
                name="ASOBO_material_alphamode_dither",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Set Asobo tags
        if blender_material.msfs_show_road_material or blender_material.msfs_show_collision_material:
            tags = []
            if blender_material.msfs_road_material.value == True:
                tags.append("Road")
            if blender_material.msfs_collision_material.value == True:
                tags.append("Collision")

            if tags:
                gltf2_material.extensions["ASOBO_tags"] = Extension(
                    name="ASOBO_tags",
                    extension={
                        "tags": tags
                    },
                    required=False
                )

        # Day/Night cycle
        if blender_material.msfs_show_day_night_cycle and blender_material.msfs_day_night_cycle.value:
            gltf2_material.extensions["ASOBO_material_day_night_switch"] = Extension(
                name="ASOBO_material_day_night_switch",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Draw order
        if blender_material.msfs_show_draworder and blender_material.msfs_draw_order.value > 0:
            gltf2_material.extensions["ASOBO_material_draw_order"] = Extension(
                name="ASOBO_material_draw_order",
                extension={
                    "drawOrderOffset": blender_material.msfs_draw_order.value
                },
                required=False
            )

        # Cast shadow
        if blender_material.msfs_show_no_cast_shadow and blender_material.msfs_no_cast_shadow.value:
            gltf2_material.extensions["ASOBO_material_shadow_options"] = Extension(
                name="ASOBO_material_shadow_options",
                extension={
                    "noCastShadow": blender_material.msfs_no_cast_shadow.value
                },
                required=False
            )

        # Pearlescent
        if blender_material.msfs_show_pearl and blender_material.msfs_use_pearl_effect.value:
            gltf2_material.extensions["ASOBO_material_pearlescent"] = Extension(
                name="ASOBO_material_pearlescent",
                extension={
                    "pearlShift": blender_material.msfs_pearl_shift.value,
                    "pearlRange": blender_material.msfs_pearl_range.value,
                    "pearlBrightness": blender_material.msfs_pearl_brightness.value
                },
                required=False
            )

        # UV Options
        if blender_material.msfs_show_ao_use_uv2 or blender_material.msfs_show_uv_clamp:
            gltf2_material.extensions["ASOBO_material_UV_options"] = Extension(
                name="ASOBO_material_UV_options",
                extension={
                    "AOUseUV2": blender_material.msfs_ao_use_uv2.value,
                    "clampUVX": blender_material.msfs_uv_clamp_x.value,
                    "clampUVY": blender_material.msfs_uv_clamp_y.value,
                    "clampUVZ": blender_material.msfs_uv_clamp_z.value,
                    "UVOffsetU": blender_material.msfs_uv_offset_u.value,
                    "UVOffsetV": blender_material.msfs_uv_offset_v.value,
                    "UVTilingU": blender_material.msfs_uv_tiling_u.value,
                    "UVTilingV": blender_material.msfs_uv_tiling_v.value,
                    "UVRotation": blender_material.msfs_uv_rotation.value
                },
                required=False
            )

        # Detail maps
        if (blender_material.msfs_show_detail_albedo or blender_material.msfs_show_detail_metallic or  \
                blender_material.msfs_show_detail_normal):
            extension = {}
            if blender_material.msfs_detail_albedo_texture:
                extension["detailColorTexture"] = MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_albedo_texture, export_settings)
            if blender_material.msfs_detail_metallic_texture:
                extension["detailMetalRoughAOTexture"] = MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_metallic_texture, export_settings)
            if blender_material.msfs_detail_normal_texture:
                extension["detailNormalTexture"] = MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_normal_texture, export_settings)
            if extension:
                extension["UVScale"] = blender_material.msfs_detail_uv_scale.value
                extension["UVOffset"] = (blender_material.msfs_detail_uv_offset_x.value, blender_material.msfs_detail_uv_offset_y.value)
                extension["blendThreshold"] = blender_material.msfs_blend_threshold.value

                gltf2_material.extensions["ASOBO_material_detail_map"] = Extension(
                        name="ASOBO_material_detail_map",
                        extension=extension,
                        required=False
                    )
