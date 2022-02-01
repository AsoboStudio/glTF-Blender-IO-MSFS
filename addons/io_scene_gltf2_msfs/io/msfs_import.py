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