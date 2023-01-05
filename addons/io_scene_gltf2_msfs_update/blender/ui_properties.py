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
import os

# from .func_properties import *

# class MSFS_UL_ObjectBehaviorListItem(bpy.types.UIList):
#     bl_idname = "MSFS_UL_object_behaviorListItem"
#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
#         split = layout.split(factor=0.65)
#         split.label(text=item.name)
#         split.label(text="(kf:%i-%i)"%(item.kf_start,item.kf_end))

class MSFS_PT_BoneProperties(bpy.types.Panel):
    bl_label = "MSFS Properties"
    bl_idname = "BONE_PT_msfs_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'
    
    def draw(self, context):
        layout = self.layout

        if context.mode != 'EDIT_ARMATURE':
            active_bone = context.active_bone
            box = layout.box()
            box.prop(active_bone,"msfs_override_unique_id")
            if active_bone.msfs_override_unique_id:
                box.prop(active_bone, "msfs_unique_id")


        box.label(text = "Behavior list", icon = 'ANIM')
        box.template_list('MSFS_UL_object_behaviorListItem', "", context.object, 'msfs_behavior', context.object, 'msfs_active_behavior')

        if len(context.object.msfs_behavior) > context.object.msfs_active_behavior:
            behavior = context.object.msfs_behavior[context.object.msfs_active_behavior]

            subbox=box.box()
            subbox.label(text=behavior.name,icon='OUTLINER_DATA_GP_LAYER')
            if behavior.source_file != "":
                subbox.label(text="XML: %s"%behavior.source_filename,icon='FILE')
            split=subbox.split(factor=0.75)
            split.label(text="Keyframes start: %i"%behavior.kf_start,icon='DECORATE_KEYFRAME')
            split.label(text="end: %i"%behavior.kf_end)
            subbox.operator('msfs.behavior_remove_selected_from_object',text="Remove selected behavior",icon='TRASH')

class MSFS_PT_ObjectProperties(bpy.types.Panel):
    bl_label = "MSFS Properties"
    bl_idname = "OBJECT_PT_msfs_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object.type
    
    def draw(self, context):
        layout = self.layout

        active_object = context.object

        box = layout.box()
        box.prop(active_object,"msfs_override_unique_id")
        if active_object.msfs_override_unique_id:
            box.prop(active_object, "msfs_unique_id")
            

        if active_object.type == 'LIGHT':
            box = layout.box()
            box.label(text = "MSFS Light Parameters", icon='LIGHT')
            box.prop(active_object, 'msfs_light_has_symmetry')
            box.prop(active_object, 'msfs_light_flash_frequency')
            box.prop(active_object, 'msfs_light_flash_duration')
            box.prop(active_object, 'msfs_light_flash_phase')
            box.prop(active_object, 'msfs_light_rotation_speed')
            box.prop(active_object, 'msfs_light_day_night_cycle')

        elif active_object.type == 'EMPTY':
            box = layout.box()
            box.label(text="MSFS Collision Parameters", icon='SHADING_BBOX')
            box.prop(active_object, "msfs_gizmo_type") # TODO: change to msfs_msfs_gizmo_type
            if active_object.msfs_gizmo_type != "NONE":
                box.prop(active_object, "msfs_collision_is_road_collider")
        
        


        #if bpy.context.active_object.type == 'ARMATURE':
        #    box=layout.box()
        #    box.label(text = "Behavior tags are stored in individual bones.", icon = 'ANIM')
        #else:
        #    box=layout.box()
        #    box.label(text = "Behavior list", icon = 'ANIM')
        #    box.template_list('OBJECTBEHAVIOR_UL_listItem', "", context.object, 'msfs_behavior', context.object, 'msfs_active_behavior')

        #    if len(context.object.msfs_behavior) > context.object.msfs_active_behavior:
        #        behavior = context.object.msfs_behavior[context.object.msfs_active_behavior]

        #        subbox=box.box()
        #        subbox.label(text=behavior.name,icon='OUTLINER_DATA_GP_LAYER')
        #        if behavior.source_file != "":
        #            subbox.label(text="XML: %s"%behavior.source_filename,icon='FILE')
        #        split=subbox.split(factor=0.75)
        #        split.label(text="Keyframes start: %i"%behavior.kf_start,icon='DECORATE_KEYFRAME')
        #        split.label(text="end: %i"%behavior.kf_end)
        #        subbox.operator('msfs.behavior_remove_selected_from_object',text="Remove selected behavior",icon='TRASH')



