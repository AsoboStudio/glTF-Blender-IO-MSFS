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
import urllib
import bpy

from .. import get_version_string
from .msfs_gizmo import MSFSGizmo
from .msfs_light import MSFSLight
from .msfs_material import MSFSMaterial
from .msfs_unique_id import MSFS_unique_id


class Export:
    
    def gather_asset_hook(self, gltf2_asset, export_settings):
        if self.properties.enabled == True:
            if gltf2_asset.extensions is None:
                gltf2_asset.extensions = {}
            gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
                name="ASOBO_normal_map_convention",
                extension={"tangent_space_convention": "DirectX"},
                required=False
            )

            gltf2_asset.generator += " and Asobo Studio MSFS Blender I/O v" + get_version_string()

        # for the vetex color rainbow
        # asset hook is called first before the nodes and objects and mesh, so we make changes to the meshes here
        # possible caching of blender data may result in changes not takeng at the point of hook function running
        # does not work in:
        # def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, skip_filter, materials, export_settings):

        #print("gather_asset_hook - Started with ", gltf2_asset)
        for o in bpy.context.scene.objects:
            #print("gather_asset_hook - Scene Object",o)
            # only for meshes
            if o.type == 'MESH':
                obj = o
                #print("gather_asset_hook - obj", obj, obj.data)
                for ca in obj.data.color_attributes:
                    if ca.data_type != 'FLOAT_COLOR':
                        print("gather_asset_hook - col before", obj, ca.domain, ca.data_type)
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.geometry.attribute_convert(mode='GENERIC', domain='CORNER', data_type='FLOAT_COLOR')
                        print("gather_asset_hook - After", obj, obj.data)
                        for ca in obj.data.color_attributes:
                            print("gather_asset_hook - col after", obj, ca.data_type)
        print("gather_asset_hook - Done")

    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        if self.properties.enabled:
            for i, image in enumerate(gltf2_plan.images):
                image.uri = os.path.basename(urllib.parse.unquote(image.uri))

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled:

            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_object, blender_object)

            if blender_object.type == 'LIGHT':
                MSFSLight.export(gltf2_object, blender_object)
    
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        if self.properties.enabled:

            if gltf2_node.extensions is None:
                gltf2_node.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_node, blender_bone)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        if self.properties.enabled:
            MSFSGizmo.export(gltf2_scene.nodes, blender_scene, export_settings)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        # blender 3.3 removes base color values with base color texture - have to add back in
        print("gather_material_hook - Started with gltf2_material", gltf2_material, gltf2_material.pbr_metallic_roughness, gltf2_material.pbr_metallic_roughness.base_color_texture, gltf2_material.pbr_metallic_roughness.base_color_factor)
        # #print("exportsettings", export_settings)
        print("gather_material_hook - blender material", blender_material, blender_material.msfs_base_color_texture, blender_material.msfs_base_color_factor)
        # if it has a detail color texture then set basecolor to none
        base_color = blender_material.msfs_base_color_factor
        print("gather_material_hook - blender material - delete base color before", blender_material, blender_material.msfs_base_color_texture, base_color[0], base_color[1], base_color[2], base_color[3])
        if gltf2_material.pbr_metallic_roughness.base_color_factor is None:
            #gltf2_material.pbr_metallic_roughness.base_color_factor = base_color
            gltf2_material.pbr_metallic_roughness.base_color_factor = [base_color[0],base_color[1],base_color[2],base_color[3]]
        print("gather_material_hook - blender material - delete base color after", blender_material, blender_material.msfs_base_color_texture, blender_material.msfs_base_color_factor, gltf2_material.pbr_metallic_roughness.base_color_factor)
        if self.properties.enabled:
            print("gather_material_hook - export")
            MSFSMaterial.export(gltf2_material, blender_material, export_settings)
        print("gather_material_hook - Done")
