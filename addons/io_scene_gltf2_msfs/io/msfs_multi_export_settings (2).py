# glTF-Blender-IO-MSFS
# Copyright 2018-2021 The glTF-Blender-IO authors
# Copyright 2022 The glTF-Blender-IO-MSFS authors
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


class MSFS_MultiExporterSettings(bpy.types.PropertyGroup):
    #### General Options
    ## keep original texture option Check
    export_keep_originals: bpy.props.BoolProperty(
        name="Keep original",
        description=(
            "Keep original textures files if possible. "
            "WARNING: if you use more than one texture, "
            "where pbr standard requires only one, only one texture will be used. "
            "This can lead to unexpected results"
        ),
        default=False,
    )
    ## Texture directory path
    export_texture_dir: bpy.props.StringProperty(
        name="Textures",
        description="Folder to place texture files in. Relative to the .gltf file",
        default="",
    )

    ## Copyright string UI
    export_copyright: bpy.props.StringProperty(
        name="Copyright",
        description="Legal rights and conditions for the model",
        default="",
    )
   
    ## Asobo Unique ID Check
    use_unique_id: bpy.props.BoolProperty(
        name='Use Asbob_unique_id Extension',
        description='use ASOBO_unique_id extension',
        default=True
    )
    
    #### Include Options
    ## Export Visible Only Check - TODO : See if this works
    use_visible: bpy.props.BoolProperty(
        name="Visible Objects", description="Export visible objects only", default=False
    )

    ## Export Renderable Objects Check
    use_renderable: bpy.props.BoolProperty(
        name="Renderable Objects",
        description="Export renderable objects only",
        default=False,
    )

    ## Export Active Collection Check
    use_active_collection: bpy.props.BoolProperty(
        name="Active Collection",
        description="Export objects in the active collection only",
        default=False,
    )
    
    ## Export Custom Propreties Check
    export_extras: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export custom properties as glTF extras",
        default=False,
    )
    
    ## Export Camera Check
    export_cameras: bpy.props.BoolProperty(
        name="Cameras", description="Export cameras", default=False
    )

    ## Export Punctual Lights Check
    export_lights: bpy.props.BoolProperty(
        name="Punctual Lights",
        description="Export directional, point, and spot lights. "
        'Uses "KHR_lights_punctual" glTF extension',
        default=False,
    )
        
    #### Transform Options
    ## Y Up Check
    export_yup: bpy.props.BoolProperty(
        name="+Y Up", description="Export using glTF convention, +Y up", default=True
    )

    #### Geometry options
    ## Export Apply Modifiers Check
    export_apply: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers (excluding Armatures) to mesh objects -"
        "WARNING: prevents exporting shape keys",
        default=False,
    )
    
    ## Export UVs Check
    export_texcoords: bpy.props.BoolProperty(
        name="UVs",
        description="Export UVs (texture coordinates) with meshes",
        default=True,
    )

    ## Export normals Check
    export_normals: bpy.props.BoolProperty(
        name="Normals", description="Export vertex normals with meshes", default=True
    )

    ## Export tangents Check
    export_tangents: bpy.props.BoolProperty(
        name="Tangents", description="Export vertex tangents with meshes", default=False
    )

    ## Export Vertex Colors Check
    export_colors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Export vertex colors with meshes",
        default=True,
    )
    
    ## Export Loose Edge Check
    use_mesh_edges: bpy.props.BoolProperty(
        name="Loose Edges",
        description=(
            "Export loose edges as lines, using the material from the first material slot"
        ),
        default=False,
    )
    
    ## Export Loose Points Check
    use_mesh_vertices: bpy.props.BoolProperty(
        name="Loose Points",
        description=(
            "Export loose points as glTF points, using the material from the first material slot"
        ),
        default=False,
    )
    
    ## Export materials option Check
    export_materials: bpy.props.EnumProperty(
        name="Materials",
        items=(
            ("EXPORT", "Export", "Export all materials used by included objects"),
            (
                "PLACEHOLDER",
                "Placeholder",
                "Do not export materials, but write multiple primitive groups per mesh, keeping material slot information",
            ),
            (
                "NONE",
                "No export",
                "Do not export materials, and combine mesh primitive groups, losing material slot information",
            ),
        ),
        description="Export materials ",
        default="EXPORT",
    )

    ## Export Image format UI (Auto/Jpeg/None)
    export_image_format: bpy.props.EnumProperty(
        name="Images",
        items=(
            (
                "AUTO",
                "Automatic",
                "Save PNGs as PNGs and JPEGs as JPEGs. " "If neither one, use PNG",
            ),
            (
                "JPEG",
                "JPEG Format (.jpg)",
                "Save images as JPEGs. (Images that need alpha are saved as PNGs though.) "
                "Be aware of a possible loss in quality",
            ),
            ("NONE", "None", "Don't export images"),
        ),
        description=(
            "Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web "
            "applications due to the smaller file size. Alternatively they can be omitted if they are not needed"
        ),
        default="AUTO",
    )

    #### Animation Options
    ## Use Current Frame Check
    export_current_frame: bpy.props.BoolProperty(
        name="Use Current Frame",
        description="Export the scene in the current animation frame",
        default=False,
    )
    
    ##* Export Animation Options Check
    export_animations: bpy.props.BoolProperty(
        name="Animations",
        description="Exports active actions and NLA tracks as glTF animations",
        default=True,
    )

    ## Limit to Playback Range Check
    export_frame_range: bpy.props.BoolProperty(
        name="Limit to Playback Range",
        description="Clips animations to selected playback range",
        default=True,
    )

    ## Sampling Rate Slider (1-120)
    export_frame_step: bpy.props.IntProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        default=1,
        min=1,
        max=120,
    )

    ## Always Sample Animations Check
    export_force_sampling: bpy.props.BoolProperty(
        name="Always Sample Animations",
        description="Apply sampling to all animations",
        default=True,
    )

    ## Group by NLA Track Check
    export_nla_strips: bpy.props.BoolProperty(
        name="Group by NLA Track",
        description=(
            "When on, multiple actions become part of the same glTF animation if "
            "they're pushed onto NLA tracks with the same name. "
            "When off, all the currently assigned actions become one glTF animation"
        ),
        default=True,
    )

    ## Optimize Animation Size Check
    optimize_animation_size: bpy.props.BoolProperty(
        name="Optimize Animation Size",
        description=(
            "Reduces exported filesize by removing duplicate keyframes"
            "Can cause problems with stepped animation"
        ),
        default=True,
    )
    
    ## Deformation Bones Only Check
    export_def_bones: bpy.props.BoolProperty(
        name="Export Deformation Bones Only",
        description="Export Deformation bones only (and needed bones for hierarchy)",
        default=False,
    )

    ##* Skinning Option Check
    export_skins: bpy.props.BoolProperty(
        name="Skinning", description="Export skinning (armature) data", default=True
    )

    ## Export All Bone Influences Check
    export_all_influences: bpy.props.BoolProperty(
        name="Include All Bone Influences",
        description="Allow >4 joint vertex influences. Models may appear incorrectly in many viewers",
        default=False,
    )

    export_displacement: bpy.props.BoolProperty(
        name="Displacement Textures (EXPERIMENTAL)",
        description="EXPERIMENTAL: Export displacement textures. "
        'Uses incomplete "KHR_materials_displacement" glTF extension',
        default=False,
    )
    


class MSFS_PT_export_main(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.prop(settings, "export_keep_originals")
        if settings.export_keep_originals is False:
            layout.prop(settings, "export_texture_dir", icon="FILE_FOLDER")

        layout.prop(settings, "export_copyright")
        layout.prop(settings, "use_unique_id")


class MSFS_PT_export_include(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Include"
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        col = layout.column(heading="Limit to", align=True)
        col.prop(settings, "use_visible")
        col.prop(settings, "use_renderable")
        col.prop(settings, "use_active_collection")

        col = layout.column(heading="Data", align=True)
        col.prop(settings, "export_extras")
        col.prop(settings, "export_cameras")
        col.prop(settings, "export_lights")
 
 
class MSFS_PT_export_transform(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Transform"
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.prop(settings, "export_yup")


class MSFS_PT_export_geometry(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Geometry"
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.prop(settings, "export_apply")
        layout.prop(settings, "export_texcoords")
        layout.prop(settings, "export_normals")
        col = layout.column()
        col.active = settings.export_normals
        col.prop(settings, "export_tangents")
        layout.prop(settings, "export_colors")

        col = layout.column()
        col.prop(settings, "use_mesh_edges")
        col.prop(settings, "use_mesh_vertices")

        layout.prop(settings, "export_materials")
        col = layout.column()
        col.active = settings.export_materials == "EXPORT"
        col.prop(settings, "export_image_format")


class MSFS_PT_export_animation(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Animation"
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.prop(settings, "export_current_frame")


class MSFS_PT_export_animation_export(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Animation"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.prop(settings, "export_animations", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.active = settings.export_animations

        layout.prop(settings, "export_frame_range")
        layout.prop(settings, "export_frame_step")
        layout.prop(settings, "export_force_sampling")
        layout.prop(settings, "export_nla_strips")
        layout.prop(settings, "optimize_animation_size")

        row = layout.row()
        row.active = settings.export_force_sampling
        row.prop(settings, "export_def_bones")
        if (
            settings.export_force_sampling is False
            and settings.export_def_bones is True
        ):
            layout.label(
                text="Export only deformation bones is not possible when not sampling animation"
            )


class MSFS_PT_export_animation_skinning(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Skinning"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.prop(settings, "export_skins", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.active = settings.export_skins
        layout.prop(settings, "export_all_influences")


def register():
    bpy.types.Scene.msfs_multi_exporter_settings = bpy.props.PointerProperty(
        type=MSFS_MultiExporterSettings
    )
