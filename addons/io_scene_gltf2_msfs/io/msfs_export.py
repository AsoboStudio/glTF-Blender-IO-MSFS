# glTF-Blender-IO-MSFS
# Copyright (C) 2021-2022 The glTF-Blender-IO-MSFS authors

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
import bpy
import urllib

from .. import get_version_string

from .msfs_light import MSFSLight
from .msfs_gizmo import MSFSGizmo
from .msfs_material import MSFSMaterial
from .msfs_material_animation import MSFSMaterialAnimation

class Export:

    material_actions = []
    
    def gather_asset_hook(self, gltf2_asset, export_settings):
        if self.properties.enabled == True:
            if gltf2_asset.extensions is None:
                gltf2_asset.extensions = {}
            gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
                name="ASOBO_normal_map_convention",
                extension={"tangent_space_convention": "DirectX"},
                required=False
            )

            gltf2_asset.generator += " and Asobo Studio MSFS Blender I/O v" + get_version_string()

    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        if self.properties.enabled:
            for i, image in enumerate(gltf2_plan.images):
                image.uri = os.path.basename(urllib.parse.unquote(image.uri))

            for animation in gltf2_plan.animations:
                MSFSMaterialAnimation.finalize_target(animation, gltf2_plan)

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled:

            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if blender_object.type == 'LIGHT':
                MSFSLight.export(gltf2_object, blender_object)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        if self.properties.enabled:
            MSFSGizmo.export(gltf2_scene.nodes, blender_scene, export_settings)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if self.properties.enabled:
            MSFSMaterial.export(gltf2_material, blender_material, export_settings)

    def gather_actions_hook(self, blender_object, blender_actions, blender_tracks, action_on_type, export_settings):
        if self.properties.enabled:
            # Keep track of what material actions we've already exported - no need to export it more than once. All values passed to the hook get modified by reference
            found_blender_actions, found_blender_tracks, found_action_on_type = MSFSMaterialAnimation.gather_actions(blender_object, self.material_actions, export_settings)

            if found_blender_actions:
                blender_actions.extend(found_blender_actions)
                self.material_actions.extend(found_blender_actions)
            if found_blender_tracks:
                blender_tracks.update(found_blender_tracks)
            if found_action_on_type:
                action_on_type.update(found_action_on_type)

    def gather_animation_channel_target_hook(self, gltf2_animation_channel_target, channels, blender_object, bake_bone, bake_channel, export_settings):
        MSFSMaterialAnimation.replace_channel_target(gltf2_animation_channel_target, channels, blender_object, export_settings)

    def pre_gather_animation_hook(self, gltf2_animation, blender_action, blender_object, export_settings):
        MSFSMaterialAnimation.add_placeholder_channel(gltf2_animation, blender_action, blender_object, export_settings)

    def gather_animation_hook(self, gltf2_animation, blender_action, blender_object, export_settings):
        MSFSMaterialAnimation.finalize_animation(gltf2_animation)