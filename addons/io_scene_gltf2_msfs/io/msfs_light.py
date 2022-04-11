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

from ..com import msfs_light_props as MSFSLightExtensions

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFSLight:
    bl_options = {"UNDO"}

    extensions = [
        MSFSLightExtensions.AsoboMacroLight
    ]

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(gltf2_node, blender_node, blender_light, import_settings): # TODO: clean up function params
        parent_light = import_settings.data.nodes[
            gltf2_node.parent]  # TODO: use blender_light?
        for extension in MSFSLight.extensions:
            extension.from_dict(blender_node, parent_light, import_settings)

    @staticmethod
    def export(gltf2_object, blender_object, export_settings):
        # First, clear all KHR_lights_punctual extensions from children. TODO: handle 3.2 differences
        for child in gltf2_object.children:
            if child.extensions and child.extensions.get("KHR_lights_punctual"):
                child.extensions.pop("KHR_lights_punctual")

        for extension in MSFSLight.extensions:
            extension.to_extension(blender_object, gltf2_object, export_settings)
