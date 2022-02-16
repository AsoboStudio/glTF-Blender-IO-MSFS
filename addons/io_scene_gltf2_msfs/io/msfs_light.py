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


class MSFSLight:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_macro_light"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def export(gltf2_object, blender_object):
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

        gltf2_object.extensions[MSFSLight.extension_name] = Extension(
            name=MSFSLight.extension_name,
            extension=extension,
            required=False
        )
