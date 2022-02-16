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

import os
import re
import bpy
import uuid
import xml.dom.minidom
import xml.etree.ElementTree as etree

# Property Groups
class MultiExporterObjectLOD(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(name="", type=bpy.types.Object)
    enabled: bpy.props.BoolProperty(name="", default=False)
    lod_value: bpy.props.IntProperty(name="", default=0, min=0, max=1000)
    flatten_on_export: bpy.props.BoolProperty(name="", default=False)
    keep_instances: bpy.props.BoolProperty(name="", default=False)
    file_name: bpy.props.StringProperty(name="", default="")

class MultiExporterObjectGroup(bpy.types.PropertyGroup):
    group_name: bpy.props.StringProperty(name="", default="")
    expanded: bpy.props.BoolProperty(name="", default=True)
    lods: bpy.props.CollectionProperty(type=MultiExporterObjectLOD)
    folder_name: bpy.props.StringProperty(name="", default="", subtype="DIR_PATH")
    generate_xml: bpy.props.BoolProperty(name="", default=True)

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

    name: bpy.props.StringProperty(name="", default="")
    file_path: bpy.props.StringProperty(name="", default="", subtype="FILE_PATH", update=update_file_path)
    enabled: bpy.props.BoolProperty(name="", default=False)
    expanded: bpy.props.BoolProperty(name="", default=True)
    layers: bpy.props.CollectionProperty(type=MultiExporterPresetLayer)

# Scene Properties
class MSFSMultiExporterProperties:
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(items=
            (("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", "")),
    )

# Operators
class MSFS_OT_MultiExportGLTF2(bpy.types.Operator):
    bl_idname = 'export_scene.multi_export_gltf'
    bl_label = 'Multi-Export glTF 2.0'

    def execute(self, context):
        if context.scene.msfs_multi_exporter_current_tab == "OBJECTS":
            object_groups = context.scene.msfs_multi_exporter_object_groups

            for object_group in object_groups:
                # Generate XML if needed
                if object_group.generate_xml:
                    root = etree.Element("ModelInfo", guid="{" + str(uuid.uuid4()) + "}", version="1.1")
                    lods = etree.SubElement(root, "LODS")

                    lod_values = []

                    for lod in object_group.lods:
                        if lod.enabled:
                            lod_values.append(lod.lod_value)

                    lod_values = sorted(lod_values, reverse=True)

                    for lod_value in lod_values:
                        etree.SubElement(lods, "LOD", minSize=str(lod_value), ModelFile=os.path.splitext(lod.file_name)[0] + ".gltf")

                    if lod_values:
                        # Format XML
                        dom = xml.dom.minidom.parseString(etree.tostring(root))
                        xml_string = dom.toprettyxml(encoding='utf-8')

                        with open(os.path.join(object_group.folder_name, object_group.group_name + ".xml"), 'wb') as f:
                            f.write(xml_string)
                            f.close()
                
                # Export glTF
                for lod in object_group.lods:
                    # Use selected objects in order to specify what to export
                    for obj in bpy.context.selected_objects:
                        obj.select_set(False)

                    def select_recursive(obj):
                        obj.select_set(True)
                        for child in obj.children:
                            select_recursive(child)

                    select_recursive(lod.object)

                    if lod.enabled:
                        bpy.ops.export_scene.gltf(
                            export_format="GLTF_SEPARATE",
                            export_selected=True,
                            filepath=os.path.join(object_group.folder_name, lod.file_name)
                        )

        elif context.scene.msfs_multi_exporter_current_tab == "PRESETS":
            presets = bpy.context.scene.msfs_multi_exporter_presets
            for preset in presets:
                if preset.enabled:
                    # Clear currently selected objects
                    for obj in bpy.context.selected_objects:
                        obj.select_set(False)

                    # Loop through all enabled layers and select all objects
                    for layer in preset.layers:
                        if layer.enabled:
                            for obj in layer.collection.all_objects:
                                obj.select_set(True)

                    bpy.ops.export_scene.gltf(
                        export_format="GLTF_SEPARATE",
                        export_selected=True,
                        filepath=os.path.join(preset.file_path)
                    )

        return {"FINISHED"}

class MSFS_OT_ReloadObjectGroups(bpy.types.Operator):
    bl_idname = "msfs.reload_object_groups"
    bl_label = "Reload object groups"

    def get_group_from_object_name(self, object_name):
        matches = re.findall("(?i)x\d_|_lod[0-9]+", object_name) # If an object starts with xN_ or ends with _LODN, treat as an LOD
        if matches:
            # Get base object group name from object
            for match in matches:
                filtered_string = object_name.replace(match, "")
            return filtered_string
        else:
            # If prefix or suffix isn't found, use the object name as the group
            return object_name

    def execute(self, context):
        object_groups = bpy.context.scene.msfs_multi_exporter_object_groups

        # Remove deleted objects and empty object groups
        for i, object_group in enumerate(object_groups):
            for j, lod in enumerate(object_group.lods):
                if not lod.object.name in bpy.context.scene.objects:
                    object_groups[i].lods.remove(j)

                # Make sure object still matches group name
                if not self.get_group_from_object_name(lod.object.name) == object_group.group_name:
                    object_groups[i].lods.remove(j)

            if len(object_group.lods) == 0:
                object_groups.remove(i)

        # Search all objects in scene to find object groups
        found_object_groups = {}
        for obj in bpy.context.scene.objects:
            if obj.parent is None: # Only search "root" objects
                group_name = self.get_group_from_object_name(obj.name)

                # Set object group or append
                if group_name in found_object_groups.keys():
                    found_object_groups[group_name].append(obj)
                else:
                    found_object_groups[group_name] = [obj]

        # Create object groups and LODs
        for _, (object_group_name, objects) in enumerate(found_object_groups.items()):
            # Check if object group already exists, and if it doesn't, create one
            if not object_group_name in [object_group.group_name for object_group in object_groups]:
                object_group = object_groups.add()
                object_group.group_name = object_group_name
            else:
                for object_group in object_groups:
                    if object_group.group_name == object_group_name:
                        break
            
            # Set all LODs in object group
            for obj in objects:
                # If the object is at the root level (no parent)
                if obj.parent is None:
                    if not obj in [lod.object for lod in object_group.lods]:
                        lod = object_group.lods.add()
                        lod.object = obj
                        lod.file_name = obj.name

        return {"FINISHED"}

class MSFS_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.types.Scene.msfs_multi_exporter_current_tab

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}

class MSFS_OT_AddPreset(bpy.types.Operator):
    bl_idname = "msfs.multi_export_add_preset"
    bl_label = "Add preset"

    def execute(self, context):
        presets = bpy.context.scene.msfs_multi_exporter_presets
        preset = presets.add()
        preset.name = f"Preset {len(presets)}"

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
                            row.prop(layer, "expanded", text=layer.collection.name,
                                        icon="DOWNARROW_HLT" if layer.expanded else "RIGHTARROW", icon_only=True, emboss=False)
                            row.prop(layer, "enabled", text="Enabled")
                            if layer.expanded:
                                drawTree(box, children)
                        else:
                            row.label(text=layer.collection.name)
                            row.prop(layer, "enabled", text="Enabled")

                        break

        drawTree(layout, self.collection_tree[bpy.context.scene.collection])

# Panels
class MSFS_PT_MultiExporter(bpy.types.Panel):
    bl_label = "Multi-Export glTF 2.0"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Multi-Export glTF 2.0"

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_exporter_properties.enabled

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        current_tab = context.scene.msfs_multi_exporter_current_tab

        row = layout.row(align=True)
        row.operator(MSFS_OT_ChangeTab.bl_idname, text="Objects",
                     depress=(current_tab == "OBJECTS")).current_tab = "OBJECTS"
        row.operator(MSFS_OT_ChangeTab.bl_idname, text="Presets",
                     depress=(current_tab == "PRESETS")).current_tab = "PRESETS"

class MSFS_PT_MultiExporterObjectsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "OBJECTS"

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS_OT_ReloadObjectGroups.bl_idname, text="Reload LODs")

        object_groups = context.scene.msfs_multi_exporter_object_groups

        total_lods = 0
        for object_group in object_groups:
            total_lods += len(object_group.lods)
        if total_lods == 0:
            box = layout.box()
            box.label(text="No LODs found in scene")
        else:
            for object_group in object_groups:
                row = layout.row()
                if len(object_group.lods) > 0:
                    box = row.box()
                    box.prop(object_group, "expanded", text=object_group.group_name,
                             icon="DOWNARROW_HLT" if object_group.expanded else "RIGHTARROW", icon_only=True, emboss=False)
                    if object_group.expanded:
                        box.prop(object_group, "generate_xml", text="Generate XML")
                        box.prop(object_group, "folder_name", text="Folder")

                        col = box.column()
                        for lod in object_group.lods:
                            row = col.row()
                            row.prop(lod, "enabled", text=lod.object.name)
                            subrow = row.column()
                            subrow.prop(lod, "lod_value", text="LOD Value")
                            # subrow.prop(lod, "flatten_on_export", text="Flatten on Export") # Disable these two options for now as there's not a great way to implement them
                            # subrow.prop(lod, "keep_instances", text="Keep Instances")
                            subrow.prop(lod, "file_name", text="File Name")

        row = layout.row(align=True)
        row.operator(MSFS_OT_MultiExportGLTF2.bl_idname, text="Export")

class MSFS_PT_MultiExporterPresetsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {'HIDE_HEADER'}

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
            box.prop(preset, "expanded", text=preset.name,
                        icon="DOWNARROW_HLT" if preset.expanded else "RIGHTARROW", icon_only=True, emboss=False)

            if preset.expanded:
                box.prop(preset, "enabled", text="Enabled")
                box.prop(preset, "name", text="Name")
                box.prop(preset, "file_path", text="Export Path")

                box.operator(MSFS_OT_EditLayers.bl_idname, text="Edit Layers").preset_index = i

                box.operator(MSFS_OT_RemovePreset.bl_idname, text="Remove").preset_index = i

        row = layout.row()
        row.operator(MSFS_OT_MultiExportGLTF2.bl_idname, text="Export")


def register():
    bpy.types.Scene.msfs_multi_exporter_object_groups = bpy.props.CollectionProperty(type=MultiExporterObjectGroup)
    bpy.types.Scene.msfs_multi_exporter_presets = bpy.props.CollectionProperty(type=MultiExporterPreset)

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(MSFS_PT_MultiExporter)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    try:
        bpy.utils.unregister_class(MSFS_PT_MultiExporter)
    except Exception:
        pass
