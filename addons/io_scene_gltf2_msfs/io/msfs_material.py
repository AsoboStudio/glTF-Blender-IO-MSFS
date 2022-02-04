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
    def create_image(index, import_settings):
        pytexture = import_settings.data.textures[index]
        BlenderImage.create(import_settings, pytexture.source)
        pyimg = import_settings.data.images[pytexture.source]

        # Find image created
        if pyimg.name in bpy.data.images:
            return bpy.data.images[pyimg.name]
        elif os.path.basename(pyimg.uri) in bpy.data.images:
            return bpy.data.images[pyimg.uri]
        elif "Image_%d" % index in bpy.data.images:
            return bpy.data.images["Image_%d" % index]

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
    def create(gltf_material, blender_material, import_settings):
        # Set material type
        material_type = None
        if gltf_material.extras.get("ASOBO_material_code") == "GeoDecalFrosted":
            material_type = "msfs_geo_decal"
        elif gltf_material.extras.get("ASOBO_material_code") == "Porthole":
            material_type = "msfs_porthole"
        elif gltf_material.extras.get("ASOBO_material_code") == "Windshield":
            material_type = "msfs_windshield"

        if not material_type:  # Because some materials share the extension name, we need to check the extras first for material type
            if "ASOBO_material_anisotropic" in gltf_material.extensions:
                material_type = "msfs_anisotropic"
            elif "ASOBO_material_SSS" in gltf_material.extensions:  # This is both hair and SSS, as they share the same properties
                material_type = "msfs_sss"
            elif "ASOBO_material_glass" in gltf_material.extensions:
                material_type = "msfs_glass"
            elif "ASOBO_material_blend_gbuffer" in gltf_material.extensions:
                material_type = "msfs_decal"
            elif "ASOBO_material_clear_coat" in gltf_material.extensions:
                material_type = "msfs_clearcoat"
            elif "ASOBO_material_fake_terrain" in gltf_material.extensions:
                material_type = "msfs_fake_terrain"
            elif "ASOBO_material_fresnel_fade" in gltf_material.extensions:
                material_type = "msfs_fresnel"
            elif "ASOBO_material_parallax_window" in gltf_material.extensions:
                material_type = "msfs_parallax"
            elif "ASOBO_material_environment_occluder" in gltf_material.extensions:
                material_type = "msfs_env_occluder"
            elif "ASOBO_material_invisible" in gltf_material.extensions:
                material_type = "msfs_invisible"
            else:
                for key in gltf_material.extensions.keys():  # Check all extensions and see if any Asobo extensions are present, and if so, it's a standard material
                    if key.upper().startswith("ASOBO_"):
                        material_type = "msfs_standard"

        blender_material.msfs_material_mode = material_type

        # Set blendmode
        if gltf_material.extensions.get("ASOBO_material_alphamode_dither", {}).get("enabled"):
            blender_material.blend_mode = "DITHER"

        # Set Asobo tags
        tags = gltf_material.extensions.get("ASOBO_tags")
        if tags:
            if "Road" in tags:
                gltf_material.msfs_road_material = True
            if "Collision" in tags:
                gltf_material.msfs_collision_material = True

        # Day/Night cycle
        if gltf_material.extensions.get("ASOBO_material_day_night_switch", {}).get("enabled"):
            gltf_material.msfs_day_night_cycle = True

        # Windshield options
        windshield = gltf_material.extensions.get("ASOBO_material_windshield_v2")  # TODO: maybe add support for v1?
        if windshield:
            blender_material.msfs_rain_drop_scale = windshield.get("rainDropScale")
            blender_material.msfs_wiper_1_state = windshield.get("wiper1State")
            blender_material.msfs_wiper_2_state = windshield.get("wiper2State")
            blender_material.msfs_wiper_3_state = windshield.get("wiper3State")
            blender_material.msfs_wiper_4_state = windshield.get("wiper4State")

        # Draw order
        draw_order = gltf_material.extensions.get("ASOBO_material_draw_order")
        if draw_order:
            blender_material.msfs_draw_order = draw_order.get("drawOrderOffset")

        # Cast shadow
        cast_shadow = gltf_material.extensions.get("ASOBO_material_shadow_options")
        if cast_shadow:
            blender_material.msfs_no_cast_shadow = cast_shadow.get("noCastShadow")

        # Pearlescent
        pearl = gltf_material.extensions.get("ASOBO_material_pearlescent")
        if pearl:
            blender_material.msfs_pearl_shift = pearl.get("pearlShift")
            blender_material.msfs_pearl_range = pearl.get("pearlRange")
            blender_material.msfs_pearl_brightness = pearl.get("pearlBrightness")

        # UV Options
        uv_options = gltf_material.extensions.get("ASOBO_material_UV_options")
        if uv_options:
            blender_material.msfs_ao_use_uv2 = uv_options.get("AOUseUV2")
            blender_material.msfs_uv_clamp_x = uv_options.get("clampUVX")
            blender_material.msfs_uv_clamp_y = uv_options.get("clampUVY")
            blender_material.msfs_uv_clamp_z = uv_options.get("clampUVZ")

        # Detail maps
        detail_map = gltf_material.extensions.get("ASOBO_material_detail_map")
        if detail_map:
            detail_color_index = detail_map.get("detailColorTexture", {}).get("index")
            if detail_color_index is not None:
                blender_material.msfs_detail_albedo_texture = MSFSMaterial.create_image(detail_color_index, import_settings)

            detail_metal_index = detail_map.get("detailMetalRoughAOTexture", {}).get("index")
            if detail_metal_index is not None:
                blender_material.msfs_detail_metallic_texture = MSFSMaterial.create_image(detail_metal_index, import_settings)

            detail_normal_index = detail_map.get("detailNormalTexture", {}).get("index")
            if detail_normal_index is not None:
                blender_material.msfs_detail_normal_texture = MSFSMaterial.create_image(detail_normal_index, import_settings)

            blender_material.msfs_detail_uv_scale = detail_map.get("UVScale")
            blender_material.msfs_detail_uv_offset_x = detail_map.get("UVOffset")[0]
            blender_material.msfs_detail_uv_offset_y = detail_map.get("UVOffset")[1]
            blender_material.msfs_blend_threshold = detail_map.get("blendTreshold")

        # Blend gbuffer
        blend_gbuffer = gltf_material.extensions.get("ASOBO_material_blend_gbuffer")
        if blend_gbuffer:
            if material_type == "msfs_decal":  # Decal and geo decal share properties but with different variable names
                blender_material.msfs_decal_blend_factor_color = blend_gbuffer.get("baseColorBlendFactor")
                blender_material.msfs_decal_blend_factor_metal = blend_gbuffer.get("metallicBlendFactor")
                blender_material.msfs_decal_blend_factor_roughness = blend_gbuffer.get("roughnessBlendFactor")
                blender_material.msfs_decal_blend_factor_normal = blend_gbuffer.get("normalBlendFactor")
                blender_material.msfs_decal_blend_factor_emissive = blend_gbuffer.get("emissiveBlendFactor")
                blender_material.msfs_decal_blend_factor_occlusion = blend_gbuffer.get("occlusionBlendFactor")
            else:
                blender_material.msfs_geo_decal_blend_factor_color = blend_gbuffer.get("baseColorBlendFactor")
                blender_material.msfs_geo_decal_blend_factor_metal = blend_gbuffer.get("metallicBlendFactor")
                blender_material.msfs_geo_decal_blend_factor_roughness = blend_gbuffer.get("roughnessBlendFactor")
                blender_material.msfs_geo_decal_blend_factor_normal = blend_gbuffer.get("normalBlendFactor")
                blender_material.msfs_geo_decal_blend_factor_melt_sys = blend_gbuffer.get("emissiveBlendFactor")
                blender_material.msfs_geo_decal_blend_factor_blast_sys = blend_gbuffer.get("occlusionBlendFactor")

        # SSS
        if material_type == "msfs_sss":
            sss_extension = blender_material.extensions.get("ASOBO_material_SSS", {})

            blender_material.msfs_color_sss = sss_extension.get("SSSColor")

        # Glass
        elif material_type == "msfs_glass":
            glass_extension = blender_material.extensions.get("ASOBO_material_glass", {})

            blender_material.msfs_glass_reflection_mask_factor = glass_extension.get("glassReflectionMaskFactor")
            blender_material.msfs_glass_deformation_factor = glass_extension.get("glassDeformationFactor")

        # Clearcoat
        elif material_type == "msfs_clearcoat":
            clearcoat_extension = blender_material.extensions.get("ASOBO_material_clear_coat", {})

            dirt_index = clearcoat_extension.get("dirtTexture", {}).get("index")
            if dirt_index is not None:
                blender_material.msfs_clearcoat_texture = MSFSMaterial.create_image(dirt_index, import_settings)

        # Fresnel
        elif material_type == "msfs_fresnel":
            fresnel_extension = blender_material.extensions.get("ASOBO_material_fresnel_fade", {})

            blender_material.msfs_fresnel_factor = fresnel_extension.get("fresnelFactor")
            blender_material.msfs_fresnel_opacity_bias = fresnel_extension.get("fresnelOpacityOffset")

        # Parallax
        elif material_type == "msfs_parallax":
            parallax_extension = blender_material.extensions.get("ASOBO_material_parallax_window", {})

            blender_material.msfs_parallax_scale = parallax_extension.get("parallaxScale")
            blender_material.msfs_parallax_room_size_x = parallax_extension.get("roomSizeXScale")
            blender_material.msfs_parallax_room_size_y = parallax_extension.get("roomSizeYScale")
            blender_material.msfs_parallax_room_number = parallax_extension.get("roomNumberXY")
            blender_material.msfs_parallax_corridor = parallax_extension.get("corridor")

            behind_window_index = parallax_extension.get("behindWindowMapTexture", {}).get("index")
            if behind_window_index is not None:
                blender_material.msfs_behind_glass_texture = MSFSMaterial.create_image(behind_window_index, import_settings)

    @staticmethod
    def export(gltf2_material, blender_material, export_settings):
        # Set material type and related properties
        # Anisotropic
        if blender_material.msfs_material_mode == "msfs_anisotropic":
            gltf2_material.extensions["ASOBO_material_anisotropic"] = Extension(
                name="ASOBO_material_anisotropic",
                extension={
                    "enabled": True
                },
                required=False
            )

        # SSS, Hair
        elif blender_material.msfs_material_mode in ["msfs_sss", "msfs_hair"]:
            gltf2_material.extensions["ASOBO_material_SSS"] = Extension(
                name="ASOBO_material_SSS",
                extension={
                    "SSSColor": list(blender_material.msfs_color_sss)
                },
                required=False
            )

        # Hair
        elif blender_material.msfs_material_mode == "msfs_glass":
            gltf2_material.extensions["ASOBO_material_glass"] = Extension(
                name="ASOBO_material_glass",
                extension={
                    "glassReflectionMaskFactor": blender_material.msfs_glass_reflection_mask_factor,
                    "glassDeformationFactor": blender_material.msfs_glass_deformation_factor
                },
                required=False
            )

        # Decal
        elif blender_material.msfs_material_mode == "msfs_decal":
            gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = Extension(
                name="ASOBO_material_blend_gbuffer",
                extension={
                    "enabled": True,
                    "baseColorBlendFactor": blender_material.msfs_decal_blend_factor_color,
                    "metallicBlendFactor": blender_material.msfs_decal_blend_factor_metal,
                    "roughnessBlendFactor": blender_material.msfs_decal_blend_factor_roughness,
                    "normalBlendFactor": blender_material.msfs_decal_blend_factor_normal,
                    "emissiveBlendFactor": blender_material.msfs_decal_blend_factor_emissive,
                    "occlusionBlendFactor": blender_material.msfs_decal_blend_factor_occlusion,
                },
                required=False
            )

        # Clearcoat
        elif blender_material.msfs_material_mode == "msfs_clearcoat":
            gltf2_material.extensions["ASOBO_material_clear_coat"] = Extension(
                name="ASOBO_material_clear_coat",
                extension={
                    "dirtTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_clearcoat_texture, export_settings)
                },
                required=False
            )

        # Environment occluder
        elif blender_material.msfs_material_mode == "msfs_env_occluder":
            gltf2_material.extensions["ASOBO_material_environment_occluder"] = Extension(
                name="ASOBO_material_environment_occluder",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Fake terrain
        elif blender_material.msfs_material_mode == "msfs_fake_terrain":
            gltf2_material.extensions["ASOBO_material_fake_terrain"] = Extension(
                name="ASOBO_material_fake_terrain",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Fresnel
        elif blender_material.msfs_material_mode == "msfs_fresnel":
            gltf2_material.extensions["ASOBO_material_fresnel_fade"] = Extension(
                name="ASOBO_material_fresnel_fade",
                extension={
                    "fresnelFactor": blender_material.msfs_fresnel_factor,
                    "fresnelOpacityOffset": blender_material.msfs_fresnel_opacity_bias
                },
                required=False
            )

        # Windshield
        elif blender_material.msfs_material_mode == "msfs_windshield":
            if blender_material.msfs_rain_drop_scale > 0:
                gltf2_material.extensions["ASOBO_material_windshield_v2"] = Extension(
                    name="ASOBO_material_windshield_v2",
                    extension={
                        "rainDropScale": blender_material.msfs_rain_drop_scale,
                        "wiper1State": blender_material.msfs_wiper_1_state,
                        "wiper2State": blender_material.msfs_wiper_2_state,
                        "wiper3State": blender_material.msfs_wiper_3_state,
                        "wiper4State": blender_material.msfs_wiper_4_state
                    },
                    required=False
                )

            gltf2_material.extras["ASOBO_material_code"] = "Windshield"

        # Porthole
        elif blender_material.msfs_material_mode == "msfs_porthole":
            gltf2_material.extras["ASOBO_material_code"] = "Porthole"

        # Parallax
        elif blender_material.msfs_material_mode == "msfs_parallax":
            gltf2_material.extensions["ASOBO_material_parallax_window"] = Extension(
                name="ASOBO_material_parallax_window",
                extension={
                    "parallaxScale": blender_material.msfs_parallax_scale,
                    "roomSizeXScale": blender_material.msfs_parallax_room_size_x,
                    "roomSizeYScale": blender_material.msfs_parallax_room_size_y,
                    "roomNumberXY": blender_material.msfs_parallax_room_number,
                    "corridor": blender_material.msfs_parallax_corridor,
                    "behindWindowMapTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_behind_glass_texture, export_settings)
                },
                required=False
            )

        # Geo decal
        elif blender_material.msfs_material_mode == "msfs_geo_decal":
            gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = Extension(
                name="ASOBO_material_blend_gbuffer",
                extension={
                    "baseColorBlendFactor": blender_material.msfs_geo_decal_blend_factor_color,
                    "metallicBlendFactor": blender_material.msfs_geo_decal_blend_factor_metal,
                    "roughnessBlendFactor": blender_material.msfs_geo_decal_blend_factor_roughness,
                    "normalBlendFactor": blender_material.msfs_geo_decal_blend_factor_normal,
                    "emissiveBlendFactor": blender_material.msfs_geo_decal_blend_factor_melt_sys,
                    "occlusionBlendFactor": blender_material.msfs_geo_decal_blend_factor_blast_sys,
                },
                required=False
            )
            gltf2_material.extras["ASOBO_material_code"] = "GeoDecalFrosted"

        # Invisible
        elif blender_material.msfs_material_mode == "msfs_invisible":
            gltf2_material.extensions["ASOBO_material_invisible"] = Extension(
                name="ASOBO_material_invisible",
                extension={
                    "enabled": True
                },
                required=False
            )


        # Set blendmode
        if blender_material.msfs_show_blend_mode and blender_material.msfs_blend_mode == 'DITHER':
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
            if blender_material.msfs_road_material == True:
                tags.append("Road")
            if blender_material.msfs_collision_material == True:
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
        if blender_material.msfs_show_day_night_cycle and blender_material.msfs_day_night_cycle:
            gltf2_material.extensions["ASOBO_material_day_night_switch"] = Extension(
                name="ASOBO_material_day_night_switch",
                extension={
                    "enabled": True
                },
                required=False
            )

        # Draw order
        if blender_material.msfs_show_draworder and blender_material.msfs_draw_order > 0:
            gltf2_material.extensions["ASOBO_material_draw_order"] = Extension(
                name="ASOBO_material_draw_order",
                extension={
                    "drawOrderOffset": blender_material.msfs_draw_order
                },
                required=False
            )

        # Cast shadow
        if blender_material.msfs_show_no_cast_shadow and blender_material.msfs_no_cast_shadow:
            gltf2_material.extensions["ASOBO_material_shadow_options"] = Extension(
                name="ASOBO_material_shadow_options",
                extension={
                    "noCastShadow": blender_material.msfs_no_cast_shadow
                },
                required=False
            )

        # Pearlescent
        if blender_material.msfs_show_pearl and blender_material.msfs_use_pearl_effect:
            gltf2_material.extensions["ASOBO_material_pearlescent"] = Extension(
                name="ASOBO_material_pearlescent",
                extension={
                    "pearlShift": blender_material.msfs_pearl_shift,
                    "pearlRange": blender_material.msfs_pearl_range,
                    "pearlBrightness": blender_material.msfs_pearl_brightness
                },
                required=False
            )

        # UV Options
        if blender_material.msfs_show_ao_use_uv2 or blender_material.msfs_show_uv_clamp:
            if (blender_material.msfs_ao_use_uv2 or blender_material.msfs_uv_clamp_x or \
                    blender_material.msfs_uv_clamp_y or blender_material.msfs_uv_clamp_z):
                gltf2_material.extensions["ASOBO_material_UV_options"] = Extension(
                    name="ASOBO_material_UV_options",
                    extension={
                        "AOUseUV2": blender_material.msfs_ao_use_uv2,
                        "clampUVX": blender_material.msfs_uv_clamp_x,
                        "clampUVY": blender_material.msfs_uv_clamp_y,
                        "clampUVZ": blender_material.msfs_uv_clamp_z
                    },
                    required=False
                )

        # Detail maps
        if (blender_material.msfs_show_detail_albedo or blender_material.msfs_show_detail_metallic or  \
                blender_material.msfs_show_detail_normal):
            gltf2_material.extensions["ASOBO_material_detail_map"] = Extension(
                    name="ASOBO_material_detail_map",
                    extension={
                        "detailColorTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_albedo_texture, export_settings),
                        "detailMetalRoughAOTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_metallic_texture, export_settings),
                        "detailNormalTexture": MSFSMaterial.export_image(blender_material, blender_material.msfs_detail_normal_texture, export_settings),
                        "UVScale": blender_material.msfs_detail_uv_scale,
                        "UVOffset": (blender_material.msfs_detail_uv_offset_x, blender_material.msfs_detail_uv_offset_y),
                        "blendThreshold": blender_material.msfs_blend_threshold
                    },
                    required=False
                )
