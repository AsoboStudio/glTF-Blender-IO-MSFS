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

class MSFS_attached_behavior(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = "behavior", default = "")
    source_file: bpy.props.StringProperty(name = "filepath", subtype='FILE_NAME', default = "")
    source_filename: bpy.props.StringProperty(name = "filename", subtype='FILE_NAME', default = "")
    kf_start: bpy.props.IntProperty(name = "kf_start", min=0,  default = 0)
    kf_end: bpy.props.IntProperty(name = "kf_end", min=0,  default = 1)

bpy.utils.register_class(MSFS_attached_behavior)

class MSFS_LI_object_properties():
    bpy.types.Object.msfs_behavior = bpy.props.CollectionProperty(type = MSFS_attached_behavior)
    bpy.types.Object.msfs_active_behavior = bpy.props.IntProperty(name="Active behavior",min=0,default=0)

    bpy.types.Object.msfs_override_unique_id = bpy.props.BoolProperty(name='Override Unique ID',default=False)
    bpy.types.Object.msfs_unique_id = bpy.props.StringProperty(name='ID',default="")
    bpy.types.Bone.msfs_override_unique_id = bpy.props.BoolProperty(name='Override Unique ID',default=False)
    bpy.types.Bone.msfs_unique_id = bpy.props.StringProperty(name='ID',default="")

    bpy.types.Object.msfs_light_has_symmetry = bpy.props.BoolProperty(name='Has symmetry',default=False)
    bpy.types.Object.msfs_light_flash_frequency = bpy.props.FloatProperty(name='Flash frequency',min=0.0,default=0.0)
    bpy.types.Object.msfs_light_flash_duration = bpy.props.FloatProperty(name='Flash duration',min=0.0,default=0.0)
    bpy.types.Object.msfs_light_flash_phase = bpy.props.FloatProperty(name='Flash phase',default=0.0)
    bpy.types.Object.msfs_light_rotation_speed = bpy.props.FloatProperty(name='Rotation speed',default=0.0)
    bpy.types.Object.msfs_light_day_night_cycle = bpy.props.BoolProperty(name='Day/Night cycle',default=False,description="Set this value to 'true' if you want the light to be visible at night only.")

    bpy.types.Object.msfs_collision_is_road_collider = bpy.props.BoolProperty(name="Road Collider", default=False)