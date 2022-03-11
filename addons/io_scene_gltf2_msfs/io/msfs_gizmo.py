# glTF-Blender-IO-MSFS
# Copyright (C) 2021-2022 The glTF-Blender-IO-MSFS authors

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

from . import msfs_io_utilities

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFSGizmo:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_gizmo_object"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf2_node, blender_object, import_settings):
        gltf_mesh = import_settings.data.meshes[gltf2_node.mesh]
        if gltf_mesh.extensions:
            extension = gltf_mesh.extensions.get(MSFSGizmo.extension_name)
            if extension:
                for gizmo_object in extension.get("gizmo_objects"):
                    bpy.ops.object.empty_add()
                    gizmo = bpy.context.object

                    if gizmo_object.get("translation"):
                        gizmo.location = msfs_io_utilities.gltf_location_to_blender(
                            gizmo_object.get("translation")
                        )
                    if gizmo_object.get("rotation"):
                        gizmo.rotation_mode = "QUATERNION"
                        gizmo.rotation_quaternion = (
                            msfs_io_utilities.gltf_rotation_to_blender(
                                gizmo_object.get("rotation")
                            )
                        )

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
                    elif type == "box":
                        gizmo.scale[0] = params.get("length")
                        gizmo.scale[1] = params.get("width")
                        gizmo.scale[2] = params.get("height")
                    elif type == "cylinder":
                        gizmo.scale[0] = params.get("radius")
                        gizmo.scale[1] = params.get("radius")
                        gizmo.scale[2] = params.get("height")

                    # Set road collider
                    if "Road" in gizmo_object.get("extensions", {}).get(
                        "ASOBO_tags", {}
                    ).get("tags"):
                        gizmo.msfs_collision_is_road_collider = True

                    gizmo.parent = blender_object
                    gizmo.matrix_parent_inverse = blender_object.matrix_world.inverted()

                    # Set collection
                    for collection in gizmo.users_collection:
                        collection.objects.unlink(gizmo)
                    blender_object.users_collection[0].objects.link(gizmo)

    @staticmethod
    def export(gltf2_mesh, blender_mesh):
        gizmo_objects = []
        for object in bpy.context.scene.objects:
            if (
                object.type == "MESH"
                and bpy.data.meshes[object.data.name] == blender_mesh
            ):
                for child in object.children:
                    if child.type == "EMPTY" and child.msfs_gizmo_type != "NONE":
                        gizmo_object = {}
                        translation, rotation, scale = msfs_io_utilities.get_trs(child)
                        if translation:
                            gizmo_object["translation"] = translation
                        if rotation:
                            gizmo_object["rotation"] = rotation
                        gizmo_object["type"] = child.msfs_gizmo_type

                        if child.msfs_gizmo_type == "sphere":
                            gizmo_object["params"] = {
                                "radius": abs(scale[0] * scale[1] * scale[2])
                            }
                        elif child.msfs_gizmo_type == "box":
                            gizmo_object["params"] = {
                                "length": abs(scale[0]),
                                "width": abs(scale[1]),
                                "height": abs(scale[2]),
                            }
                        elif child.msfs_gizmo_type == "cylinder":
                            gizmo_object["params"] = {
                                "radius": abs(scale[0] * scale[1]),
                                "height": abs(scale[2]),
                            }

                        tags = ["Collision"]
                        if child.msfs_collision_is_road_collider:
                            tags.append("Road")

                        gizmo_object["extensions"] = {
                            "ASOBO_tags": Extension(
                                name="ASOBO_tags",
                                extension={"tags": tags},
                                required=False,
                            )
                        }
                        gizmo_objects.append(gizmo_object)

        if gizmo_objects:
            gltf2_mesh.extensions[MSFSGizmo.extension_name] = Extension(
                name=MSFSGizmo.extension_name,
                extension={"gizmo_objects": gizmo_objects},
                required=False,
            )
