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

class MSFS_UniqueID:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_uniqueID"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf2_node, blender_node, import_settings):
        pass

    @staticmethod
    def export(gltf2_object, blender_object):
        extension = {}

        extension["id"] = blender_object.name

        gltf2_object.extensions[MSFS_UniqueID.extension_name] = Extension(
            name=MSFS_UniqueID.extension_name,
            extension=extension,
            required=False
        )