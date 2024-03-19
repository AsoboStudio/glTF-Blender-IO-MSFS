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

    ## Remember export settings check
    will_save_settings: bpy.props.BoolProperty(
        name="Remember Export Settings",
        description="Store glTF export settings in the Blender project.",
        default=False
    )

    ## MSFS extensions Check
    def msfs_enable_msfs_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_settings
        settings = context.scene.msfs_multi_exporter_settings
        props.enable_msfs_extension = settings.enable_msfs_extension

    enable_msfs_extension: bpy.props.BoolProperty(
        name='Use Microsoft Flight Simulator Extensions',
        description='Enable Microsoft Flight Simulator Extensions',
        default=True,
        update=msfs_enable_msfs_extension_update
    )

    ## Asobo Unique ID Check
    def msfs_use_unique_id_extension_update(self, context):
        props = bpy.context.scene.msfs_exporter_settings
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
    use_selection: bpy.props.BoolProperty(
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
        description="Export custom properties as glTF extras. Must be disabled for export dedicated to Microsoft Flight Simulator",
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
        name="Normals", 
        description="Export vertex normals with meshes", 
        default=True
    )

    ## Export Tangents Check
    export_tangents: bpy.props.BoolProperty(
        name="Tangents", 
        description="Export vertex tangents with meshes", 
        default=False
    )

    ## Export Vertex Colors Check
    export_colors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Export vertex colors with meshes",
        default=True,
    )
    
    ## Export Attributes Colors Check
    export_attributes: bpy.props.BoolProperty(
        name='Attributes',
        description='Export Attributes (when starting with underscore)',
        default=False
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
    ## JPEG Quality
    export_jpeg_quality: bpy.props.IntProperty(
        name='JPEG quality',
        description='Quality of JPEG export',
        default=75,
        min=0,
        max=100
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

    ## Lighting Modes -> >= 3.6 
    export_import_convert_lighting_mode: bpy.props.EnumProperty(
        name='Lighting Mode',
        items=(
            ('SPEC', 'Standard', 'Physically-based glTF lighting units (cd, lx, nt)'),
            ('COMPAT', 'Unitless', 'Non-physical, unitless lighting. Useful when exposure controls are not available'),
            ('RAW', 'Raw (Deprecated)', 'Blender lighting strengths with no conversion'),
        ),
        description='Optional backwards compatibility for non-standard render engines. Applies to lights',# TODO: and emissive materials',
        default='SPEC'
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

    ## Animation mode export -> >= 3.6
    export_animation_mode: bpy.props.EnumProperty(
        name='Animation mode',
        items=(('ACTIONS', 'Actions',
        'Export actions (actives and on NLA tracks) as separate animations'),
        ('ACTIVE_ACTIONS', 'Active actions merged',
        'All the currently assigned actions become one glTF animation'),
        ('NLA_TRACKS', 'NLA Tracks',
        'Export individual NLA Tracks as separate animation'),
        ('SCENE', 'Scene',
        'Export baked scene as a single animation')
        ),
        description='Export Animation mode',
        default='ACTIONS'
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
    export_optimize_animation_size: bpy.props.BoolProperty(
        name="Optimize Animation Size",
        description=(
            "Reduces exported filesize by removing duplicate keyframes"
            "Can cause problems with stepped animation"
        ),
        default=True,
    )

    ## Optimize Animation Force keeping channels for bones Check -> >= 3.6
    export_optimize_animation_keep_anim_armature: bpy.props.BoolProperty(
        name='Force keeping channels for bones',
        description=(
            "if all keyframes are identical in a rig, "
            "force keeping the minimal animation. "
            "When off, all possible channels for "
            "the bones will be exported, even if empty "
            "(minimal animation, 2 keyframes)"
        ),
        default=False
    )

    ## Optimize Animation Force keeping channels for objects Check -> >= 3.6
    export_optimize_animation_keep_anim_object: bpy.props.BoolProperty(
        name='Force keeping channel for objects',
        description=(
            "If all keyframes are identical for object transformations, "
            "force keeping the minimal animation"
        ),
        default=False
    )

    ## Export negative frames check -> >= 3.6
    export_negative_frame: bpy.props.EnumProperty(
        name='Negative Frames',
        items=(('SLIDE', 'Slide',
        'Slide animation to start at frame 0'),
        ('CROP', 'Crop',
        'Keep only frames above frame 0'),
        ),
        description='Negative Frames are slid or cropped',
        default='SLIDE'
    )

    ## Set all glTF Animation starting at 0 check -> >= 3.6
    export_anim_slide_to_zero: bpy.props.BoolProperty(
        name='Set all glTF Animation starting at 0',
        description=(
            "Set all glTF animation starting at 0.0s. "
            "Can be useful for looping animations"
        ),
        default=False
    )

    ## Bake all objects animation check -> >= 3.6
    export_bake_animation: bpy.props.BoolProperty(
        name='Bake All Objects Animations',
        description=(
            "Force exporting animation on every object. "
            "Can be useful when using constraints or driver. "
            "Also useful when exporting only selection"
        ),
        default=False
    )

    ## Split animation by object when animation mode is set to scene check -> >= 3.6
    export_anim_scene_split_object: bpy.props.BoolProperty(
        name='Split Animation by Object',
        description=(
            "Export Scene as seen in Viewport, "
            "But split animation by Object"
        ),
        default=True
    )

    ## Export all armature actions check
    export_anim_single_armature: bpy.props.BoolProperty(
        name="Export all Armature Actions",
        description=(
            "Export all actions, bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=False
    )

    ## Reset pose bones between actions check -> >= 3.6
    export_reset_pose_bones: bpy.props.BoolProperty(
        name='Reset pose bones between actions',
        description=(
            "Reset pose bones between each action exported. "
            "This is needed when some bones are not keyed on some animations"
        ),
        default=True
    )

    ## Use rest position check -> >= 3.6
    export_rest_position_armature: bpy.props.BoolProperty(
        name='Use Rest Position Armature',
        description=(
            "Export armatures using rest position as joints' rest pose. "
            "When off, current frame pose is used as rest pose"
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

    ## Export shape key animation check -> >= 3.6
    export_morph_animation: bpy.props.BoolProperty(
        name='Shape Key Animations',
        description='Export shape keys animations (morph targets)',
        default=False
    )

    ## Reset shape keys between actions check -> >= 3.6
    export_morph_reset_sk_data: bpy.props.BoolProperty(
        name='Reset shape keys between actions',
        description=(
            "Reset shape keys between each action exported. "
            "This is needed when some SK channels are not keyed on some animations"
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

    ## Flatten Bones Check -> >= 3.6
    export_hierarchy_flatten_bones: bpy.props.BoolProperty(
        name='Flatten Bone Hierarchy',
        description='Flatten Bone Hierarchy. Useful in case of non decomposable transformation matrix',
        default=False
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
        layout.prop(settings, "will_save_settings")
        

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
        col1.prop(settings, "use_selection") ## To use the MultiExporter panel, it's important to have use selected to True
        col1.enabled = False
        col2 = layout.column(heading="Limit to", align=True)
        col2.prop(settings, "use_visible")
        col2.prop(settings, "use_renderable")
        col2.prop(settings, "use_active_collection")
        if (bpy.app.version >= (3, 3, 0)):
            col2.prop(settings, "use_active_scene")

        if (settings.enable_msfs_extension):
            col2 = layout.column(heading="", align=True)
            col2.prop(settings, "export_extras")
            col2.enabled = False
            col3 = layout.column(heading="Data", align=True)
            col3.prop(settings, "export_lights")
            col3.prop(settings, "export_cameras")
        else:
            col2 = layout.column(heading="Data", align=True)
            col2.prop(settings, "export_extras")
            col2.prop(settings, "export_lights")
            col2.prop(settings, "export_cameras")
 
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
    bl_label = "Mesh"
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
        if (bpy.app.version >= (3, 6, 0)):
            layout.prop(settings, "export_attributes")

        col = layout.column()
        col.prop(settings, "use_mesh_edges")
        col.prop(settings, "use_mesh_vertices")

class MSFS_PT_export_material(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Material"
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

        layout.prop(settings, "export_materials")
        col = layout.column()
        col.active = settings.export_materials == "EXPORT"
        col.prop(settings, "export_image_format")
        if (bpy.app.version >= (3, 6, 0)):
            col.prop(settings, "export_jpeg_quality")

class MSFS_PT_export_shapekeys(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Shape Keys"
    bl_parent_id = "MSFS_PT_MultiExporter"
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

class MSFS_PT_export_armature(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Armature"
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
        layout.active = settings.export_skins
        
        if (bpy.app.version >= (3, 6, 0)):
            layout.prop(settings, 'export_rest_position_armature')

        if (bpy.app.version >= (3, 3, 0)):
            row = layout.row()
            row.active = settings.export_force_sampling
            row.prop(settings, 'export_def_bones')
            if settings.export_force_sampling is False and settings.export_def_bones is True:
                layout.label(text="Export only deformation bones is not possible when not sampling animation")
            
            if (bpy.app.version >= (3, 6, 0)):
                layout.prop(settings, 'export_hierarchy_flatten_bones')

class MSFS_PT_export_skinning(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Skinning"
    bl_parent_id = "MSFS_PT_MultiExporter"
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

class MSFS_PT_export_Lighting(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Lighting"
    bl_parent_id = "MSFS_PT_MultiExporter"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            layout.prop(settings, "export_import_convert_lighting_mode")

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
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and \
            context.scene.msfs_multi_exporter_settings.export_draco_mesh_compression_enable

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

    def draw_header(self, context):
        settings = context.scene.msfs_multi_exporter_settings
        self.layout.prop(settings, "export_animations", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        settings = context.scene.msfs_multi_exporter_settings
        layout.active = settings.export_animations

        if (bpy.app.version >= (3, 6, 0)):
            layout.prop(settings, 'export_animation_mode')
            if settings.export_animation_mode == "ACTIVE_ACTIONS":
                layout.prop(settings, 'export_nla_strips_merged_animation_name')
            row = layout.row()
            row.active = settings.export_force_sampling and settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS']
            row.prop(settings, 'export_bake_animation')
            if settings.export_animation_mode == "SCENE":
                layout.prop(settings, 'export_anim_scene_split_object')
        else:
            layout.prop(settings, "export_current_frame")
            layout.prop(settings, "export_frame_range")
            layout.prop(settings, "export_frame_step")
            layout.prop(settings, "export_force_sampling")
            layout.prop(settings, "export_nla_strips")
            if settings.export_nla_strips is False and bpy.app.version >= (3, 3, 0):
                layout.prop(settings, 'export_nla_strips_merged_animation_name')
            layout.prop(settings, "export_optimize_animation_size")
            if (bpy.app.version >= (3, 3, 0)):
                layout.prop(settings, "export_anim_single_armature")
            else:
                layout.prop(settings, 'export_def_bones')


class MSFS_PT_export_animation_notes(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Notes"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0)) and \
            context.scene.msfs_multi_exporter_settings.export_animation_mode in ["NLA_TRACKS", "SCENE"]

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            if settings.export_animation_mode == "SCENE":
                layout.label(text="Scene mode uses full bake mode:")
                layout.label(text="- sampling is active")
                layout.label(text="- baking all objects is active")
                layout.label(text="- Using scene frame range")
            elif settings.export_animation_mode == "NLA_TRACKS":
                layout.label(text="Track mode uses full bake mode:")
                layout.label(text="- sampling is active")
                layout.label(text="- baking all objects is active")

class MSFS_PT_export_animation_ranges(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Rest & Ranges"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            layout.prop(settings, 'export_current_frame')
            row = layout.row()
            row.active = settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'NLA_TRACKS']
            row.prop(settings, 'export_frame_range')
            layout.prop(settings, 'export_anim_slide_to_zero')
            row = layout.row()
            row.active = settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'NLA_TRACKS']
            layout.prop(settings, 'export_negative_frame')

class MSFS_PT_export_animation_armature(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Armature"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            layout.active = settings.export_animations

            layout.prop(settings, 'export_anim_single_armature')
            layout.prop(settings, 'export_reset_pose_bones')

class MSFS_PT_export_animation_shapekeys(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Shapekeys Animation"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw_header(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            settings = context.scene.msfs_multi_exporter_settings
            self.layout.active = settings.export_animations and settings.export_morph
            self.layout.prop(settings, "export_morph_animation", text="")

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings

            layout.active = settings.export_animations
            layout.prop(settings, 'export_morph_reset_sk_data')

class MSFS_PT_export_animation_sampling(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Sampling Animations"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw_header(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            settings = context.scene.msfs_multi_exporter_settings
            self.layout.active = settings.export_animations and settings.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS']
            self.layout.prop(settings, "export_force_sampling", text="")

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            
            layout.active = settings.export_animations
            layout.prop(settings, 'export_frame_step')

class MSFS_PT_export_animation_optimize(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Optimize Animations"
    bl_parent_id = "MSFS_PT_export_animation"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.msfs_multi_exporter_current_tab == "SETTINGS" and (bpy.app.version >= (3, 6, 0))

    def draw(self, context):
        if (bpy.app.version >= (3, 6, 0)):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            settings = context.scene.msfs_multi_exporter_settings
            
            layout.active = settings.export_animations

            layout.prop(settings, 'export_optimize_animation_size')

            row = layout.row()
            row.prop(settings, 'export_optimize_animation_keep_anim_armature')

            row = layout.row()
            row.prop(settings, 'export_optimize_animation_keep_anim_object')
        
def register():
    bpy.types.Scene.msfs_multi_exporter_settings = bpy.props.PointerProperty(type=MSFS_MultiExporterSettings)
