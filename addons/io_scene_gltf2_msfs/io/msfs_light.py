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

import math

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
from mathutils import Matrix, Quaternion, Euler

class MSFSLight:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_macro_light"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf2_node, blender_node, blender_light, import_settings):
        parent_light = import_settings.data.nodes[
            gltf2_node.parent]  # The glTF exporter creates the actual light as a child of the node that has the Asobo extension
        if parent_light.extensions:
            extension = parent_light.extensions.get(MSFSLight.extension_name)
            if extension:
                # Set Blender light properties
                blender_light.color = extension.get("color")
                blender_light.energy = extension.get("intensity")
                if blender_light.type == "SPOT":
                    blender_light.spot_size = extension.get("cone_angle")

                # Set MSFS light properties
                blender_node.msfs_light_has_symmetry = extension.get("has_symmetry")
                blender_node.msfs_light_flash_frequency = extension.get("flash_frequency")
                blender_node.msfs_light_flash_duration = extension.get("flash_duration")
                blender_node.msfs_light_flash_phase = extension.get("flash_phase")
                blender_node.msfs_light_rotation_speed = extension.get("rotation_speed")
                blender_node.msfs_light_day_night_cycle = extension.get("day_night_cycle")

    @staticmethod
    def export(gltf2_object, blender_object):
        # First, clear all KHR_lights_punctual extensions from children. TODO: remove children?
        for child in gltf2_object.children:
            if child.extensions and child.extensions.get("KHR_lights_punctual"):
                child.extensions.pop("KHR_lights_punctual")

        angle = 360.0
        if blender_object.data.type == 'SPOT':
            angle = (180.0 / math.pi) * blender_object.data.spot_size

        extension = {}

        extension["color"] = list(blender_object.data.color)
        extension["intensity"] = blender_object.data.energy
        extension["cone_angle"] = angle
        extension["has_symmetry"] = blender_object.msfs_light_has_symmetry
        extension["flash_frequency"] = blender_object.msfs_light_flash_frequency
        extension["flash_duration"] = blender_object.msfs_light_flash_duration
        extension["flash_phase"] = blender_object.msfs_light_flash_phase
        extension["rotation_speed"] = blender_object.msfs_light_rotation_speed
        extension["day_night_cycle"] = blender_object.msfs_light_day_night_cycle

        # start quick dirty fix to solve rotationn problem 
        # this can be removed after blender 3.2 goes out
        currentRotationQuat = Quaternion((gltf2_object.rotation[3],gltf2_object.rotation[0],gltf2_object.rotation[1],gltf2_object.rotation[2])) if gltf2_object.rotation  else Quaternion()
        quat_a = Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
        r =  currentRotationQuat @ quat_a
        gltf2_object.rotation = [r.x,r.y,r.z,r.w]
        #end quick fix
        gltf2_object.extensions[MSFSLight.extension_name] = Extension(
            name=MSFSLight.extension_name,
            extension=extension,
            required=False
        )