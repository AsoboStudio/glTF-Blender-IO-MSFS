# Copyright 2021-2022 The glTF-Blender-IO-MSFS authors.
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

import os
import urllib

from .. import get_version_string
from .msfs_gizmo import MSFSGizmo
from .msfs_light import MSFSLight
from .msfs_material import MSFSMaterial
from .msfs_unique_id import MSFS_unique_id


class Export:
    
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

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled:

            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_object, blender_object)

            if blender_object.type == 'LIGHT':
                MSFSLight.export(gltf2_object, blender_object)
    
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        if self.properties.enabled:

            if gltf2_node.extensions is None:
                gltf2_node.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_node, blender_bone)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        if self.properties.enabled:
            MSFSGizmo.export(gltf2_scene.nodes, blender_scene, export_settings)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if self.properties.enabled:
            # KHR_materials_emissive_strength issue with msfs materials for bloom

            # KHR_materials_emissive_strength revert the Khronos gltf code to add an extension for emissive scale > 1.0
            # return the emissive_factor back to the missive color multiplied by the emissive scale
            for extension in gltf2_material.extensions:
                if extension:
                    print("gather_gltf_extensions_hook - KHR Extension", gltf2_material.name, gltf2_material.extensions, extension, gltf2_material.emissive_factor)
                    if extension == "KHR_materials_emissive_strength":

                        for colorChannel in blender_material.node_tree.nodes['Emissive RGB'].outputs[0].default_value[0:3]:
                            print ("gather_gltf_extensions_hook - Color value", colorChannel)
                        maxchannel = max(blender_material.node_tree.nodes['Emissive RGB'].outputs[0].default_value[0:3])
                        emissive_scale = blender_material.node_tree.nodes['Emissive Scale'].outputs[0].default_value
                        print("gather_gltf_extensions_hook - maxchannel", maxchannel, emissive_scale)

                        print("gather_gltf_extensions_hook - change remove emissive_factor KHR_materials_emissive_strength")
                        gltf2_material.emissive_factor = [f * maxchannel * emissive_scale for f in gltf2_material.emissive_factor]
                        del gltf2_material.extensions['KHR_materials_emissive_strength']

            MSFSMaterial.export(gltf2_material, blender_material, export_settings)

