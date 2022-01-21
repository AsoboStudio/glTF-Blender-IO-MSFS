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
import math

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFSGizmo():
    bl_options = {"UNDO"}

    extension_name = "ASOBO_gizmo_object"

    def __new__(cls, *args, **kwargs):
            raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf_node, blender_object, import_settings):
        gltf_mesh = import_settings.data.meshes[gltf_node.mesh]
        if gltf_mesh.extensions:
            extension = gltf_mesh.extensions.get(MSFSGizmo.extension_name)
            if extension:
                for gizmo_object in extension.get("gizmo_objects"):
                    bpy.ops.object.empty_add()
                    gizmo = bpy.context.object

                    # Set gizmo location
                    gizmo.location = gizmo_object.get("translation")

                    # Set gizmo type and rename gizmo
                    type = gizmo_object.get("type")
                    gizmo.msfs_gizmo_type = type

                    if type == "sphere":
                        gizmo.name = "Sphere Collision"
                    elif type == "box":
                        gizmo.name = "Box Collision"
                    elif type == "cylinder":
                        gizmo.name = "Cylinder Collision"

                    # Get gizmo scale
                    params = gizmo_object.get("params", {})
                    if type == "sphere":
                        gizmo.scale[0] = params.get("radius")
                        gizmo.scale[1] = params.get("radius")
                        gizmo.scale[2] = params.get("radius")
                    elif type == "cylinder":
                        gizmo.scale[0] = params.get("radius")
                        gizmo.scale[1] = params.get("radius")
                        gizmo.scale[2] = params.get("height")

                    # Set road collider
                    if "Road" in gizmo_object.get("extensions", {}).get("ASOBO_tags", {}).get("tags"):
                        gizmo.msfs_collision_is_road_collider = True

                    gizmo.parent = blender_object

                    # Set collection
                    for collection in gizmo.users_collection:
                        collection.objects.unlink(gizmo)
                    blender_object.users_collection[0].objects.link(gizmo)


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