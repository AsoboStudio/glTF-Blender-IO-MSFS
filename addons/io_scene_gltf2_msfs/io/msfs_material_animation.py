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

from io_scene_gltf2.blender.exp import gltf2_blender_gather_animation_channels
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

# TODO: somehow centralize all the functions - very hard to keep track of process order
class MSFSMaterialAnimation:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_property_animation"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def get_material_from_data_path(blender_object, blender_action, data_path, export_settings):
        """
        EXPORT
        Utility function to return a blender material from an action, if the action's target is a material

        :param blender_object: the blender object that is being animated
        :param blender_action: the blender action that is being exported
        :param data_path: the target path of the action

        :return: a blender material, or None
        """
        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None:
                continue

            if material.animation_data is not None:
                if blender_action == material.animation_data.action:
                    try: # Only return material if the target is on the material
                        material.path_resolve(data_path.split(".")[0])
                    except:
                        continue
                    else:
                        return material
                elif export_settings['gltf_nla_strips'] is True: # Check if the animation is an NLA strip
                    for track in material.animation_data.nla_tracks:
                        non_muted_strips = [strip for strip in track.strips if strip.action is not None and strip.mute is False]
                        if track.strips is None or len(non_muted_strips) != 1:
                            continue
                        for strip in non_muted_strips:
                            if blender_action == strip.action:
                                try: # Only return material if the target is on the material
                                    material.path_resolve(data_path.split(".")[0])
                                except:
                                    continue
                                else:
                                    return material

    @staticmethod
    def gather_actions(blender_object, blender_actions, blender_tracks, action_on_type, export_settings):
        """
        EXPORT
        Based off code in the Khronos glTF exporter. This looks through all the materials in the object and checks
        if there are any animations on them, and if so, add to the actions list.

        :param blender_object: the blender object that is being animated
        :param blender_actions: list of blender_actions affecting the object
        :param blender_tracks: dictionary of NLA tracks for the animation
        :param action_on_type: dictionary of animation type per action
        :return:
        """
        # First step is to get a list of all material animation actions and NLA tracks (if used)
        if not (blender_object.type == "MESH" and blender_object.data is not None
                    and len(blender_object.material_slots) > 0):
            return

        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None or material.animation_data is None:
                continue

            if material.animation_data.action is not None:
                blender_actions.append(material.animation_data.action)
                blender_tracks[material.animation_data.action.name] = None
                action_on_type[material.animation_data.action.name] = "MATERIAL"

            # Collect associated strips from NLA tracks
            if export_settings['gltf_nla_strips'] is True:
                for track in material.animation_data.nla_tracks:
                    # Multi-strip tracks do not export correctly yet (they need to be baked),
                    # so skip them for now and only write single-strip tracks.
                    non_muted_strips = [strip for strip in track.strips if strip.action is not None and strip.mute is False]
                    if track.strips is None or len(non_muted_strips) != 1:
                        continue
                    for strip in non_muted_strips:
                        blender_actions.append(strip.action)
                        blender_tracks[strip.action.name] = track.name # Always set after possible active action -> None will be overwrite
                        action_on_type[strip.action.name] = "MATERIAL"

    @staticmethod
    def replace_channel_target(gltf2_animation_channel, channels, blender_object, action_name, export_settings):
        """
        EXPORT
        Replace targets for channels that are material animations. We don't use the target object for material targets, instead we
        have a path to the material index and cooresponding property. Unfortunately, we don't have access to the finalized glTF material tree yet,
        so we need to temporarily keep a reference to the blender material and the value that is being animated. This is properly finalized later.

        :param gltf2_animation_channel: a glTF animation channel
        :param channels: list of channel groups gathered by the Khronos exporter. This has the data_path that we're interested in.
        :param blender_object: the blender object that is being animated
        :param action_name: the name of the blender action being exported
        :return:
        """
        for channel in channels:
            blender_material = MSFSMaterialAnimation.get_material_from_data_path(blender_object, bpy.data.actions[action_name], channel.data_path, export_settings)
            if not blender_material:
                continue

            gltf2_animation_channel.target = blender_material.path_resolve(channel.data_path.split(".")[0])

    @staticmethod
    def add_placeholder_channel(gltf2_animation, blender_action, blender_object, export_settings):
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
        for fcurve in blender_action.fcurves:
            material = MSFSMaterialAnimation.get_material_from_data_path(blender_object, blender_action, fcurve.data_path, export_settings)

            if material is None:
                # If we actually find a property besides the material animations, we don't need a temp fcurve
                return

        # Create temp action and insert fake keyframes
        temp_action = bpy.data.actions.new(name="TempAction")

        fcurve = temp_action.fcurves.new(data_path="scale", index=0)
        fcurve.keyframe_points.add(1)


        # Collect temp channel and cleanup
        gltf2_animation.channels.extend(
            gltf2_blender_gather_animation_channels.gather_animation_channels(temp_action, blender_object, export_settings)
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
        for i, channel in enumerate(gltf2_animation.channels):
            if not hasattr(channel.target, "id_data"):
                continue

            if type(channel.target.id_data) != bpy.types.Material:
                continue

            material_animation_channels.append({
                "sampler": channel.sampler,
                "target": channel.target 
            })
            gltf2_animation.channels.pop(i)

        if material_animation_channels:
            gltf2_animation.extensions[MSFSMaterialAnimation.extension_name] = Extension(
                name=MSFSMaterialAnimation.extension_name,
                extension={
                    "channels": material_animation_channels
                },
                required=False
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
        
        if MSFSMaterialAnimation.extension_name not in gltf2_animation.extensions.keys():
            return

        for channel in gltf2_animation.extensions[MSFSMaterialAnimation.extension_name]["channels"]:
            material_index = None
            for j, material in enumerate(gltf2_plan.materials):
                if material.name == channel["target"].id_data.name:
                    material_index = j
                    break
            
            if material_index is None:
                continue

            blender_material = channel["target"].id_data
            target_property = channel["target"].path_from_id().split(".")[0]

            if target_property == "msfs_color_albedo_mix":
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/baseColorFactor"
            elif target_property == "msfs_color_emissive_mix":
                channel["target"] = f"materials/{material_index}/emissiveFactor"
            elif target_property == "msfs_metallic_scale":
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/metallicFactor"
            elif target_property == "msfs_roughness_scale":
                channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/roughnessFactor"
            elif target_property == "msfs_uv_offset_u":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetU"
            elif target_property == "msfs_uv_offset_v":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetV"
            elif target_property == "msfs_uv_tiling_u":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingU"
            elif target_property == "msfs_uv_tiling_v":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingV"
            elif target_property == "msfs_uv_rotation":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVRotation"
            elif target_property == "msfs_wiper_1_state":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper1State"
            elif target_property == "msfs_wiper_2_state":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper2State"
            elif target_property == "msfs_wiper_3_state":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper3State"
            elif target_property == "msfs_wiper_4_state":
                channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_windshield_v2/wiper4State"