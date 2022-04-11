# glTF-Blender-IO-MSFS
# Copyright (C) 2020-2022 The glTF-Blender-IO-MSFS authors

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
import os

class MSFS_PT_ObjectProperties(bpy.types.Panel):
    bl_label = "MSFS Properties"
    bl_idname = "OBJECT_PT_msfs_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return (context.object.type == 'EMPTY')
    
    def draw(self, context):
        layout = self.layout

        active_object = context.object

        if active_object.type == 'EMPTY':
            box = layout.box()
            box.label(text="MSFS Collision Parameters", icon='SHADING_BBOX')
            box.prop(active_object, "msfs_gizmo_type")
            if active_object.msfs_gizmo_type != "NONE":
                box.prop(active_object, "msfs_collision_is_road_collider")