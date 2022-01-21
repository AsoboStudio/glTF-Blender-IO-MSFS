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
from .msfs_light import MSFSLight
from .msfs_gizmo import MSFSGizmo
from .msfs_material import MSFSMaterial

class Import:

    def __init__(self):
        pass

    # Create lights
    def gather_import_light_after_hook(self, gltf_node, blender_node, blender_light, import_settings):
        MSFSLight.create(gltf_node, blender_node, blender_light, import_settings)

    # Create gizmos
    def gather_import_node_after_hook(self, vnode, gltf_node, blender_object, import_settings):
        MSFSGizmo.create(gltf_node, blender_object, import_settings)

    # Create materials
    def gather_import_material_after_hook(self, gltf_material, vertex_color, blender_mat, import_settings):
        MSFSMaterial.create(gltf_material, blender_mat, import_settings)