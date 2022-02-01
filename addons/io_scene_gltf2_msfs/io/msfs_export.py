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

from .msfs_light import MSFSLight
from .msfs_gizmo import MSFSGizmo
from .msfs_material import MSFSMaterial

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

    def gather_gltf_hook(self, gltf2_plan, export_settings):
        for i, image in enumerate(gltf2_plan.images):
            image.uri =os.path.basename(image.uri)

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled == True:
            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if blender_object.type == 'LIGHT':
                MSFSLight.export(gltf2_object, blender_object)

    def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, skip_filter, material_names, export_settings):
        # Set gizmo objects extension
        MSFSGizmo.export(gltf2_mesh, blender_mesh)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        # Recursive function to filter children that are gizmos
        def get_children(node):
            children = []
            for child in node.children:
                blender_object = bpy.context.scene.objects.get(child.name)
                if blender_object:
                    if blender_object.type != "EMPTY" and blender_object.msfs_gizmo_type == "NONE":
                        child.children = get_children(child)
                        children.append(child)
            return children

        # Construct new node list with filtered children
        new_nodes = []
        for node in list(gltf2_scene.nodes.copy()):
            node.children = get_children(node)
            new_nodes.append(node)

        gltf2_scene.nodes = new_nodes

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if (self.properties.enabled == True and blender_material.msfs_material_mode != None):
            if blender_material.msfs_material_mode != 'NONE':
                if gltf2_material.extensions is None:
                    gltf2_material.extensions = {}
                if gltf2_material.extras is None:
                    gltf2_material.extras = {}

                MSFSMaterial.export(gltf2_material, blender_material, export_settings)