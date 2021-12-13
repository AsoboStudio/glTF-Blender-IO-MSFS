# Copyright 2021 The FlightSim-glTF-Blender-IO authors.
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
import inspect
import pkgutil
import importlib
from pathlib import Path

bl_info = {
    "name" : "Microsoft Flight Simulator glTF Extension",
    "author" : "Luca Pierabella, Wing42, pepperoni505, ronh991, tml1024, and others",
    "description" : "This toolkit prepares your 3D assets to be used for Microsoft Flight Simulator",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "File > Import-Export",
    "warning" : "This version of the addon is work-in-progress. Don't use it in your active development cycle, as it adds variables and objects to the scene that may cause issues further down the line.",
    "category" : "Import-Export",
    "tracker_url": "https://github.com/AsoboStudio/FlightSim-glTF-Blender-IO"
}

class ExtAsoboProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name='ASOBO extensions',
        description='ASOBO extension for glTF',
        default=True
        )

class GLTF_PT_AsoboExtensionPanel(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Enabled"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_location = "File > Export > glTF 2.0"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_ext_gltf"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Blender2MSFS Extensions",icon='TOOL_SETTINGS')

    def draw(self, context):
        props = bpy.context.scene.msfs_ExtAsoboProperties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.prop(props, 'enabled')


def recursive_module_search(path, root=""):
    for _, module_name, is_package in pkgutil.iter_modules([str(path)]):
        if is_package:
            yield from recursive_module_search(path / module_name, root + module_name)
        else:
            yield (root, module_name)

modules = []

# search all modules and find classes that inherit from bpy
for module_name in recursive_module_search(Path(__file__).parent):
    if module_name[1] in locals():
        modules.append(importlib.reload(locals()[module_name[1]]))
    else:
        modules.append(importlib.import_module("." + module_name[1], package=__package__ + "." + module_name[0]))

classes = []

for module in modules:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if module.__name__ in str(obj): # check if the class is in the same module
                if "bpy" in str(inspect.getmro(obj)[1]): # sort of a hacky way to check if the class inherits from bpy
                    classes.append(obj)

def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
    try:
        bpy.utils.register_class(ExtAsoboProperties)
    except Exception:
        pass
    bpy.types.Scene.msfs_ExtAsoboProperties = bpy.props.PointerProperty(type=ExtAsoboProperties)


def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel

def unregister():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_panel():
    try:
        bpy.utils.unregister_class(GLTF_PT_AsoboExtensionPanel)
    except Exception:
        pass