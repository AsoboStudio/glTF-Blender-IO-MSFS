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


# Scene Properties
class MSFSMultiExporterProperties:
    bpy.types.Scene.msfs_multi_exporter_current_tab = bpy.props.EnumProperty(
        items=(
            ("OBJECTS", "Objects", ""),
            ("PRESETS", " Presets", ""),
            ("SETTINGS", "Settings", ""),
        ),
    )


# Operators
class MSFS_OT_MultiExportGLTF2(bpy.types.Operator):
    bl_idname = "export_scene.multi_export_gltf"
    bl_label = "Multi-Export glTF 2.0"

    @staticmethod
    def export(file_path):
        settings = bpy.context.scene.msfs_multi_exporter_settings

        bpy.ops.export_scene.gltf(
            export_format="GLTF_SEPARATE",
            use_selection=True,
            filepath=file_path,
            export_copyright=settings.export_copyright,
            export_image_format=settings.export_image_format,
            export_texture_dir=settings.export_texture_dir,
            export_keep_originals=settings.export_keep_originals,
            export_texcoords=settings.export_texcoords,
            export_normals=settings.export_normals,
            export_tangents=settings.export_tangents,
            export_materials=settings.export_materials,
            export_colors=settings.export_colors,
            use_mesh_edges=settings.use_mesh_edges,
            use_mesh_vertices=settings.use_mesh_vertices,
            export_cameras=settings.export_cameras,
            use_visible=settings.use_visible,
            use_renderable=settings.use_renderable,
            use_active_collection=settings.use_active_collection,
            export_extras=settings.export_extras,
            export_yup=settings.export_yup,
            export_apply=settings.export_apply,
            export_animations=settings.export_animations,
            export_frame_range=settings.export_frame_range,
            export_frame_step=settings.export_frame_step,
            export_force_sampling=settings.export_force_sampling,
            export_nla_strips=settings.export_nla_strips,
            export_def_bones=settings.export_def_bones,
            export_current_frame=settings.export_current_frame,
            export_skins=settings.export_skins,
            export_all_influences=settings.export_all_influences,
            export_lights=settings.export_lights,
            export_displacement=settings.export_displacement,
        )

    def execute(self, context):
        if context.scene.msfs_multi_exporter_current_tab == "OBJECTS":
            from .msfs_multi_export_objects import MSFS_LODGroupUtility

            lod_groups = context.scene.msfs_multi_exporter_lod_groups
            sort_by_collection = context.scene.multi_exporter_grouped_by_collections

            for lod_group in lod_groups:
                # Generate XML if needed
                if lod_group.generate_xml:
                    root = etree.Element(
                        "ModelInfo", guid="{" + str(uuid.uuid4()) + "}", version="1.1"
                    )
                    lods = etree.SubElement(root, "LODS")

                    lod_values = []

                    for lod in lod_group.lods:
                        if not MSFS_LODGroupUtility.lod_is_visible(context, lod):
                            continue

                        if lod.enabled:
                            lod_values.append(lod.lod_value)
                    lod_values = sorted(lod_values, reverse=True)

                    for lod_value in lod_values:
                        etree.SubElement(
                            lods,
                            "LOD",
                            minSize=str(lod_value),
                            ModelFile=os.path.splitext(lod.file_name)[0] + ".gltf",
                        )

                    if lod_values:
                        # Format XML
                        dom = xml.dom.minidom.parseString(etree.tostring(root))
                        xml_string = dom.toprettyxml(encoding="utf-8")

                        with open(
                            bpy.path.abspath(
                                os.path.join(
                                    lod_group.folder_name,
                                    lod_group.group_name + ".xml",
                                )
                            ),
                            "wb",
                        ) as f:
                            f.write(xml_string)
                            f.close()

                # Export glTF
                for lod in lod_group.lods:
                    if not MSFS_LODGroupUtility.lod_is_visible(context, lod):
                        continue

                    if lod.enabled:
                        # Use selected objects in order to specify what to export
                        for obj in bpy.context.selected_objects:
                            obj.select_set(False)

                        def select_recursive(obj):
                            if obj in list(bpy.context.window.view_layer.objects):
                                obj.select_set(True)
                                for child in obj.children:
                                    select_recursive(child)

                        if sort_by_collection:
                            for obj in lod.collection.all_objects:
                                obj.select_set(True)
                        else:
                            select_recursive(lod.object)

                        MSFS_OT_MultiExportGLTF2.export(
                            os.path.join(
                                bpy.path.abspath(lod_group.folder_name),
                                os.path.splitext(lod.file_name)[0],
                            )
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
                                if obj in list(bpy.context.window.view_layer.objects):
                                    obj.select_set(True)

                    MSFS_OT_MultiExportGLTF2.export(bpy.path.abspath(preset.file_path))

        return {"FINISHED"}


class MSFS_OT_ChangeTab(bpy.types.Operator):
    bl_idname = "msfs.multi_export_change_tab"
    bl_label = "Change tab"

    current_tab: bpy.types.Scene.msfs_multi_exporter_current_tab

    def execute(self, context):
        context.scene.msfs_multi_exporter_current_tab = self.current_tab
        return {"FINISHED"}


# Panels
class MSFS_PT_MultiExporter(bpy.types.Panel):
    bl_label = "Multi-Export glTF 2.0"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
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
        row.operator(
            MSFS_OT_ChangeTab.bl_idname,
            text="Objects",
            depress=(current_tab == "OBJECTS"),
        ).current_tab = "OBJECTS"
        row.operator(
            MSFS_OT_ChangeTab.bl_idname,
            text="Presets",
            depress=(current_tab == "PRESETS"),
        ).current_tab = "PRESETS"
        row.operator(
            MSFS_OT_ChangeTab.bl_idname,
            text="Settings",
            depress=(current_tab == "SETTINGS"),
        ).current_tab = "SETTINGS"


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
