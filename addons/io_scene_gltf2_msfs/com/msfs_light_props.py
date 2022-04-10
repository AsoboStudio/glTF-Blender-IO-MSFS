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

import bpy

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class AsoboMacroLight:

    SerializedName = "ASOBO_macro_light"

    class Defaults:
        Color = [1.0, 1.0, 1.0]
        Intensity = 1.0
        ConeAngle = 90.0
        HasSymmetry = False
        FlashFrequency = 0.0
        FlashDuration = 0.2
        FlashPhase = 0.0
        RotationSpeed = 0.0
        Kelvin = 3600.0  # TODO: ????
        ActivationMode = "ALWAYS_ON"

    bpy.types.Object.msfs_light_color = bpy.props.FloatVectorProperty(
        name="Color",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=3,
        default=Defaults.Color,  # TODO: update
        options=set(),  # ANIMATABLE is a default item in options, so for properties that shouldn't be animatable, we have to overwrite this.
    )
    bpy.types.Object.msfs_light_intensity = bpy.props.FloatProperty(
        name="Intensity",
        min=0.0,
        max=10000000.0,
        default=Defaults.Intensity,
        options=set(),
    )
    bpy.types.Object.msfs_light_cone_angle = bpy.props.FloatProperty(
        name="Cone Angle",
        min=0.0,
        max=360.0,
        default=Defaults.ConeAngle,
        options=set(),
    )
    bpy.types.Object.msfs_light_has_symmetry = bpy.props.BoolProperty(
        name="Has Symmetry",
        default=Defaults.HasSymmetry,
        options=set(),
    )
    bpy.types.Object.msfs_light_flash_frequency = bpy.props.FloatProperty(
        name="Flash Frequency",
        description="Flashes per minute",
        min=0.0,
        max=1000.0,
        default=Defaults.FlashFrequency,
        options=set(),
    )
    bpy.types.Object.msfs_light_flash_duration = bpy.props.FloatProperty(
        name="Flash Duration",
        description="Flash duration in seconds",
        min=0.0,
        max=1000.0,
        default=Defaults.FlashDuration,
        options=set(),
    )
    bpy.types.Object.msfs_light_flash_phase = bpy.props.FloatProperty(
        name="Flash Phase",
        description="Flash phase in seconds",
        min=0.0,
        max=1000.0,
        default=Defaults.FlashPhase,
        options=set(),
    )
    bpy.types.Object.msfs_light_rotation_speed = bpy.props.FloatProperty(
        name="Rotation Speed",
        description="Rotations per minute",
        min=-1000.0,
        max=1000.0,
        default=Defaults.RotationSpeed,
        options=set(),
    )
    bpy.types.Object.msfs_light_activation_mode = bpy.props.EnumProperty(
        name="Activation Mode",
        items=(
            ("DAY_NIGHT_CYCLE", "Day/Night Cycle", ""),
            ("ALWAYS_ON", "Always On", ""),
        ),
        default=Defaults.ActivationMode,
    )

    @staticmethod
    def from_dict(blender_object, gltf2_node, import_settings):
        extensions = gltf2_node.extensions
        if extensions is None:
            return

        assert isinstance(extensions, dict)
        extension = extensions.get(AsoboMacroLight.SerializedName)
        if extension is None:
            return

        if extension.get("color"):
            blender_object.msfs_light_color = extension.get("color")
        if extension.get("intensity"):
            blender_object.msfs_light_intensity = extension.get("intensity")
        if extension.get("coneAngle"):
            blender_object.msfs_light_cone_angle = extension.get("coneAngle")
        if extension.get("hasSimmetry"):  # This is spelled incorrectly on purpose
            blender_object.msfs_light_has_symmetry = extension.get("hasSimmetry")
        if extension.get("flashFrequency"):
            blender_object.msfs_light_flash_frequency = extension.get("flashFrequency")
        if extension.get("dayNightCycle"):
            blender_object.msfs_light_activation_mode = "DAY_NIGHT_CYCLE"
        if extension.get("flashDuration"):
            blender_object.msfs_light_flash_duration = extension.get("flashDuration")
        if extension.get("flashPhase"):
            blender_object.msfs_light_flash_phase = extension.get("flashPhase")
        if extension.get("rotationSpeed"):
            blender_object.msfs_light_rotation_speed = extension.get("rotationSpeed")

    @staticmethod
    def to_extension(blender_object, gltf2_node, export_settings):
        result = {}
        if blender_object.type == "LIGHT":
            result["color"] = blender_object.msfs_light_color
            result["intensity"] = blender_object.msfs_light_intensity
            result["coneAngle"] = blender_object.msfs_light_cone_angle
            result["hasSimmetry"] = blender_object.msfs_light_has_symmetry  # This is spelled incorrectly on purpose
            result["flashFrequency"] = blender_object.msfs_light_flash_frequency
            result["dayNightCycle"] = (blender_object.msfs_light_activation_mode == "DAY_NIGHT_CYCLE")  # TODO: is this right?
            result["flashDuration"] = blender_object.msfs_light_flash_duration
            result["flashPhase"] = blender_object.msfs_light_flash_phase
            result["rotationSpeed"] = blender_object.msfs_light_rotation_speed

            gltf2_node.extensions[AsoboMacroLight.SerializedName] = Extension(
                name=AsoboMacroLight.SerializedName,
                extension=result,
                required=False,
            )
