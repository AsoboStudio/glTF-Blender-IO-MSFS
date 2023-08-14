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
from .. import get_prefs

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

    # get the preferences set in add-on intall menu
    addonpreferences = get_prefs()
    texture_dir = ''
    copyright = ''
    print(addonpreferences)
    print("addon preferences - ", addonpreferences.export_texture_dir, addonpreferences.export_copyright)
    texture_dir = addonpreferences.export_texture_dir
    copyright = addonpreferences.export_copyright

    ## Texture directory path
    export_texture_dir: bpy.props.StringProperty(
        name="Textures",
        description="Folder to place texture files in. Relative to the .gltf file",
        default=texture_dir,
    )

    ## Copyright string UI
    export_copyright: bpy.props.StringProperty(
        name="Copyright",
        description="Legal rights and conditions for the model",
        default=copyright,
    )

    ## Remember export settings check
    remember_export_settings: bpy.props.BoolProperty(
        name="Remember Export Settings",
        description="Store glTF export settings in the Blender project.",
        default=False
    )

    #This code assumes your folder name is the name of your addon
    #It also assumes that this function is placed inside a .py file in the base folder

    ## MSFS extensions Check
    def msfs_enable_msfs_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_properties
        settings = context.scene.msfs_multi_exporter_settings
        props.enabled = settings.enable_msfs_extension

    enable_msfs_extension: bpy.props.BoolProperty(
        name='Use Microsoft Flight Simulator Extensions',
        description='Enable Microsoft Flight Simulator Extensions',
        default=True,
        update=msfs_enable_msfs_extension_update
    )

    ## Asobo Unique ID Check
    def msfs_use_unique_id_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_properties
        settings = context.scene.msfs_multi_exporter_settings
        props.use_unique_id = settings.use_unique_id
    
    use_unique_id: bpy.props.BoolProperty(
        name='Use ASOBO Unique ID Extension',
        description='Enable ASOBO Unique ID extension',
        default=True,
        update=msfs_use_unique_id_extension_update
    )
    
    #### Include Options
    ## Export Selected Only Check - TODO : See if this works
    use_selected: bpy.props.BoolProperty(
        name="Selected Objects", 
        description= (
            "Export selected objects only. "
            "Disabled for the use of the MultiExporter (Needs to be always checked)"
        ), 
        default=True
    )

    ## Export Visible Only Check - TODO : See if this works
    use_visible: bpy.props.BoolProperty(
        name="Visible Objects", 
        description="Export visible objects only", 
        default=False
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

    use_active_scene: bpy.props.BoolProperty(
        name="Active Scene",
        description="Export active scene only",
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
        name="Cameras", 
        description="Export cameras", 
        default=False
    )

    ## Export Punctual Lights Check
    export_lights: bpy.props.BoolProperty(
        name="Punctual Lights",
        description= (
            "Export directional, point, and spot lights. "
            "Uses 'KHR_lights_punctual' glTF extension"
        ),
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
        description=(
            "Apply modifiers (excluding Armatures) to mesh objects. "
            "WARNING: prevents exporting shape keys"
        ),
        default=False,
    )
    
    ## Export UVs Check
    export_texcoords: bpy.props.BoolProperty(
        name="UVs",
        description="Export UVs (texture coordinates) with meshes",
        default=True,
    )

    ## Export Normals Check
    export_normals: bpy.props.BoolProperty(
        name="Normals", description="Export vertex normals with meshes", default=True
    )

    ## Export Tangents Check
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

    ## Draco compression check 
    export_draco_mesh_compression_enable: bpy.props.BoolProperty(
        name='Draco mesh compression',
        description=(
            "Compress mesh using Draco. "
            "WARNING: Draco compression is not supported in Microsoft Flight Simulator"
        ),
        default=False
    )

    ## Draco compression level
    export_draco_mesh_compression_level: bpy.props.IntProperty(
        name='Compression level',
        description='Compression level (0 = most speed, 6 = most compression, higher values currently not supported)',
        default=6,
        min=0,
        max=10
    )

    ## Draco compression position quatization
    export_draco_position_quantization: bpy.props.IntProperty(
        name='Position quantization bits',
        description='Quantization bits for position values (0 = no quantization)',
        default=14,
        min=0,
        max=30
    )

    ## Draco compression normal quatization
    export_draco_normal_quantization: bpy.props.IntProperty(
        name='Normal quantization bits',
        description='Quantization bits for normal values (0 = no quantization)',
        default=10,
        min=0,
        max=30
    )

    ## Draco compression texture coordinate quatization
    export_draco_texcoord_quantization: bpy.props.IntProperty(
        name='Texcoord quantization bits',
        description='Quantization bits for texture coordinate values (0 = no quantization)',
        default=12,
        min=0,
        max=30
    )

    ## Draco compression vertex color quatization
    export_draco_color_quantization: bpy.props.IntProperty(
        name='Color quantization bits',
        description='Quantization bits for color values (0 = no quantization)',
        default=10,
        min=0,
        max=30
    )

    ## Draco compression generic quatization
    export_draco_generic_quantization: bpy.props.IntProperty(
        name='Generic quantization bits',
        description='Quantization bits for generic coordinate values like weights or joints (0 = no quantization)',
        default=12,
        min=0,
        max=30
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
        default=False,
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

    ## Export NLA strips merged animation name
    export_nla_strips_merged_animation_name: bpy.props.StringProperty(
        name='Merged Animation Name',
        description=(
            "Name of single glTF animation to be exported"
        ),
        default='Animation'
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

    ## Export all armature actions check
    export_all_armature_actions: bpy.props.BoolProperty(
        name="Export all Armature Actions",
        description=(
            "Export all actions, bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=True
    )

    ## Export Shape Keys check
    export_morph: bpy.props.BoolProperty(
        name='Shape Keys',
        description=(
            "Export shape keys (morph targets). "
            "WARNING: Morph targets ar not interpreated by Microsoft Flight Simulator."
        ),
        default=False
    )

    ## Export Shape Keys Normals check
    export_morph_normal: bpy.props.BoolProperty(
        name='Shape Key Normals',
        description=(
            "Export vertex normals with shape keys (morph targets). "
            "WARNING: Morph targets ar not interpreated by Microsoft Flight Simulator."
        ),
        default=False
    )

    ## Export Shape Keys Tangent check
    export_morph_tangent: bpy.props.BoolProperty(
        name='Shape Key Tangents',
        description=(
            "Export vertex tangents with shape keys (morph targets). "
            "WARNING: Morph targets ar not interpreated by Microsoft Flight Simulator."
        ),
        default=False
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

    ## Deformation Bones Only Check
    export_def_bones: bpy.props.BoolProperty(
        name="Export Deformation Bones Only",
        description="Export Deformation bones only (and needed bones for hierarchy)",
        default=False,
    )

    ## Export displacement Check (works with Blender < 3.3 versions)
    export_displacement: bpy.props.BoolProperty(
        name="Displacement Textures (EXPERIMENTAL)",
        description=(
            "EXPERIMENTAL: Export displacement textures. "
            "Uses incomplete "'KHR_materials_displacement'" glTF extension. "
            "WARNING: works with Blender < 3.3 versions"
        ),
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
        layout.prop(settings, "remember_export_settings")
        

class MSFS_PT_MSFSExporterExtensionPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = ""
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Microsoft Flight Simulator Extensions", icon='TOOL_SETTINGS')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.prop(settings, 'enable_msfs_extension', text="Enabled")
        if settings.enable_msfs_extension:
            layout.prop(settings, 'use_unique_id', text="Enable ASOBO Unique ID extension")


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

        col1 = layout.column(heading="", align=True)
        col1.prop(settings, "use_selected") ## To use the MultiExporter panel, it's important to have use selected to True
        col1.enabled = False
        col2 = layout.column(heading="Limit to", align=True)
        col2.prop(settings, "use_visible")
        col2.prop(settings, "use_renderable")
        col2.prop(settings, "use_active_collection")
        col2.prop(settings, "use_active_scene")

        col2 = layout.column(heading="Data", align=True)
        col2.prop(settings, "export_extras")
        col2.prop(settings, "export_cameras")
        col2.prop(settings, "export_lights")
 
 
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

class MSFS_PT_export_geometry_compression(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Compression"
    bl_parent_id = "MSFS_PT_export_geometry"
    bl_options = {'DEFAULT_CLOSED'}

    def __init__(self):
        from io_scene_gltf2.io.com import gltf2_io_draco_compression_extension
        self.is_draco_available = gltf2_io_draco_compression_extension.dll_exists(quiet=True)

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.prop(settings, "export_draco_mesh_compression_enable", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.active = settings.export_draco_mesh_compression_enable
        layout.prop(settings, 'export_draco_mesh_compression_level')

        col = layout.column(align=True)
        col.prop(settings, 'export_draco_position_quantization', text="Quantize Position")
        col.prop(settings, 'export_draco_normal_quantization', text="Normal")
        col.prop(settings, 'export_draco_texcoord_quantization', text="Tex Coord")
        col.prop(settings, 'export_draco_color_quantization', text="Color")
        col.prop(settings, 'export_draco_generic_quantization', text="Generic")

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
        if settings.export_nla_strips is False:
            layout.prop(settings, 'export_nla_strips_merged_animation_name')
        layout.prop(settings, "optimize_animation_size")
        layout.prop(settings, "export_all_armature_actions")


class MSFS_PT_export_animation_shapekeys(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Shape Keys"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS"

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.prop(settings, "export_morph", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings

        layout.active = settings.export_morph

        layout.prop(settings, 'export_morph_normal')
        col = layout.column()
        col.active = settings.export_morph_normal
        col.prop(settings, 'export_morph_tangent')


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

        row = layout.row()
        row.active = settings.export_force_sampling
        row.prop(settings, 'export_def_bones')
        if settings.export_force_sampling is False and settings.export_def_bones is True:
            layout.label(text="Export only deformation bones is not possible when not sampling animation")


def register():
    bpy.types.Scene.msfs_multi_exporter_settings = bpy.props.PointerProperty(
        type=MSFS_MultiExporterSettings
    )
