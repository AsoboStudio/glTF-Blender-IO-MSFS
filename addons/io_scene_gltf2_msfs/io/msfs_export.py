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
        if self.properties.enabled:
            MSFSMaterial.export(gltf2_material, blender_material, export_settings)

    # mesh hook to change vertex color attributes in vertex colors from Face Corner - Byte Color default to Face Corner Color (byte to float??)
    # but data looks the same.
    def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, skip_filter, materials, export_settings):
        print("gather_mesh_hookgather_mesh_hook - Started with ", gltf2_mesh, blender_mesh)
        for col in blender_mesh.color_attributes:
            print("gather_mesh_hook - col", col, col.data_type, col.domain, col.name)
            colname_to_remove = ''
            for coldata in col.data:
                if col.data_type == 'BYTE_COLOR':
                    #print("gather_mesh_hook - col data byte", col.data_type, coldata)
                    colname_to_remove = col.name
                else:
                    #print("gather_mesh_hook - col data float (to be skipped)", col.data_type, coldata)
            colname_to_add = colname_to_remove + "_ASOBO_export_update"
            if colname_to_remove:
                print("gather_mesh_hook - col to remove/add", colname_to_remove, colname_to_add)
                colattr = blender_mesh.color_attributes.new(name=colname_to_add, type='FLOAT_COLOR', domain='CORNER',)
                print("gather_mesh_hook - loop and add new color attribute data", colname_to_add)
                print("gather_mesh_hook - range", len(col.data))
                for v_index in range(len(col.data)):
                    #print("gather_mesh_hook - color", col.data[v_index].bytecolorattribute.bytecolorattributevalue.color)
                    print("gather_mesh_hook - color", col.data[v_index].color)
                    colattr.data[v_index].color = col.data[v_index].color
                blender_mesh.color_attributes.remove(col)
        print("gather_mesh_hook - Done")
