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

import os
import bpy

from .msfs_multi_export import MSFS_OT_MultiExportGLTF2


class MultiExporterPresetLayer(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(name="", type=bpy.types.Collection)
    enabled: bpy.props.BoolProperty(name="", default=False)
    expanded: bpy.props.BoolProperty(name="", default=True)


class MultiExporterPreset(bpy.types.PropertyGroup):
    def update_file_path(self, context):
        # Make sure file_path always ends in .gltf
        if os.path.basename(self.file_path):
            file_path = bpy.path.ensure_ext(
                os.path.splitext(self.file_path)[0],
                ".gltf",
            )
            if self.file_path != file_path:
                self.file_path = file_path
            else:
               self.name =  os.path.basename(self.file_path)
        elif not os.path.isfile(self.file_path):
            file_path = os.path.join(self.file_path, self.name + ".gltf")
            if self.file_path != file_path:
                self.file_path = file_path
            else:
               self.name =  os.path.splitext(os.path.basename(self.file_path))[0]

    def update_name(self, context):
        file_path = os.path.dirname(self.file_path) + "\\" + self.name
        file_path = bpy.path.ensure_ext(
                os.path.splitext(file_path)[0],
                ".gltf",
            )
        if(self.file_path != file_path):
            self.file_path = file_path
        else:
            self.name =  os.path.splitext(os.path.basename(self.file_path))[0]

    name: bpy.props.StringProperty(name="", default="", update=update_name)
    file_path: bpy.props.StringProperty(name="", default="", subtype="FILE_PATH", update=update_file_path)
    enabled: bpy.props.BoolProperty(name="", default=False)
    expanded: bpy.props.BoolProperty(name="", default=True)
    layers: bpy.props.CollectionProperty(type=MultiExporterPresetLayer)


class MSFS_OT_AddPreset(bpy.types.Operator):
    bl_idname = "msfs.multi_export_add_preset"
    bl_label = "Add preset"

    def execute(self, context):
        presets = bpy.context.scene.msfs_multi_exporter_presets
        preset = presets.add()
        preset.name = f"Preset {len(presets)}"
        preset.file_path = preset.name + ".gltf"

        return {"FINISHED"}


class MSFS_OT_RemovePreset(bpy.types.Operator):
    bl_idname = "msfs.multi_export_remove_preset"
    bl_label = "Remove preset"

    preset_index: bpy.props.IntProperty()

    def execute(self, context):
        presets = bpy.context.scene.msfs_multi_exporter_presets
        presets.remove(self.preset_index)

        return {"FINISHED"}


class MSFS_OT_EditLayers(bpy.types.Operator):
    bl_idname = "msfs.multi_export_edit_layers"
    bl_label = "Edit layers"

    preset_index: bpy.props.IntProperty()

    collection_tree = {}

    def execute(self, context):
        return {"FINISHED"}

    def getChildren(self, collection, children):
        children[collection] = {}
        for child in collection.children:
            children[collection] = self.getChildren(child, children[collection])
        return children

    def invoke(self, context, event):
        preset = bpy.context.scene.msfs_multi_exporter_presets[self.preset_index]

        for i, layer in enumerate(preset.layers):
            if not layer.collection in list(bpy.data.collections):
                preset.layers.remove(i)

        for collection in bpy.data.collections:
            if not collection in [layer.collection for layer in preset.layers]:
                layer = preset.layers.add()
                layer.collection = collection

        # Because it isn't really possible to define children in the layers, we have to generate a "tree" of collections with their children, and use that when rendering.
        self.collection_tree = self.getChildren(bpy.context.scene.collection, {})

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        preset = bpy.context.scene.msfs_multi_exporter_presets[self.preset_index]

        # Loop through our collection tree and draw layers with respect to children
        def drawTree(layout_item, tree):
            for i, (collection, children) in enumerate(tree.items()):
                for layer in preset.layers:
                    if layer.collection == collection:
                        box = layout_item.box()
                        row = box.row()
                        if layer.collection.children:
                            row.prop(
                                layer,
                                "expanded",
                                text=layer.collection.name,
                                icon="DOWNARROW_HLT"
                                if layer.expanded
                                else "RIGHTARROW",
                                icon_only=True,
                                emboss=False,
                            )
                            row.prop(layer, "enabled", text="Enabled")
                            if layer.expanded:
                                drawTree(box, children)
                        else:
                            row.label(text=layer.collection.name)
                            row.prop(layer, "enabled", text="Enabled")

                        break

        drawTree(layout, self.collection_tree[bpy.context.scene.collection])


class MSFS_PT_MultiExporterPresetsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "PRESETS"

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS_OT_AddPreset.bl_idname, text="Add Preset")

        presets = bpy.context.scene.msfs_multi_exporter_presets
        for i, preset in enumerate(presets):
            row = layout.row()
            box = row.box()
            box.prop(
                preset,
                "expanded",
                text=preset.name,
                icon="DOWNARROW_HLT" if preset.expanded else "RIGHTARROW",
                icon_only=True,
                emboss=False,
            )

            if preset.expanded:
                box.prop(preset, "enabled", text="Enabled")
                box.prop(preset, "name", text="Name")
                box.prop(preset, "file_path", text="Export Path")

                box.operator(
                    MSFS_OT_EditLayers.bl_idname, text="Edit Layers"
                ).preset_index = i

                box.operator(
                    MSFS_OT_RemovePreset.bl_idname, text="Remove"
                ).preset_index = i

        row = layout.row()
        row.operator(MSFS_OT_MultiExportGLTF2.bl_idname, text="Export")


def register():
    bpy.types.Scene.msfs_multi_exporter_presets = bpy.props.CollectionProperty(
        type=MultiExporterPreset
    )
