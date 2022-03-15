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
import numpy as np

from io_scene_gltf2.io.imp.gltf2_io_binary import BinaryData
from io_scene_gltf2.blender.imp.gltf2_blender_animation_utils import (
    make_fcurve,
    simulate_stash,
)
from io_scene_gltf2.blender.exp import gltf2_blender_gather_animation_channels
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class MSFSMaterialAnimationTarget:
    """
    Utility class to help us set the final material animation target. We lose these values during the export process, as the data path needs to be
    set to 'value' during export in order to get the Khronos exporter to pick up on the animation. The reference to the material is important to
    find the final glTF material, and channels is used to restore the original data path at the end of export.

    :param material: a blender material
    :param data_path: string value that contains the prop name
    :param channels: list of blender fcurves in order for us to restore data path after export
    """

    def __init__(self, material, data_path, channels):
        self.material = material
        self.data_path = data_path
        self.channels = channels


class MSFSMaterialAnimation:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_property_animation"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def create(import_settings):
        # NLA tracks are added bottom to top, so create animations in reverse so the first winds up on top
        for gltf2_animation in reversed(import_settings.data.animations):
            import_settings.action_cache = {}
            import_settings.needs_stash = []

            if gltf2_animation.extensions is None:
                return

            extension = gltf2_animation.extensions.get(
                MSFSMaterialAnimation.extension_name
            )
            if extension is None:
                return

            for channel in extension.get("channels"):
                sampler = channel.get("sampler")
                target = channel.get("target")

                material_idx = int(
                    target.split("/")[1]
                )  # The target will look something like "materials/INDEX/PROPERTY", so we use this to get the material index
                path = target.replace(
                    f"materials/{material_idx}/", ""
                )  # Get the actual path from the target - we have to remove the "materials/INDEX/" prefix from the path to get the path

                action = MSFSMaterialAnimation.get_or_create_action(
                    import_settings, material_idx, gltf2_animation.track_name
                )

                keys = BinaryData.get_data_from_accessor(
                    import_settings, gltf2_animation.samplers[sampler].input
                )
                values = BinaryData.get_data_from_accessor(
                    import_settings, gltf2_animation.samplers[sampler].output
                )

                if gltf2_animation.samplers[sampler].interpolation == "CUBICSPLINE":
                    values = values[1::3]

                blender_path = None
                group_name = None
                num_components = 0
                if path == "pbrMetallicRoughness/baseColorFactor":
                    blender_path = "msfs_base_color_factor"
                    group_name = "Base Color"
                    num_components = 4
                elif path == "emissiveFactor":
                    blender_path = "msfs_emissive_factor"
                    group_name = "Emissive Color"
                    num_components = 3
                elif path == "pbrMetallicRoughness/metallicFactor":
                    blender_path = "msfs_metallic_factor"
                    group_name = "Metallic Factor"
                    num_components = 1
                elif path == "pbrMetallicRoughness/roughnessFactor":
                    blender_path = "msfs_roughness_factor"
                    group_name = "Roughness Factor"
                    num_components = 1
                elif path == "extensions/ASOBO_material_UV_options/UVOffsetU":
                    blender_path = "msfs_uv_offset_u"
                    group_name = "UV Offset U"
                    num_components = 1
                elif path == "extensions/ASOBO_material_UV_options/UVOffsetV":
                    blender_path = "msfs_uv_offset_v"
                    group_name = "UV Offset V"
                    num_components = 1
                elif path == "extensions/ASOBO_material_UV_options/UVTilingU":
                    blender_path = "msfs_uv_tiling_u"
                    group_name = "UV Tiling U"
                    num_components = 1
                elif path == "extensions/ASOBO_material_UV_options/UVTilingV":
                    blender_path = "msfs_uv_tiling_v"
                    group_name = "UV Tiling V"
                    num_components = 1
                elif path == "extensions/ASOBO_material_UV_options/UVRotation":
                    blender_path = "msfs_uv_rotation"
                    group_name = "UV Rotation"
                    num_components = 1
                elif path == "extensions/ASOBO_material_windshield_v2/wiper1State":
                    blender_path = "msfs_wiper_1_state"
                    group_name = "Wiper 1 State"
                    num_components = 1
                elif path == "extensions/ASOBO_material_windshield_v2/wiper2State":
                    blender_path = "msfs_wiper_2_state"
                    group_name = "Wiper 2 State"
                    num_components = 1
                elif path == "extensions/ASOBO_material_windshield_v2/wiper3State":
                    blender_path = "msfs_wiper_3_state"
                    group_name = "Wiper 3 State"
                    num_components = 1
                elif path == "extensions/ASOBO_material_windshield_v2/wiper4State":
                    blender_path = "msfs_wiper_4_state"
                    group_name = "Wiper 4 State"
                    num_components = 1

                # Group values by component size
                values = np.array_split(values, len(values) / num_components)

                # Create action
                fps = bpy.context.scene.render.fps

                coords = [0] * (2 * len(keys))
                coords[::2] = (key[0] * fps for key in keys)

                for i in range(0, num_components):
                    coords[1::2] = (vals[i] for vals in values)
                    make_fcurve(
                        action,
                        coords,
                        data_path=blender_path,
                        index=i,
                        group_name=group_name,
                        interpolation=gltf2_animation.samplers[sampler].interpolation,
                    )

            # Push all actions onto NLA tracks
            for (mat, action) in import_settings.needs_stash:
                simulate_stash(mat, gltf2_animation.track_name, action)

                # Unmute track TODO: not sure why it gets muted - look into this
                for track in mat.animation_data.nla_tracks:
                    if track.name == gltf2_animation.track_name:
                        track.mute = False

    @staticmethod
    def get_or_create_action(gltf, material_idx, anim_name):
        """
        IMPORT
        Utility function to create or get a blender action on a material. If the action already exists, we return instead of creating

        :param gltf: the glTF import plan
        :param material_idx: index of glTF material
        :param anim_name: name of animation we are importing
        """
        mat = gltf.data.materials[material_idx]
        mat_name = list(mat.blender_material.values())[
            0
        ]  # The blender_material dictionary will only have one key-value pair, so we can get the value of the first item, which will be the blender material name

        blender_mat = bpy.data.materials[mat_name]

        action = gltf.action_cache.get(mat_name)
        if not action:
            name = anim_name + "_" + mat_name
            action = bpy.data.actions.new(name)
            action.id_root = "MATERIAL"
            gltf.needs_stash.append((blender_mat, action))
            gltf.action_cache[mat_name] = action

        return action

    @staticmethod
    def get_material_from_action(blender_object, blender_action, export_settings):
        """
        EXPORT
        Utility function to return a blender material from an action, if the action is a material

        :param blender_object: the blender object that is being animated
        :param blender_action: the blender action that is being exported

        :return: a blender material, or None
        """
        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None:
                continue

            if material.animation_data is not None:
                if blender_action == material.animation_data.action:
                    return material
                elif (
                    export_settings["gltf_nla_strips"] is True
                ):  # Check if the animation is an NLA strip
                    for track in material.animation_data.nla_tracks:
                        non_muted_strips = [
                            strip
                            for strip in track.strips
                            if strip.action is not None and strip.mute is False
                        ]
                        if track.strips is None or len(non_muted_strips) != 1:
                            continue
                        for strip in non_muted_strips:
                            if blender_action == strip.action:
                                return material

    @staticmethod
    def gather_actions(
        blender_object, gathered_actions, export_settings
    ):
        """
        EXPORT
        Based off code in the Khronos glTF exporter. This looks through all the materials in the object and checks
        if there are any animations on them, and if so, add to the actions list.

        :param blender_object: the blender object that is being animated
        :param gathered_actions: list of blender actions already gathered
        :return: blender_actions, blender_tracks, action_on_type
        """
        blender_actions = []
        blender_tracks = {}
        action_on_type = {}

        # First step is to get a list of all material animation actions and NLA tracks (if used)
        if not (
            blender_object.type == "MESH"
            and blender_object.data is not None
            and len(blender_object.material_slots) > 0
        ):
            return blender_actions, blender_tracks, action_on_type

        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None or material.animation_data is None:
                continue

            if material.animation_data.action is not None and material.animation_data.action not in gathered_actions: # If more than one object shares this material, the action will get exported multiple times. We prevent that by checking if we've already gathered it
                blender_actions.append(material.animation_data.action)
                blender_tracks[material.animation_data.action.name] = None
                action_on_type[material.animation_data.action.name] = "MATERIAL"

            # Collect associated strips from NLA tracks
            if export_settings["gltf_nla_strips"] is True:
                for track in material.animation_data.nla_tracks:
                    # Multi-strip tracks do not export correctly yet (they need to be baked),
                    # so skip them for now and only write single-strip tracks.
                    non_muted_strips = [
                        strip
                        for strip in track.strips
                        if strip.action is not None and strip.mute is False
                    ]
                    if track.strips is None or len(non_muted_strips) != 1:
                        continue
                    for strip in non_muted_strips:
                        if strip.action not in gathered_actions:
                            blender_actions.append(strip.action)
                            blender_tracks[
                                strip.action.name
                            ] = (
                                track.name
                            )  # Always set after possible active action -> None will be overwrite
                            action_on_type[strip.action.name] = "MATERIAL"

        return blender_actions, blender_tracks, action_on_type

    @staticmethod
    def replace_channel_target(
        gltf2_animation_channel_target, channels, blender_object, export_settings
    ):
        """
        EXPORT
        Replace targets for channels that are material animations. We don't use the target object for material targets, instead we
        have a path to the material index and cooresponding property. Unfortunately, we don't have access to the finalized glTF material tree yet,
        so we need to temporarily keep a reference to the blender material and the value that is being animated. This is properly finalized later.

        :param gltf2_animation_channel_target: a glTF animation channel target
        :param channels: list of channel groups gathered by the Khronos exporter. This has the data_path that we're interested in.
        :param blender_object: the blender object that is being animated
        :param action_name: the name of the blender action being exported
        :return:
        """
        for channel in channels:
            blender_material = MSFSMaterialAnimation.get_material_from_action(
                blender_object, channel.id_data, export_settings
            )
            if not blender_material:
                continue

            gltf2_animation_channel_target.path = MSFSMaterialAnimationTarget(
                blender_material, channel.data_path, channels
            )

            # Temporarily set data path to value in order to force the Khronos exporter to gather keyframes. We undo this later in the export process
            channel.data_path = "value"

    @staticmethod
    def add_placeholder_channel(
        gltf2_animation, blender_action, blender_object, export_settings
    ):
        """
        EXPORT
        If we have a glTF animation with only material animations, we need to create a placeholder scale channel. Because we utilize the `extensions`
        attribute of the animation, the channels end up being empty, which is against the glTF spec. By using this fake scale channel, we bypass this issue.

        :param gltf2_animation: a glTF animation
        :param blender_action: the blender action that is being exported
        :param blender_object: the blender object that is being animated
        :param export_settings: dictionary of export settings provided by the Khronos exporter
        :return:
        """
        if not blender_action.fcurves:
            return

        for fcurve in blender_action.fcurves:
            material = MSFSMaterialAnimation.get_material_from_action(
                blender_object, blender_action, export_settings
            )

            if material is None:
                # If we actually find a property besides the material animations, we don't need a temp fcurve
                return

        # Create temp action and insert fake keyframes
        temp_action = bpy.data.actions.new(name="TempAction")

        fcurve = temp_action.fcurves.new(data_path="scale", index=0)
        fcurve.keyframe_points.add(1)

        # Collect temp channel and cleanup
        gltf2_animation.channels.extend(
            gltf2_blender_gather_animation_channels.gather_animation_channels(
                temp_action, blender_object, export_settings
            )
        )

        bpy.data.actions.remove(temp_action)

    @staticmethod
    def finalize_animation(gltf2_animation):
        """
        EXPORT
        After the glTF animation is done being gathered, we can move all material animated channels to the Asobo extension and remove it from `channels`.

        :param gltf2_animation: a glTF animation
        :return:
        """
        material_animation_channels = []
        for channel in list(gltf2_animation.channels):
            if not isinstance(channel.target.path, MSFSMaterialAnimationTarget):
                continue

            if type(channel.target.path.material) != bpy.types.Material:
                continue

            material_animation_channels.append(
                {"sampler": channel.sampler, "target": channel.target.path}
            )

            # Restore proper animation channel paths
            for blender_channel in channel.target.path.channels:
                blender_channel.data_path = channel.target.path.data_path

            gltf2_animation.channels.remove(channel)

        if material_animation_channels:
            gltf2_animation.extensions[
                MSFSMaterialAnimation.extension_name
            ] = Extension(
                name=MSFSMaterialAnimation.extension_name,
                extension={"channels": material_animation_channels},
                required=False,
            )

    @staticmethod
    def finalize_target(gltf2_animation, gltf2_plan):
        """
        EXPORT
        Now that we have the finalized material tree, we can properly set the animation channel targets to the proper index, and replace the temporary
        blender material reference.

        :param gltf2_animation: a glTF animation
        :param gltf2_plan: the finalized glTF data
        :return:
        """
        if not gltf2_animation.extensions:
            return

        if (
            MSFSMaterialAnimation.extension_name
            not in gltf2_animation.extensions.keys()
        ):
            return

        for channel in list(gltf2_animation.extensions[MSFSMaterialAnimation.extension_name][
            "channels"
        ]):
            material_index = None
            for j, material in enumerate(gltf2_plan.materials):
                if material.name == channel["target"].material.name:
                    material_index = j
                    break

            if material_index is None:
                continue

            target_property = channel["target"].data_path

            if target_property == "msfs_base_color_factor":
                channel[
                    "target"
                ] = f"materials/{material_index}/pbrMetallicRoughness/baseColorFactor"
            elif target_property == "msfs_emissive_factor":
                channel["target"] = f"materials/{material_index}/emissiveFactor"
            elif target_property == "msfs_metallic_factor":
                channel[
                    "target"
                ] = f"materials/{material_index}/pbrMetallicRoughness/metallicFactor"
            elif target_property == "msfs_roughness_factor":
                channel[
                    "target"
                ] = f"materials/{material_index}/pbrMetallicRoughness/roughnessFactor"
            elif target_property == "msfs_uv_offset_u":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetU"
            elif target_property == "msfs_uv_offset_v":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetV"
            elif target_property == "msfs_uv_tiling_u":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingU"
            elif target_property == "msfs_uv_tiling_v":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingV"
            elif target_property == "msfs_uv_rotation":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVRotation"
            elif target_property == "msfs_wiper_1_state":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper1State"
            elif target_property == "msfs_wiper_2_state":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper2State"
            elif target_property == "msfs_wiper_3_state":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper3State"
            elif target_property == "msfs_wiper_4_state":
                channel[
                    "target"
                ] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper4State"
            else:
                # If we somehow have a property animated that isn't supported, remove the channel
                gltf2_animation.extensions[MSFSMaterialAnimation.extension_name]["channels"].remove(channel)
