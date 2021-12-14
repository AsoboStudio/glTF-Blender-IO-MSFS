# Copyright 2021 The FlightSim-glTF-Blender-IO authors.
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
import inspect
import pkgutil
import importlib
from pathlib import Path

bl_info = {
    "name": "Microsoft Flight Simulator glTF Extension",
    "author": "Luca Pierabella, Wing42, pepperoni505, ronh991, tml1024, and others",
    "description": "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
    "location": "File > Import-Export",
    "warning": "This version of the addon is work-in-progress. Don't use it in your active development cycle, as it adds variables and objects to the scene that may cause issues further down the line.",
    "category": "Import-Export",
    "tracker_url": "https://github.com/AsoboStudio/FlightSim-glTF-Blender-IO"
}


class ExtAsoboProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name='ASOBO extensions',
        description='ASOBO extension for glTF',
        default=True
    )


class GLTF_PT_AsoboExtensionPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Enabled"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_location = "File > Export > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Blender2MSFS Extensions", icon='TOOL_SETTINGS')

    def draw(self, context):
        props = bpy.context.scene.msfs_ExtAsoboProperties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(props, 'enabled')


def recursive_module_search(path, root=""):
    for _, name, ispkg in pkgutil.iter_modules([str(path)]):
        if ispkg:
            yield from recursive_module_search(path / name, f"{root}.{name}")
        else:
            yield root, name


def modules():
    for root, name in recursive_module_search(Path(__file__).parent):
        if name in locals():
            yield importlib.reload(locals()[name])
        else:
            yield importlib.import_module(f".{name}", package=f"{__package__}{root}")


classes = []


# Refresh the list of classes
def update_class_list():
    global classes

    classes = []

    for module in modules():
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) \
                    and module.__name__ in str(obj) \
                    and "bpy" in str(inspect.getmro(obj)[1]):
                classes.append(obj)


def register():
    # Refresh the list of classes whenever the addon is reloaded so we can stay up to date with the files on disk.
    update_class_list()

    for cls in classes:
        try:
            print( "registering class: {0}".format(cls))
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    try:
        bpy.utils.register_class(ExtAsoboProperties)
    except Exception:
        pass

    bpy.types.Scene.msfs_ExtAsoboProperties = bpy.props.PointerProperty(type=ExtAsoboProperties)


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


def unregister_panel():
    try:
        bpy.utils.unregister_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass


# todo :
# find a way to move this in exp.msfs_export.py 
class glTF2ExportUserExtension:

    ## all glTF2ExportUserExtension  must be decalred here
    # the khronos exporter look only of the __init__ in the preferences-> addons modules
    # look \io_scene_gltf2\__init__.py line 622

    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.msfs_ExtAsoboProperties

    def gather_asset_hook(self, gltf2_asset, export_settings):
        if self.properties.enabled == True:
            if gltf2_asset.extensions is None:
                gltf2_asset.extensions = {}
            gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
                name="ASOBO_normal_map_convention",
                extension={"tangent_space_convention": "DirectX"},
                required=False
            )

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        import math

        if self.properties.enabled == True:
            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if blender_object.type == 'LIGHT':
                angle = 360.0
                if blender_object.data.type == 'SPOT':
                    angle = (180.0 / math.pi) * blender_object.data.spot_size

                gltf2_object.extensions["ASOBO_macro_light"] = self.Extension(
                    name = "ASOBO_macro_light",
                    extension={
                        "color": [blender_object.data.color[0],blender_object.data.color[1],blender_object.data.color[2]],
                        "intensity": blender_object.data.energy,
                        "cone_angle": angle,
                        "has_simmetry": blender_object.msfs_light_has_symmetry,
                        "flash_frequency": blender_object.msfs_light_flash_frequency,
                        "flash_duration": blender_object.msfs_light_flash_duration,
                        "flash_phase": blender_object.msfs_light_flash_phase,
                        "rotation_speed": blender_object.msfs_light_rotation_speed,
                        "day_night_cycle": blender_object.msfs_light_day_night_cycle,
                    },
                    required = False
                )
                


    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if (self.properties.enabled == True and blender_material.msfs_material_mode != None):
            if blender_material.msfs_material_mode != 'NONE':
                if gltf2_material.extensions is None:
                    gltf2_material.extensions = {}
                if gltf2_material.extras is None:
                    gltf2_material.extras = {}
                
                # Check the blend mode and attach extensions if necessary.
                # As far as I can tell, the regular blendmodes don't need an extension to work.
                if blender_material.msfs_show_blend_mode == True:
                    if blender_material.msfs_blend_mode == 'DITHER':
                        gltf2_material.extensions["ASOBO_material_alphamode_dither"] = self.Extension(
                            name="ASOBO_material_alphamode_dither",
                            extension={"enabled": True},
                            required=False
                        )

                if (blender_material.msfs_show_road_material == True or blender_material.msfs_show_collision_material == True):
                    if (blender_material.msfs_road_material == True or blender_material.msfs_collision_material == True):
                        new_ext = {}
                        if blender_material.msfs_road_material == True:
                            new_ext["tags"] = ["Road"]
                        if blender_material.msfs_collision_material == True:
                            new_ext["tags"] = ["Collision"]
                        if blender_material.msfs_collision_material == True and blender_material.msfs_road_material == True:
                            new_ext["tags"] = ["Road", "Collision"]

                        gltf2_material.extensions["ASOBO_tags"] = self.Extension(
                            name="ASOBO_tags",
                            extension=new_ext,
                            required=False
                        )

                if blender_material.msfs_show_day_night_cycle == True:
                    if blender_material.msfs_day_night_cycle == True:
                        gltf2_material.extensions["ASOBO_material_day_night_switch"] = self.Extension(
                            name="ASOBO_material_day_night_switch",
                            extension={ "enabled": True },
                            required=False
                        )

                if blender_material.msfs_show_windshield_options == True:
                    if blender_material.msfs_rain_drop_scale > 0:
                        gltf2_material.extensions["ASOBO_material_windshield_v2"] = self.Extension(
                            name="ASOBO_material_windshield_v2",
                            extension={ "rainDropScale": blender_material.msfs_rain_drop_scale,
                            "wiper1State": blender_material.msfs_wiper_1_state,
                            "wiper2State": blender_material.msfs_wiper_2_state,
                            "wiper3State": blender_material.msfs_wiper_3_state,
                            "wiper4State": blender_material.msfs_wiper_4_state },
                            required=False
                        )

                if blender_material.msfs_show_draworder == True:
                    if blender_material.msfs_draw_order > 0:
                        gltf2_material.extensions["ASOBO_material_draw_order"] = self.Extension(
                            name="ASOBO_material_draw_order",
                            extension={"drawOrderOffset": blender_material.msfs_draw_order},
                            required=False
                        )

                if blender_material.msfs_show_no_cast_shadow == True:
                    if blender_material.msfs_no_cast_shadow == True:
                        gltf2_material.extensions["ASOBO_material_shadow_options"] = self.Extension(
                            name="ASOBO_material_shadow_options",
                            extension={"noCastShadow": blender_material.msfs_no_cast_shadow},
                            required=False
                        )

                if blender_material.msfs_show_pearl == True:
                    if blender_material.msfs_use_pearl_effect == True:
                        gltf2_material.extensions["ASOBO_material_pearlescent"] = self.Extension(
                            name="ASOBO_material_pearlescent",
                            extension={"pearlShift": blender_material.msfs_pearl_shift,
                            "pearlRange": blender_material.msfs_pearl_range,
                            "pearlBrightness": blender_material.msfs_pearl_brightness},
                            required=False
                        )

                #-double-sided injected through material settings
                #-responsive aa missing

                if (blender_material.msfs_show_ao_use_uv2 == True or blender_material.msfs_show_uv_clamp == True):
                    if (blender_material.msfs_ao_use_uv2 == True or blender_material.msfs_uv_clamp_x == True or
                            blender_material.msfs_uv_clamp_y == True or blender_material.msfs_uv_clamp_z == True):
                        gltf2_material.extensions["ASOBO_material_UV_options"] = self.Extension(
                            name="ASOBO_material_UV_options",
                            extension={ "AOUseUV2": blender_material.msfs_ao_use_uv2,
                                        "clampUVX": blender_material.msfs_uv_clamp_x,
                                        "clampUVY": blender_material.msfs_uv_clamp_y,
                                        "clampUVZ": blender_material.msfs_uv_clamp_z},
                            required=False
                        )

                #Let's inject some detail maps, through Asobo extensions:
                if (blender_material.msfs_show_detail_albedo == True or blender_material.msfs_show_detail_metallic == True or blender_material.msfs_show_detail_normal == True):
                    from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import gather_texture_info

                    nodes = blender_material.node_tree.nodes

                    detail_extension = {}
                    if blender_material.msfs_detail_albedo_texture != None:
                        #let's find the node:
                        node = nodes.get("albedo_detail_mix")
                        if node != None:
                            inputs = (node.inputs["Color2"],)
                        albedo_detail_texture = gather_texture_info(inputs, export_settings)
                        if albedo_detail_texture != None:
                            detail_extension["detailColorTexture"] = albedo_detail_texture
                    if blender_material.msfs_detail_metallic_texture != None:
                        #let's find the node:
                        node = nodes.get("metallic_detail_mix")
                        if node != None:
                            inputs = (node.inputs["Color2"],)
                        metallic_detail_texture = gather_texture_info(inputs, export_settings)
                        if metallic_detail_texture != None:
                            detail_extension["detailMetalRoughAOTexture"] = metallic_detail_texture
                    if blender_material.msfs_detail_normal_texture != None:
                        #let's find the node:
                        node = nodes.get("normal_detail_mix")
                        if node != None:
                            inputs = (node.inputs["Color2"],)
                        normal_detail_texture = gather_texture_info(inputs, export_settings)
                        if normal_detail_texture != None:
                            detail_extension["detailNormalTexture"] = normal_detail_texture
                    if len(detail_extension) > 0:
                        detail_extension["UVScale"] = blender_material.msfs_detail_uv_scale
                        detail_extension["UVOffset"] = (blender_material.msfs_detail_uv_offset_x,blender_material.msfs_detail_uv_offset_y)
                        detail_extension["blendTreshold"] = blender_material.msfs_blend_threshold

                        gltf2_material.extensions["ASOBO_material_detail_map"] = self.Extension(
                            name="ASOBO_material_detail_map",
                            extension=detail_extension,
                            required=False
                        )

                #Add the blend gbuffer:
                if blender_material.msfs_show_geo_decal_parameters == True:
                    gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = self.Extension(
                        name="ASOBO_material_blend_gbuffer",
                        extension={ "enabled": True,
                                    "baseColorBlendFactor": blender_material.msfs_geo_decal_blend_factor_color,
                                    "metallicBlendFactor": blender_material.msfs_geo_decal_blend_factor_metal,
                                    "roughnessBlendFactor": blender_material.msfs_geo_decal_blend_factor_roughness,
                                    "normalBlendFactor": blender_material.msfs_geo_decal_blend_factor_normal,
                                    "emissiveBlendFactor": blender_material.msfs_geo_decal_blend_factor_melt_sys,
                                    "occlusionBlendFactor": blender_material.msfs_geo_decal_blend_factor_blast_sys,
                                    },
                        required=False
                    )     

                if blender_material.msfs_show_decal_parameters == True:
                    gltf2_material.extensions["ASOBO_material_blend_gbuffer"] = self.Extension(
                        name="ASOBO_material_blend_gbuffer",
                        extension={ "enabled": True,
                                    "baseColorBlendFactor": blender_material.msfs_decal_blend_factor_color,
                                    "metallicBlendFactor": blender_material.msfs_decal_blend_factor_metal,
                                    "roughnessBlendFactor": blender_material.msfs_decal_blend_factor_roughness,
                                    "normalBlendFactor": blender_material.msfs_decal_blend_factor_normal,
                                    "emissiveBlendFactor": blender_material.msfs_decal_blend_factor_emissive,
                                    "occlusionBlendFactor": blender_material.msfs_decal_blend_factor_occlusion,
                                    },
                        required=False
                    )     

                #Check the material mode of the material and attach the correct extension:
                if blender_material.msfs_material_mode == 'msfs_anisotropic':
                    gltf2_material.extensions["ASOBO_material_anisotropic"] = self.Extension(
                        name="ASOBO_material_anisotropic",
                        extension={},
                        required=False
                    )            
                elif blender_material.msfs_material_mode == 'msfs_sss':
                    gltf2_material.extensions["ASOBO_material_SSS"] = self.Extension(
                        name="ASOBO_material_SSS",
                        extension={"SSSColor": [blender_material.msfs_color_sss[0],blender_material.msfs_color_sss[1],blender_material.msfs_color_sss[2],blender_material.msfs_color_sss[3]]},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_hair':
                    gltf2_material.extensions["ASOBO_material_SSS"] = self.Extension(
                        name="ASOBO_material_SSS",
                        extension={"SSSColor": [blender_material.msfs_color_sss[0],blender_material.msfs_color_sss[1],blender_material.msfs_color_sss[2],blender_material.msfs_color_sss[3]]},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_glass':
                    gltf2_material.extensions["ASOBO_material_glass"] = self.Extension(
                        name="ASOBO_material_glass",
                        extension={"glassReflectionMaskFactor": blender_material.msfs_glass_reflection_mask_factor,
                                "glassDeformationFactor": blender_material.msfs_glass_deformation_factor},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_clearcoat':
                    gltf2_material.extensions["ASOBO_material_clear_coat"] = self.Extension(
                        name="ASOBO_material_clear_coat",
                        extension={"dirtTexture": blender_material.msfs_clearcoat_texture},#TODO: reference the texture properly.
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_fake_terrain':
                    gltf2_material.extensions["ASOBO_material_fake_terrain"] = self.Extension(
                        name="ASOBO_material_fake_terrain",
                        extension={"enabled": True},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_fresnel':
                    gltf2_material.extensions["ASOBO_material_fresnel_fade"] = self.Extension(
                        name="ASOBO_material_fresnel_fade",
                        extension={"fresnelFactor": blender_material.msfs_fresnel_factor,
                                "fresnelOpacityOffset": blender_material.msfs_fresnel_opacity_bias},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_parallax':
                    from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import gather_texture_info

                    nodes = blender_material.node_tree.nodes

                    parallax_extension = {"parallaxScale": blender_material.msfs_parallax_scale,
                                          "roomSizeXScale": blender_material.msfs_parallax_room_size_x,
                                          "roomSizeYScale": blender_material.msfs_parallax_room_size_y,
                                          "roomNumberXY": blender_material.msfs_parallax_room_number,
                                          "corridor": blender_material.msfs_parallax_corridor
                                         }
                    if blender_material.msfs_behind_glass_texture != None:
                        #let's find the node:
                        node = nodes.get("albedo_detail_mix")
                        if node != None:
                            inputs = (node.inputs["Color2"],)
                        behind_glass_texture = gather_texture_info(inputs, export_settings)
                        if behind_glass_texture != None:
                            parallax_extension["behindWindowMapTexture"] = behind_glass_texture

                    gltf2_material.extensions["ASOBO_material_parallax_window"] = self.Extension(
                        name="ASOBO_material_parallax_window",
                        extension=parallax_extension,
                        required=False
                    )                                
                elif blender_material.msfs_material_mode == 'msfs_env_occluder':
                    gltf2_material.extensions["ASOBO_material_environment_occluder"] = self.Extension(
                        name="ASOBO_material_environment_occluder",
                        extension={"enabled": True},
                        required=False
                    )
                elif blender_material.msfs_material_mode == 'msfs_invisible':
                    gltf2_material.extensions["ASOBO_material_invisible"] = self.Extension(
                        name="ASOBO_material_invisible",
                        extension={"enabled": True},
                        required=False
                    )


                #add extras:
                if blender_material.msfs_material_mode == 'msfs_geo_decal':
                    gltf2_material.extras["ASOBO_material_code"] = "GeoDecalFrosted"
                elif blender_material.msfs_material_mode == 'msfs_porthole':
                    gltf2_material.extras["ASOBO_material_code"] = "Porthole"
                elif blender_material.msfs_material_mode == 'msfs_windshield':
                    gltf2_material.extras["ASOBO_material_code"] = "Windshield"