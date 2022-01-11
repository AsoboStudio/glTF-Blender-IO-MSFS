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

###################################################################################################
#
#   This file contains classes and functions to attach behaviors from an XML file to
#   objects of the scene.
#
###################################################################################################

import bpy
import os

from bpy_extras.io_utils import ImportHelper 
from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty, EnumProperty, FloatVectorProperty, PointerProperty

from .func_xml import parse_xml_behavior

class CodebaseAdd(bpy.types.Operator, ImportHelper):
    bl_label = "Add file"
    bl_idname = "msfs.codebase_add"

    filter_glob: StringProperty( default='*.xml', options={'HIDDEN'} )

    def execute(self,context):
        path, filename = os.path.split(self.filepath)

        #check if the file is already in the list and skip if it is:
        for file in context.scene.msfs_codebase:
            if file.full_path == self.filepath:
                msg="File already in codebase. Use reload if you want to reload the file."
                self.report({'ERROR'},msg)
                return{'FINISHED'}

        # Try to parse the file and populate the behavior list:
        appended_behaviors = parse_xml_behavior(self.filepath)

        if appended_behaviors == -1:
            self.report({'ERROR'}, "Couldn't parse the file <%s>."%self.filepath)
            return {'CANCELLED'}

        self.report({'INFO'}, "Appended %i new behaviors."%appended_behaviors)
        context.scene.msfs_active_codebase = 0
        
        item = bpy.context.scene.msfs_codebase.add()
        item.name = filename
        item.full_path = self.filepath

        return {'FINISHED'}
        
class CodebaseRemove(bpy.types.Operator):
    bl_label = "Remove file"
    bl_idname = "msfs.codebase_remove"

    def execute(self,context):
        #Some failsafes:
        if len(context.scene.msfs_codebase) < 1:
            self.report({'INFO'},"Codebase is empty. Nothing has been removed.")
            return{'CANCELLED'}
        if context.scene.msfs_active_codebase >= len(context.scene.msfs_codebase):
            self.report({'INFO'},"Please select the XML file you want to remove from the index.")
            return{'CANCELLED'}


        #let's first remove all behavior templates from the list:
        remove_behavior_list = []
        number_of_behavior_found = 0
        for behavior in context.scene.msfs_behavior:
            if behavior.source_file == context.scene.msfs_codebase[context.scene.msfs_active_codebase].full_path:
                number_of_behavior_found += 1
                remove_behavior_list.append(behavior)

        for element in remove_behavior_list:
            context.scene.msfs_behavior.remove(context.scene.msfs_behavior.find(element.name))
        
        self.report({'INFO'},"%i behaviors removed."%number_of_behavior_found)

        # Now, we can delete the entry in the codebase:
        context.scene.msfs_codebase.remove(context.scene.msfs_active_codebase)

        context.scene.msfs_active_codebase = 0

        return {'FINISHED'}

class ReloadBehaviorFile(bpy.types.Operator):
    bl_label = "Reload behavior"
    bl_idname = "msfs.reload_behavior_file"

    def execute(self, context):
        #Check that there's a file active:
        if len(context.scene.msfs_codebase) < 1:
            self.report({'INFO'},"Codebase is empty. Nothing has been reloaded.")
            return{'CANCELLED'}
        if context.scene.msfs_active_codebase >= len(context.scene.msfs_codebase):
            self.report({'INFO'},"Please select the XML file you want to reload.")
            return{'CANCELLED'}

        #The easiest way is toreload is to remove all of the related behaviors and then load the file again.
        filepath = context.scene.msfs_codebase[context.scene.msfs_active_codebase].full_path
        
        remove_behavior_list = []
        number_of_behavior_removed = 0
        for behavior in context.scene.msfs_behavior:
            if behavior.source_file == filepath:
                number_of_behavior_removed += 1
                remove_behavior_list.append(behavior)

        for element in remove_behavior_list:
            context.scene.msfs_behavior.remove(context.scene.msfs_behavior.find(element.name))
       
        #Now we can re-parse the file:
        appended_behaviors = parse_xml_behavior(filepath)

        if appended_behaviors == -1:
            self.report({'ERROR'}, "Couldn't parse the file <%s>."%filepath)
            return {'CANCELLED'}

        delta_behavior = appended_behaviors - number_of_behavior_removed
        if delta_behavior == 0:
            self.report({'INFO'}, "Reloaded behavior file. No new behaviors found.")
        elif delta_behavior < 0:
            self.report({'INFO'}, "Reloaded behavior file. %i behaviors have been removed."%delta_behavior)
        else:
            self.report({'INFO'}, "Reloaded behavior file. Found %i new behaviors."%delta_behavior)
        context.scene.msfs_active_codebase = 0

        
       
        print("Reloading behavior file.")
        return{'FINISHED'}


class AssignBehavior(bpy.types.Operator):
    #Assign the tag to the object here.
    
    bl_label = "Assign behavior"
    bl_idname = "msfs.behavior_assign"

    def execute(self, context):
        #check that the selection is valid:
        if context.scene.msfs_active_behavior >= len(context.scene.msfs_selected_behavior):
            self.report({'ERROR'},"Invalid behavior selection.")
            return {'CANCELLED'}


        for ob in bpy.context.selected_objects:
            #check if the tag already exists:
            found = False
            for behavior in ob.msfs_behavior:
                if behavior.name == context.scene.msfs_behavior[context.scene.msfs_active_behavior].name:
                    self.report({'INFO'},"The tag '%s' already exists in this object."%context.scene.msfs_behavior[context.scene.msfs_active_behavior].name)
                    found=True
                    
            if found == False:
                path, filename = os.path.split(context.scene.msfs_behavior[context.scene.msfs_active_behavior].source_file)

                behavior = ob.msfs_behavior.add()
                behavior.name = context.scene.msfs_behavior[context.scene.msfs_active_behavior].name
                behavior.source_file = context.scene.msfs_behavior[context.scene.msfs_active_behavior].source_file
                behavior.source_filename = filename
                behavior.kf_start = context.scene.msfs_behavior_start
                behavior.kf_end = context.scene.msfs_behavior_end

        self.report({'INFO'},"Behavior '%s' added to the selected object(s)."%context.scene.msfs_behavior[context.scene.msfs_active_behavior].name)
        return {'FINISHED'}       
     

class AssignManualBehavior(bpy.types.Operator):
    #Assign the tag to the object here.

    bl_label = "Manually assign a behavior"
    bl_idname = "msfs.behavior_assign_manually"

    def execute(self, context):
        #Check the string:
        if context.scene.msfs_manual_behavior == "":
            self.report({'ERROR'},"The behavior tag must not be empty.")
            return {'CANCELLED'}


        for ob in bpy.context.selected_objects:
            #check if the tag already exists:
            found = False
            for behavior in ob.msfs_behavior:
                if behavior.name == context.scene.msfs_manual_behavior:
                    self.report({'INFO'},"The tag '%s' already exists in this object."%context.scene.msfs_manual_behavior)
                    found=True

            if found == False:
                behavior = ob.msfs_behavior.add()
                behavior.name = context.scene.msfs_manual_behavior
                behavior.source_file = ""
                behavior.kf_start = context.scene.msfs_manual_behavior_start
                behavior.kf_end = context.scene.msfs_manual_behavior_end

        self.report({'INFO'},"Behavior '%s' added to the selected object(s)."%context.scene.msfs_manual_behavior)
        return {'FINISHED'}        



