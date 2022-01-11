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

class MSFS_OT_RemoveSelectedBehaviorFromObject(bpy.types.Operator):
    #Remove the selected tag from the selected object here

    bl_label = "Remove selected behavior"
    bl_idname = "msfs.behavior_remove_selected_from_object"

    def execute(self, context):
        #failsafes:
        if context.object.msfs_active_behavior >= len(context.object.msfs_behavior):
            self.report({'ERROR'},"Invalid behavior index.")
            return {'CANCELLED'}


        active = context.object.msfs_active_behavior
        behavior = context.object.msfs_behavior[context.object.msfs_active_behavior].name

        context.object.msfs_behavior.remove(active)

        if len(context.object.msfs_behavior) <= active:
            context.object.msfs_active_behavior = len(context.object.msfs_behavior)-1

        self.report({'INFO'},"Behavior %s removed from object."%behavior)
        
        return {'FINISHED'}   