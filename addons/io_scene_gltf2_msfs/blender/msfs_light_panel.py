# glTF-Blender-IO-MSFS
# Copyright (C) 2022 The glTF-Blender-IO-MSFS authors

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


class MSFS_PT_Light(bpy.types.Panel):
    bl_label = "MSFS Light Params"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.active_object.type == "LIGHT"

    def draw(self, context):
        layout = self.layout

        obj = context.active_object

        if obj:  # TODO: migrate?
            layout.prop(obj, "msfs_light_color")
            layout.prop(obj, "msfs_light_intensity")
            layout.prop(obj, "msfs_light_cone_angle")
            layout.prop(obj, "msfs_light_has_symmetry")
            layout.prop(obj, "msfs_light_flash_frequency")
            layout.prop(obj, "msfs_light_flash_duration")
            layout.prop(obj, "msfs_light_flash_phase")
            layout.prop(obj, "msfs_light_rotation_speed")
            layout.prop(obj, "msfs_light_activation_mode")
