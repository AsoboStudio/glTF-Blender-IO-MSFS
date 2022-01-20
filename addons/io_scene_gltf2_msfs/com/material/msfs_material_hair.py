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

from .msfs_material import *

class MSFS_Hair(MSFS_Material):

    def __init__(self, material):
        super(MSFS_Hair, self).__init__(material)

    def displayParams(self):
        self.material.msfs_show_tint = True
        self.material.msfs_show_sss_color = True

        self.material.msfs_show_glass_parameters = False
        self.material.msfs_show_decal_parameters = False
        self.material.msfs_show_fresnel_parameters = False
        self.material.msfs_show_parallax_parameters = False
        self.material.msfs_show_geo_decal_parameters = False

        self.material.msfs_show_albedo = True
        self.material.msfs_show_metallic = True
        self.material.msfs_show_normal = True
        self.material.msfs_show_emissive = True
        self.material.msfs_show_detail_albedo = False
        self.material.msfs_show_detail_metallic = False
        self.material.msfs_show_detail_normal = False
        self.material.msfs_show_blend_mask = False
        self.material.msfs_show_anisotropic_direction = True
        self.material.msfs_show_clearcoat = False
        self.material.msfs_show_behind_glass = False
        self.material.msfs_show_wiper_mask = False

        self.material.msfs_show_blend_mode = False
        self.material.use_backface_culling = not self.material.msfs_double_sided

        self.material.msfs_show_draworder = True
        self.material.msfs_show_no_cast_shadow = True
        self.material.msfs_show_double_sided = True
        self.material.msfs_show_responsive_aa = False
        self.material.msfs_show_day_night_cycle = False

        self.material.msfs_show_collision_material = True
        self.material.msfs_show_road_material = True

        self.material.msfs_show_ao_use_uv2 = True
        self.material.msfs_show_uv_clamp = True

        self.material.msfs_show_alpha_cutoff = False
        self.material.msfs_show_blend_threshold = True
        #New
        self.material.msfs_show_pearl = False
        self.material.msfs_show_windshield_options = False

    def customShaderTree(self):
        super(MSFS_Hair, self).defaultShaderStree()