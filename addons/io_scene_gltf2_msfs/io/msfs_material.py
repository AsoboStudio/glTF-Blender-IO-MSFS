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

import os
import bpy

from ..com import msfs_material_props as MSFSMaterialExtensions

from io_scene_gltf2.blender.imp.gltf2_blender_image import BlenderImage
from io_scene_gltf2.blender.exp.gltf2_blender_gather_texture_info import (
    gather_texture_info,
    gather_material_normal_texture_info_class,
    gather_material_occlusion_texture_info_class,
)


class MSFSMaterial:
    bl_options = {"UNDO"}

    extensions = [
        MSFSMaterialExtensions.AsoboMaterialCommon,
        MSFSMaterialExtensions.AsoboMaterialGeometryDecal,
        MSFSMaterialExtensions.AsoboMaterialGhostEffect,
        MSFSMaterialExtensions.AsoboMaterialDrawOrder,
        MSFSMaterialExtensions.AsoboDayNightCycle,
        MSFSMaterialExtensions.AsoboDisableMotionBlur,
        MSFSMaterialExtensions.AsoboPearlescent,
        MSFSMaterialExtensions.AsoboAlphaModeDither,
        MSFSMaterialExtensions.AsoboMaterialInvisible,
        MSFSMaterialExtensions.AsoboMaterialEnvironmentOccluder,
        MSFSMaterialExtensions.AsoboMaterialUVOptions,
        MSFSMaterialExtensions.AsoboMaterialShadowOptions,
        MSFSMaterialExtensions.AsoboMaterialResponsiveAAOptions,
        MSFSMaterialExtensions.AsoboMaterialDetail,
        MSFSMaterialExtensions.AsoboMaterialFakeTerrain,
        MSFSMaterialExtensions.AsoboMaterialFresnelFade,
        MSFSMaterialExtensions.AsoboSSS,
        MSFSMaterialExtensions.AsoboAnisotropic,
        MSFSMaterialExtensions.AsoboWindshield,
        MSFSMaterialExtensions.AsoboClearCoat,
        MSFSMaterialExtensions.AsoboParallaxWindow,
        MSFSMaterialExtensions.AsoboGlass,
        MSFSMaterialExtensions.AsoboTags,
        MSFSMaterialExtensions.AsoboMaterialCode,
    ]

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create_image(index, import_settings):
        pytexture = import_settings.data.textures[index]
        BlenderImage.create(import_settings, pytexture.source)
        pyimg = import_settings.data.images[pytexture.source]

        # Find image created
        blender_image_name = pyimg.blender_image_name
        if blender_image_name:
            return bpy.data.images[blender_image_name]

    @staticmethod
    def export_image(
        blender_material, blender_image, type, export_settings, normal_scale=None
    ):
        nodes = blender_material.node_tree.nodes
        links = blender_material.node_tree.links

        # Create a fake texture node temporarily (unfortunately this is the only solid way of doing this)
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = blender_image

        # Create shader to plug texture into
        shader_node = nodes.new("ShaderNodeBsdfPrincipled")

        # Gather texture info
        if type == "DEFAULT":
            link = links.new(shader_node.inputs["Base Color"], texture_node.outputs[0])

            texture_info = gather_texture_info(
                shader_node.inputs["Base Color"],
                (shader_node.inputs["Base Color"],),
                export_settings,
            )
        elif type == "NORMAL":
            normal_node = nodes.new("ShaderNodeNormalMap")
            if normal_scale:
                normal_node.inputs["Strength"].default_value = normal_scale
            link = links.new(normal_node.inputs["Color"], texture_node.outputs[0])
            normal_blend_link = links.new(
                shader_node.inputs["Normal"], normal_node.outputs[0]
            )

            texture_info = gather_material_normal_texture_info_class(
                shader_node.inputs["Normal"],
                (shader_node.inputs["Normal"],),
                export_settings,
            )

            links.remove(normal_blend_link)
        elif type == "OCCLUSION":
            # TODO: handle this - may not be needed
            texture_info = gather_material_occlusion_texture_info_class(
                shader_node.inputs[0], (shader_node.inputs[0],), export_settings
            )

        # Delete temp nodes
        links.remove(link)
        nodes.remove(shader_node)
        nodes.remove(texture_node)
        if type == "NORMAL":
            nodes.remove(normal_node)

        # Some versions of the Khronos exporter have gather_texture_info return a tuple
        if isinstance(texture_info, tuple):
            texture_info = texture_info[0]

        return texture_info

    @staticmethod
    def create(gltf2_material, blender_material, import_settings):
        for extension in MSFSMaterial.extensions:
            extension.from_dict(blender_material, gltf2_material, import_settings)

    @staticmethod
    def export(gltf2_material, blender_material, export_settings):
        for extension in MSFSMaterial.extensions:
            extension.to_extension(blender_material, gltf2_material, export_settings)
