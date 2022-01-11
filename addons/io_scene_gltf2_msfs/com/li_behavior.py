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

from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty, EnumProperty, FloatVectorProperty, PointerProperty

class MSFS_codebase(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = "File", subtype='FILE_NAME', default = "")
    full_path: bpy.props.StringProperty(name = "Filepath", subtype='FILE_PATH', default = "")

bpy.utils.register_class(MSFS_codebase)

class MSFS_behavior(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = "name", default = "")
    source_file: bpy.props.StringProperty(name="in file", subtype='FILE_PATH', default="")
    anim_length: bpy.props.IntProperty(name="Length", default=0)

bpy.utils.register_class(MSFS_behavior)

class MSFS_LI_material():
    def update_codebase(self, context):
        context.scene.msfs_selected_behavior.clear()
        #avoid a warning message:
        if context.scene.msfs_active_codebase >= len(context.scene.msfs_codebase):
            context.scene.msfs_active_behavior = 0
            return

        # go through the list of behaviors and match the filename
        for behavior in context.scene.msfs_behavior:
            if behavior.source_file == context.scene.msfs_codebase[context.scene.msfs_active_codebase].full_path:
                item = context.scene.msfs_selected_behavior.add()
                item.name = behavior.name
                item.full_path = behavior.source_file
        context.scene.msfs_active_behavior = 0

    # Collection of all assigned XML behavior files
    bpy.types.Scene.msfs_codebase = bpy.props.CollectionProperty(type = MSFS_codebase)
    bpy.types.Scene.msfs_active_codebase = bpy.props.IntProperty(default=0,min=0,update=update_codebase)

    # Collection of all found behavior tags:
    bpy.types.Scene.msfs_behavior = bpy.props.CollectionProperty(type = MSFS_behavior)

    # Collection of all behavior tags contained in the selected XML file:
    bpy.types.Scene.msfs_selected_behavior = bpy.props.CollectionProperty(type = MSFS_behavior)
    bpy.types.Scene.msfs_active_behavior = bpy.props.IntProperty(default=0,min=0)
    #Start/End keyframe of the selected animation
    bpy.types.Scene.msfs_behavior_start = bpy.props.IntProperty(name="KF start",default=0,min=0)
    bpy.types.Scene.msfs_behavior_end = bpy.props.IntProperty(name="KF end",default=1,min=0)

    # To manually assign a behavior tag, this string property is being used:
    bpy.types.Scene.msfs_manual_behavior = bpy.props.StringProperty(name="Tag",default="")
    #Start/End keyframe of the selected animation
    bpy.types.Scene.msfs_manual_behavior_start = bpy.props.IntProperty(name="KF start",default=0,min=0)
    bpy.types.Scene.msfs_manual_behavior_end = bpy.props.IntProperty(name="KF end",default=1,min=0)




