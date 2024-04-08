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


def equality_check(arr1, arr2, size1, size2):
   if (size1 != size2):
      return False
   for i in range(0, size2):
      # blender python color channel issues in floats ???
      if (int(arr1[i] * 10000000)/10000000 != int(arr2[i] * 10000000)/10000000):
         return False
   return True

class Export:
    
    def gather_asset_hook(self, gltf2_asset, export_settings):
        if self.properties.enable_msfs_extension == True:
            if gltf2_asset.extensions is None:
                gltf2_asset.extensions = {}
            gltf2_asset.extensions["ASOBO_normal_map_convention"] = self.Extension(
                name="ASOBO_normal_map_convention",
                extension={"tangent_space_convention": "DirectX"},
                required=False
            )

            gltf2_asset.generator += " and Asobo Studio MSFS Blender I/O v" + get_version_string()

    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        if self.properties.enable_msfs_extension:
            for i, image in enumerate(gltf2_plan.images):
                image.uri = os.path.basename(urllib.parse.unquote(image.uri))

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enable_msfs_extension:
            if gltf2_object.extensions is None:
                gltf2_object.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_object, blender_object)

            if blender_object.type == 'LIGHT':
                MSFSLight.export(gltf2_object, blender_object)
    
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        if self.properties.enable_msfs_extension:

            if gltf2_node.extensions is None:
                gltf2_node.extensions = {}

            if self.properties.use_unique_id:
                MSFS_unique_id.export(gltf2_node, blender_bone)

    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        if self.properties.enable_msfs_extension:
            MSFSGizmo.export(gltf2_scene.nodes, blender_scene, export_settings)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        # blender 3.3 removes base color values with base color texture - have to add back in
        print("gather_material_hook - Started with gltf2_material", gltf2_material, gltf2_material.pbr_metallic_roughness, gltf2_material.pbr_metallic_roughness.base_color_texture, gltf2_material.pbr_metallic_roughness.base_color_factor)
        base_color = blender_material.msfs_base_color_factor
        gltf2_base_color = gltf2_material.pbr_metallic_roughness.base_color_factor
        print("gather_material_hook - blender material - set base color factor before", blender_material, blender_material.msfs_base_color_texture, base_color[0], base_color[1], base_color[2], base_color[3], gltf2_base_color)
        if base_color is not None and gltf2_base_color is None:
            print("gather_material_hook - changing because none")
            gltf2_material.pbr_metallic_roughness.base_color_factor = [base_color[0],base_color[1],base_color[2],base_color[3]]
        if gltf2_base_color is not None:
            if not equality_check(base_color, gltf2_base_color, len(base_color), len(gltf2_base_color)):
                print("gather_material_hook - changing because different")
                gltf2_material.pbr_metallic_roughness.base_color_factor = [base_color[0],base_color[1],base_color[2],base_color[3]]
        print("gather_material_hook - blender material - set base color after", blender_material, blender_material.msfs_base_color_texture, blender_material.msfs_base_color_factor, gltf2_material.pbr_metallic_roughness.base_color_factor)


        if self.properties.enable_msfs_extension:
            MSFSMaterial.export(gltf2_material, blender_material, export_settings)
