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

import re
import os
import bpy

from .msfs_multi_export import MSFS_OT_MultiExportGLTF2


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


class MSFS_OT_ReloadObjectGroups(bpy.types.Operator):
    bl_idname = "msfs.reload_object_groups"
    bl_label = "Reload object groups"

    def get_group_from_object_name(self, object_name):
        matches = re.findall(
            "(?i)x[0-9]_|_lod[0-9]+", object_name
        )  # If an object starts with xN_ or ends with _LODN, treat as an LOD
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
                if (
                    not self.get_group_from_object_name(lod.object.name)
                    == object_group.group_name
                ):
                    object_groups[i].lods.remove(j)

            if len(object_group.lods) == 0:
                object_groups.remove(i)

        # Search all objects in scene to find object groups
        found_object_groups = {}
        for obj in bpy.context.scene.objects:
            if obj.parent is None:  # Only search "root" objects
                group_name = self.get_group_from_object_name(obj.name)

                # Set object group or append
                if group_name in found_object_groups.keys():
                    found_object_groups[group_name].append(obj)
                else:
                    found_object_groups[group_name] = [obj]

        # Create object groups and LODs
        for _, (object_group_name, objects) in enumerate(found_object_groups.items()):
            # Check if object group already exists, and if it doesn't, create one
            if not object_group_name in [
                object_group.group_name for object_group in object_groups
            ]:
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


class MSFS_PT_MultiExporterObjectsView(bpy.types.Panel):
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Multi-Export glTF 2.0"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "OBJECTS"

    def draw(self, context):
        layout = self.layout

        layout.operator(MSFS_OT_ReloadObjectGroups.bl_idname, text="Reload LODs")
        layout.prop(context.scene, "multi_exporter_show_hidden_objects")

        object_groups = context.scene.msfs_multi_exporter_object_groups

        total_lods = 0
        for object_group in object_groups:
            for lod in object_group.lods:
                if (
                    not context.scene.multi_exporter_show_hidden_objects
                    and lod.object.hide_get()
                ):
                    continue

                total_lods += 1

        if total_lods == 0:
            box = layout.box()
            box.label(text="No LODs found in scene")
        else:
            for object_group in object_groups:
                row = layout.row()
                if (
                    len(object_group.lods) == 1
                ):  # If we only have one LOD in the group, and it is hidden, then don't render the group
                    if (
                        not context.scene.multi_exporter_show_hidden_objects
                        and object_group.lods[0].object.hide_get()
                    ):
                        continue

                if len(object_group.lods) > 0:
                    box = row.box()
                    box.prop(
                        object_group,
                        "expanded",
                        text=object_group.group_name,
                        icon="DOWNARROW_HLT" if object_group.expanded else "RIGHTARROW",
                        icon_only=True,
                        emboss=False,
                    )
                    if object_group.expanded:
                        box.prop(object_group, "generate_xml", text="Generate XML")
                        box.prop(object_group, "folder_name", text="Folder")

                        col = box.column()
                        for lod in object_group.lods:
                            if (
                                not context.scene.multi_exporter_show_hidden_objects
                                and lod.object.hide_get()
                            ):
                                continue

                            row = col.row()
                            row.prop(lod, "enabled", text=lod.object.name)
                            subrow = row.column()
                            subrow.prop(lod, "lod_value", text="LOD Value")
                            # subrow.prop(lod, "flatten_on_export", text="Flatten on Export") # Disable these two options for now as there's not a great way to implement them
                            # subrow.prop(lod, "keep_instances", text="Keep Instances")
                            subrow.prop(lod, "file_name", text="File Name")

        row = layout.row(align=True)
        row.operator(MSFS_OT_MultiExportGLTF2.bl_idname, text="Export")


def register():
    bpy.types.Scene.msfs_multi_exporter_object_groups = bpy.props.CollectionProperty(
        type=MultiExporterObjectGroup
    )
