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
import math

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFSGizmo():
    bl_options = {"UNDO"}

    extension_name = "ASOBO_gizmo_object"

    def __new__(cls, *args, **kwargs):
            raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def export(gltf2_mesh, blender_mesh):
        gizmo_objects = []
        for object in bpy.context.scene.objects:
            if object.type == "MESH" and bpy.data.meshes[object.data.name] == blender_mesh:
                for child in object.children:
                    if child.type == 'EMPTY' and child.msfs_gizmo_type != "NONE":
                        gizmo_object = {}
                        gizmo_object["translation"] = list(child.location)
                        gizmo_object["type"] = child.msfs_gizmo_type

                        if child.msfs_gizmo_type == "sphere":
                            gizmo_object["params"] = {
                                "radius": abs(child.scale.x * child.scale.y * child.scale.z)
                            }
                        elif child.msfs_gizmo_type == "box":
                            gizmo_object["params"] = {
                                "length": abs(child.scale.x),
                                "width": abs(child.scale.y),
                                "height": abs(child.scale.z)
                            }
                        elif child.msfs_gizmo_type == "cylinder":
                            gizmo_object["params"] = {
                                "radius": abs(child.scale.x * child.scale.y),
                                "height": abs(child.scale.z)
                            }

                        tags = ["Collision"]
                        if child.msfs_collision_is_road_collider:
                            tags.append("Road")

                        gizmo_object["extensions"] = {
                            "ASOBO_tags": Extension(
                                name = "ASOBO_tags",
                                extension = {
                                    "tags": tags
                                },
                                required = False
                            )
                        }
                        gizmo_objects.append(gizmo_object)

        if gizmo_objects:
            gltf2_mesh.extensions[MSFSGizmo.extension_name] = Extension(
                name = MSFSGizmo.extension_name,
                extension = {
                    "gizmo_objects": gizmo_objects
                },
                required = False
            )