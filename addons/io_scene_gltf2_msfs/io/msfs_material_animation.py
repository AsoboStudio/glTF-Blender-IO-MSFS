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

from io_scene_gltf2.io.com import gltf2_io
from io_scene_gltf2.blender.exp import gltf2_blender_gather_animation_samplers
from io_scene_gltf2.blender.exp import gltf2_blender_gather_animation_channel_target
from io_scene_gltf2.io.com.gltf2_io_extensions import Extension

class MSFSMaterialAnimation:
    bl_options = {"UNDO"}

    extension_name = "ASOBO_property_animation"

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)

    @staticmethod
    def gather_actions(blender_object, blender_actions, blender_tracks, action_on_type, export_settings):
        # First step is to get a list of all material animation actions and NLA tracks (if used)
        if not (blender_object.type == "MESH" and blender_object.data is not None
                    and len(blender_object.material_slots) > 0):
            return

        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None:
                continue
            if material.animation_data is None: # Something to look out for - there may be circumstances where the animation data is actually in material.node_tree.animation_data
                continue
            if material.animation_data.action is None:
                continue

            blender_actions.append(material.animation_data.action)
            blender_tracks[material.animation_data.action.name] = None
            action_on_type[material.animation_data.action.name] = "MATERIAL"

            # Collect associated strips from NLA tracks.
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
                        action_on_type[material.animation_data.action.name] = "MATERIAL"

    @staticmethod
    def get_material_from_action(blender_object, blender_action):
        blender_material = None
        for material_slot in blender_object.material_slots:
            material = material_slot.material

            if material is None:
                continue

            if material.animation_data is not None:
                if blender_action == material.animation_data.action:
                    blender_material = material
                    break

        return blender_material

    @staticmethod
    def replace_channel_target(gltf2_animation_channel, channels, blender_object, action_name):
        blender_material = MSFSMaterialAnimation.get_material_from_action(blender_object, bpy.data.actions[action_name])
        if blender_material is None:
            return

        for channel in channels:
            try:
                gltf2_animation_channel.target = blender_material.path_resolve(channel.data_path)
            except ValueError:
                continue
            else:
                return

    @staticmethod
    def finalize_animation(gltf2_animation):
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

            blender_material = channel["target"]
            target_property = blender_material.path_from_id().split(".")[0]
            if blender_material.msfs_material_mode == "msfs_standard":
                if target_property == "msfs_color_albedo_mix":
                    channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/baseColorFactor"
                elif target_property == "msfs_color_emissive_mix":
                    channel["target"] = f"materials/{material_index}/emissiveFactor"
                elif target_property == "msfs_metallic_scale":
                    channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/metallicFactor"
                elif target_property == "msfs_roughness_scale":
                    channel["target"] = f"materials/{material_index}/pbrMetallicRoughness/roughnessFactor"
            elif blender_material.msfs_material_mode == "msfs_env_occluder":
                if target_property == "msfs_uv_offset_u":
                    channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetU"
                elif target_property == "msfs_uv_offset_v":
                    channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVOffsetV"
                elif target_property == "msfs_uv_tiling_u":
                    channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingU"
                elif target_property == "msfs_uv_tiling_v":
                    channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVTilingV"
                elif target_property == "msfs_uv_rotation":
                    channel["target"] = f"materials/{material_index}/extensions/ASOBO_material_UV_options/UVRotation"