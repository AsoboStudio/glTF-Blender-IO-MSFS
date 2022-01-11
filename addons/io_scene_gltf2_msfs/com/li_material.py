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

import bpy
from bpy.types import Material, Image
from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty, EnumProperty, FloatVectorProperty, PointerProperty
from .func_material import *


class MSFS_LI_material():
    # Use this function to update the shader node tree
    def switch_msfs_material(self,context):
        mat = context.active_object.active_material
        if mat.msfs_material_mode == 'msfs_standard':
            CreateMSFSStandardShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = True

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = True
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = True
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_standard material.")

        elif mat.msfs_material_mode == 'msfs_anisotropic':
            CreateMSFSAnisotropicShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = True
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_anisotropic material.")

        elif mat.msfs_material_mode == 'msfs_sss':
            CreateMSFSSSSShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = True

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = False
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_sss material.")

        elif mat.msfs_material_mode == 'msfs_glass':
            CreateMSFSGlassShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = True
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_glass material.")

        elif mat.msfs_material_mode == 'msfs_decal':
            CreateMSFSDecalShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = True
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = True

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_decal material.")

        elif mat.msfs_material_mode == 'msfs_clearcoat':
            CreateMSFSClearcoatShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = True
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_clearcoat material.")

        elif mat.msfs_material_mode == 'msfs_env_occluder':
            CreateMSFSEnvOccluderShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = False
            mat.msfs_show_metallic = False
            mat.msfs_show_normal = False
            mat.msfs_show_emissive = False
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = False
            mat.msfs_show_no_cast_shadow = False
            mat.msfs_show_double_sided = False
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = False
            mat.msfs_show_road_material = False

            mat.msfs_show_ao_use_uv2 = False
            mat.msfs_show_uv_clamp = False

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = False
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_env_occluder material.")

        elif mat.msfs_material_mode == 'msfs_fake_terrain':
            CreateMSFSFakeTerrainShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_fake_terrain material.")

        elif mat.msfs_material_mode == 'msfs_fresnel':
            CreateMSFSFresnelShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = True
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_fresnel material.")

        elif mat.msfs_material_mode == 'msfs_windshield':
            CreateMSFSWindshieldShader(mat)
 
            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False #Unlock this when available

            mat.msfs_show_blend_mode = True
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = True

            #mat.msfs_roughness_scale = 0.0
            #mat.msfs_metallic_scale = 0.0
            
            #switch_msfs_blendmode()
            if mat.msfs_blend_mode == 'BLEND':
                MakeTranslucent(mat)
            elif mat.msfs_blend_mode == 'MASKED':
                MakeMasked(mat)
            elif mat.msfs_blend_mode == 'DITHER':
                MakeDither(mat)
            else:
                MakeOpaque(mat)
            
            print("Switched to msfs_windshield material.")

        elif mat.msfs_material_mode == 'msfs_porthole':
            CreateMSFSPortholeShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = True
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_porthole material.")

        elif mat.msfs_material_mode == 'msfs_parallax':
            CreateMSFSParallaxShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = True
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = True
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_parallax material.")

        elif mat.msfs_material_mode == 'msfs_geo_decal':
            CreateMSFSGeoDecalShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = True

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = True
            mat.msfs_show_detail_metallic = True
            mat.msfs_show_detail_normal = True
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False

            print("Switched to msfs_geo_decal material.")

        elif mat.msfs_material_mode == 'msfs_hair':
            CreateMSFSHairShader(mat)

            mat.msfs_show_tint = True
            mat.msfs_show_sss_color = True

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = True
            mat.msfs_show_metallic = True
            mat.msfs_show_normal = True
            mat.msfs_show_emissive = True
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = True
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = True
            mat.msfs_show_no_cast_shadow = True
            mat.msfs_show_double_sided = True
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = True
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = True
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False
            
            print("Switched to msfs_hair material.")

        elif mat.msfs_material_mode == 'msfs_invisible':
            CreateMSFSInvisibleShader(mat)

            mat.msfs_show_tint = False
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = False
            mat.msfs_show_metallic = False
            mat.msfs_show_normal = False
            mat.msfs_show_emissive = False
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = False
            mat.msfs_show_no_cast_shadow = False
            mat.msfs_show_double_sided = False
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = True
            mat.msfs_show_road_material = True

            mat.msfs_show_ao_use_uv2 = False
            mat.msfs_show_uv_clamp = True

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = False
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False
            
            print("Switched to msfs_invisible material.")

        else:
            mat.msfs_show_tint = False
            mat.msfs_show_sss_color = False

            mat.msfs_show_glass_parameters = False
            mat.msfs_show_decal_parameters = False
            mat.msfs_show_fresnel_parameters = False
            mat.msfs_show_parallax_parameters = False
            mat.msfs_show_geo_decal_parameters = False

            mat.msfs_show_albedo = False
            mat.msfs_show_metallic = False
            mat.msfs_show_normal = False
            mat.msfs_show_emissive = False
            mat.msfs_show_detail_albedo = False
            mat.msfs_show_detail_metallic = False
            mat.msfs_show_detail_normal = False
            mat.msfs_show_blend_mask = False
            mat.msfs_show_anisotropic_direction = False
            mat.msfs_show_clearcoat = False
            mat.msfs_show_behind_glass = False
            mat.msfs_show_wiper_mask = False

            mat.msfs_show_blend_mode = False
            mat.use_backface_culling = not mat.msfs_double_sided

            mat.msfs_show_draworder = False
            mat.msfs_show_no_cast_shadow = False
            mat.msfs_show_double_sided = False
            mat.msfs_show_responsive_aa = False
            mat.msfs_show_day_night_cycle = False

            mat.msfs_show_collision_material = False
            mat.msfs_show_road_material = False

            mat.msfs_show_ao_use_uv2 = False
            mat.msfs_show_uv_clamp = False

            mat.msfs_show_alpha_cutoff = False
            mat.msfs_show_blend_threshold = False
            #New
            mat.msfs_show_pearl = False
            mat.msfs_show_windshield_options = False
            
            print("Switched to non-sim material.")

    def match_albedo(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        bsdf_node = nodes.get("bsdf")
        albedo = nodes.get("albedo")
        albedo_tint_mix = nodes.get("albedo_tint_mix")
        albedo_detail_mix = nodes.get("albedo_detail_mix")

        if albedo != None:
            nodes["albedo"].image = mat.msfs_albedo_texture

            if mat.msfs_albedo_texture != None:
                # Create the link:
                if albedo_tint_mix != None:
                    links.new(albedo.outputs["Color"], albedo_tint_mix.inputs["Color2"])
                if albedo_detail_mix != None:
                    links.new(albedo_detail_mix.outputs["Color"], bsdf_node.inputs["Base Color"])
            else:
                #unlink the separator:
                if albedo_tint_mix != None:
                    l = albedo_tint_mix.inputs["Color2"].links[0]
                    links.remove(l)                
                if bsdf_node != None:
                    l = bsdf_node.inputs["Base Color"].links[0]
                    links.remove(l)                

    def match_metallic(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        #Try to generate the links:
        bsdf_node = nodes.get("bsdf")
        metallic = nodes.get("metallic")
        metallic_sep_node = nodes.get("metallic_sep")

        if metallic != None:
            nodes["metallic"].image = mat.msfs_metallic_texture

            if mat.msfs_metallic_texture != None:
                nodes["metallic"].image.colorspace_settings.name = 'Non-Color'

                #link to bsdf
                if (bsdf_node != None and metallic_sep_node != None):
                    links.new(metallic_sep_node.outputs[1], bsdf_node.inputs["Roughness"])
                    links.new(metallic_sep_node.outputs[2], bsdf_node.inputs["Metallic"])
            else:
                #unlink the separator:
                if (bsdf_node != None and metallic_sep_node != None):
                    l = bsdf_node.inputs["Roughness"].links[0]
                    links.remove(l)                
                    l = bsdf_node.inputs["Metallic"].links[0]
                    links.remove(l)                

    def match_normal(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        bsdf_node = nodes.get("bsdf")
        normal = nodes.get("normal")
        normal_map_node = nodes.get("normal_map_node")

        if normal != None:
            nodes["normal"].image = mat.msfs_normal_texture

            if mat.msfs_normal_texture != None:
                nodes["normal"].image.colorspace_settings.name = 'Non-Color'
                if (bsdf_node != None and normal_map_node != None):
                        links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])
            else:
                if (bsdf_node != None and normal_map_node != None):
                    l = bsdf_node.inputs["Normal"].links[0]
                    links.remove(l)                

    def match_emissive(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        #Try to generate the links:
        bsdf_node = nodes.get("bsdf")
        emissive = nodes.get("emissive")
        emissive_tint_mix = nodes.get("emissive_tint_mix")

        if emissive != None:
            nodes["emissive"].image = mat.msfs_emissive_texture

            if mat.msfs_emissive_texture != "":
                #link to bsdf
                if (bsdf_node != None and emissive_tint_mix != None):
                    links.new(emissive_tint_mix.outputs["Color"], bsdf_node.inputs["Emission"])
            else:
                #unlink the separator:
                if (bsdf_node != None and emissive_tint_mix != None):
                    l = bsdf_node.inputs["Emission"].links[0]
                    links.remove(l)                

    def match_detail_albedo(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        albedo_detail_mix = nodes.get("albedo_detail_mix")
        detail_albedo = nodes.get("detail_albedo")

        if detail_albedo != None:
            nodes["detail_albedo"].image = mat.msfs_detail_albedo_texture
            
            if mat.msfs_detail_albedo_texture.name != "":
                # Create the link:
                if (detail_albedo != None and albedo_detail_mix != None):
                    links.new(detail_albedo.outputs["Color"], albedo_detail_mix.inputs["Color2"])
                    albedo_detail_mix.inputs[0].default_value = 0.5
            else:
                #unlink the separator:
                if (detail_albedo != None and albedo_detail_mix != None):
                    l = albedo_detail_mix.inputs["Color2"].links[0]
                    links.remove(l)                
                    albedo_detail_mix.inputs[0].default_value = 0.0

    def match_detail_metallic(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        metallic_detail_mix = nodes.get("metallic_detail_mix")
        detail_metallic = nodes.get("detail_metallic")

        if detail_metallic != None:
            detail_metallic.image = mat.msfs_detail_metallic_texture
            detail_metallic.image.colorspace_settings.name = 'Non-Color'
            if mat.msfs_detail_metallic_texture.name != "":
                # Create the link:
                if (detail_metallic != None and metallic_detail_mix != None):
                    links.new(detail_metallic.outputs["Color"], metallic_detail_mix.inputs["Color2"])
                    metallic_detail_mix.inputs[0].default_value = 0.5
            else:
                #unlink the separator:
                if (detail_metallic != None and metallic_detail_mix != None):
                    l = metallic_detail_mix.inputs["Color2"].links[0]
                    links.remove(l)                
                    metallic_detail_mix.inputs[0].default_value = 0.0

    def match_detail_normal(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        normal_detail_mix = nodes.get("normal_detail_mix")
        detail_normal = nodes.get("detail_normal")

        if detail_normal != None:
            detail_normal.image = mat.msfs_detail_normal_texture
            detail_normal.image.colorspace_settings.name = 'Non-Color'
            if mat.msfs_detail_normal_texture.name != "":
                # Create the link:
                if (detail_normal != None and normal_detail_mix != None):
                    links.new(detail_normal.outputs["Color"], normal_detail_mix.inputs["Color2"])
                    normal_detail_mix.inputs[0].default_value = 0.5
            else:
                #unlink the separator:
                if (detail_normal != None and normal_detail_mix != None):
                    l = normal_detail_mix.inputs["Color2"].links[0]
                    links.remove(l)                
                    normal_detail_mix.inputs[0].default_value = 0.0

    def match_blend_mask(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        if nodes.get("blend_mask", None) != None:
            nodes["blend_mask"].image = mat.msfs_blend_mask_texture
            nodes["blend_mask"].image.colorspace_settings.name = 'Non-Color'

            albedo_detail_mix = nodes.get("albedo_detail_mix")
            metallic_detail_mix = nodes.get("metallic_detail_mix")
            normal_detail_mix = nodes.get("normal_detail_mix")

            #link the node, if a texture is set:
            if mat.msfs_blend_mask_texture.name != "":
                if mat.msfs_blend_mask_texture.channels > 3:
                    if albedo_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Alpha"],albedo_detail_mix.inputs["Fac"])
                    if metallic_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Alpha"],metallic_detail_mix.inputs["Fac"])
                    if normal_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Alpha"],normal_detail_mix.inputs["Fac"])
                else:
                    if albedo_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Color"],albedo_detail_mix.inputs["Fac"])
                    if metallic_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Color"],metallic_detail_mix.inputs["Fac"])
                    if normal_detail_mix != None:
                        links.new(nodes["blend_mask"].outputs["Color"],normal_detail_mix.inputs["Fac"])
            else:
                if albedo_detail_mix != None:
                    l = albedo_detail_mix.inputs["Fac"].links[0]
                    links.remove(l)                
                if metallic_detail_mix != None:
                    l = metallic_detail_mix.inputs["Fac"].links[0]
                    links.remove(l)                
                if normal_detail_mix != None:
                    l = normal_detail_mix.inputs["Fac"].links[0]
                    links.remove(l)                

    def match_anisotropic_direction(self,context):
        mat = context.activate_object.active_material
        if mat.node_tree.nodes.get("anisotropic_direction", None) != None:
            mat.node_tree.nodes["anisotropic_direction"].image = mat.msfs_anisotropic_direction_texture
            mat.node_tree.nodes["anisotropic_direction"].image.colorspace_settings.name = 'Non-Color'

    def match_clearcoat(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        clearcoat = nodes.get("clearcoat")
        clearcoat_sep = nodes.get("clearcoat_sep")
        bsdf_node = nodes.get("bsdf")

        if clearcoat != None:
            mat.node_tree.nodes["clearcoat"].image = mat.msfs_clearcoat_texture
            mat.node_tree.nodes["clearcoat"].image.colorspace_settings.name = 'Non-Color'
            if (clearcoat_sep != None and bsdf_node != None):
                if mat.msfs_clearcoat_texture.name != "":
                    links.new(clearcoat_sep.outputs["R"],bsdf_node.inputs["Clearcoat"])
                    links.new(clearcoat_sep.outputs["G"],bsdf_node.inputs["Clearcoat Roughness"])
                else:
                    l = bsdf_node.inputs["Clearcoat"].links[0]
                    links.remove(l)                
                    l = bsdf_node.inputs["Clearcoat Roughness"].links[0]
                    links.remove(l)

    def match_behind_glass(self,context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        #Try to generate the links:
        albedo_detail_mix = nodes.get("albedo_detail_mix")
        behind_glass = nodes.get("behind_glass")

        if behind_glass != None:
            mat.node_tree.nodes["behind_glass"].image = mat.msfs_behind_glass_texture
            if mat.msfs_behind_glass_texture.name != "":
                # Create the link:
                if (behind_glass != None and albedo_detail_mix != None):
                    links.new(behind_glass.outputs["Color"], albedo_detail_mix.inputs["Color2"])
            else:
                #unlink the separator:
                if (behind_glass != None and albedo_detail_mix != None):
                    l = albedo_detail_mix.inputs["Color2"].links[0]
                    links.remove(l)                

    def match_wiper_mask(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links


    def switch_msfs_blendmode(self, context):
        mat = context.active_object.active_material
        if mat.msfs_material_mode == 'msfs_windshield' or mat.msfs_blend_mode == 'BLEND':
            MakeTranslucent(mat)
        elif mat.msfs_blend_mode == 'MASKED':
            MakeMasked(mat)
        elif mat.msfs_blend_mode == 'DITHER':
            MakeDither(mat)
        else:
            MakeOpaque(mat)

    #Update functions for the "tint" parameters:
    def update_color_albedo_mix(self, context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[0] = mat.msfs_color_albedo_mix[0]
            mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[1] = mat.msfs_color_albedo_mix[1]
            mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[2] = mat.msfs_color_albedo_mix[2]
            mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[0] = mat.msfs_color_albedo_mix[0]
            mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[1] = mat.msfs_color_albedo_mix[1]
            mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[2] = mat.msfs_color_albedo_mix[2]
            mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[0] = mat.msfs_color_albedo_mix[0]
            mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[1] = mat.msfs_color_albedo_mix[1]
            mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[2] = mat.msfs_color_albedo_mix[2]

    def update_color_alpha_mix(self, context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[3] = mat.msfs_color_alpha_mix
            mat.node_tree.nodes["alpha_multiply"].inputs[1].default_value = mat.msfs_color_alpha_mix
            
    def update_color_base_mix(self, context):
        mat = context.active_object.active_material
        #if mat.node_tree.nodes.get("bsdf", None) != None:
            #mat.node_tree.nodes["bsdf"].inputs.get('Base Color').default_value[3] = mat.msfs_color_alpha_mix
        mat.node_tree.nodes.get("albedo_tint").outputs[0].default_value[3] = mat.msfs_color_base_mix
        mat.node_tree.nodes["albedo_detail_mix"].inputs[0].default_value = mat.msfs_color_base_mix
        mat.node_tree.nodes["albedo_detail_mix"].inputs[2].default_value[3] = mat.msfs_color_base_mix

    def update_color_emissive_mix(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes

        bsdf = nodes.get("bsdf", None)
        emissive_tint = nodes.get("emissive_tint", None)

        if bsdf != None:
            bsdf.inputs.get('Emission').default_value[0] = mat.msfs_color_emissive_mix[0]
            bsdf.inputs.get('Emission').default_value[1] = mat.msfs_color_emissive_mix[1]
            bsdf.inputs.get('Emission').default_value[2] = mat.msfs_color_emissive_mix[2]
        if emissive_tint != None:
            emissive_tint.outputs[0].default_value[0] = mat.msfs_color_emissive_mix[0]
            emissive_tint.outputs[0].default_value[1] = mat.msfs_color_emissive_mix[1]
            emissive_tint.outputs[0].default_value[2] = mat.msfs_color_emissive_mix[2]

    def update_color_sss(self, context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs.get("Subsurface Color").default_value = mat.msfs_color_sss

    def update_double_sided(self, context):
        mat = context.active_object.active_material
        mat.use_backface_culling = not mat.msfs_double_sided

    def update_alpha_cutoff(self,context):
        mat = context.active_object.active_material
        mat.alpha_threshold = mat.msfs_alpha_cutoff

    def update_normal_scale(self,context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("normal_map_node", None) != None:
            mat.node_tree.nodes["normal_map_node"].inputs["Strength"].default_value = mat.msfs_normal_scale

    def update_detail_uv_scale(self,context):
        mat = context.active_object.active_material
        if mat.node_tree.nodes.get("detail_uv_scale", None) != None:
            mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[0] = mat.msfs_detail_uv_scale
            mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[1] = mat.msfs_detail_uv_scale
            mat.node_tree.nodes["detail_uv_scale"].inputs["Scale"].default_value[2] = mat.msfs_detail_uv_scale

    def update_detail_uv_offset(self,context):
        mat=context.active_object.active_material
        if mat.node_tree.nodes.get("detail_uv_scale", None) != None:
            mat.node_tree.nodes["detail_uv_scale"].inputs["Location"].default_value[0] = mat.msfs_detail_uv_offset_x
            mat.node_tree.nodes["detail_uv_scale"].inputs["Location"].default_value[1] = mat.msfs_detail_uv_offset_y

    def update_roughness_scale(self,context):
        mat=context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs["Roughness"].default_value = mat.msfs_roughness_scale

    def update_metallic_scale(self,context):
        mat=context.active_object.active_material
        if mat.node_tree.nodes.get("bsdf", None) != None:
            mat.node_tree.nodes["bsdf"].inputs["Metallic"].default_value = mat.msfs_metallic_scale


    # Main material mode, in accordance with MSFS material shaders:
    Material.msfs_material_mode =  bpy.props.EnumProperty(items=(('NONE',"Disabled",""),
                                                                ('msfs_standard', "MSFS Standard",""),
                                                                ('msfs_anisotropic', "MSFS Anisotropic",""),
                                                                ('msfs_sss', "MSFS Subsurface Scattering",""),
                                                                ('msfs_glass', "MSFS Glass",""),
                                                                ('msfs_decal', "MSFS Decal",""),
                                                                ('msfs_clearcoat', "MSFS Clearcoat",""),
                                                                ('msfs_env_occluder', "MSFS Environment Occluder",""),
                                                                ('msfs_fake_terrain', "MSFS Fake Terrain",""),
                                                                ('msfs_fresnel', "MSFS Fresnel Blending",""),
                                                                ('msfs_windshield', "MSFS Windshield",""),
                                                                ('msfs_porthole', "MSFS Porthole",""),
                                                                ('msfs_parallax', "MSFS Parallax",""),
                                                                ('msfs_geo_decal', "MSFS Geo Decal Frosted",""),
                                                                ('msfs_hair', "MSFS Hair",""),
                                                                ('msfs_invisible', "MSFS Invisible",""),), default='NONE',update=switch_msfs_material,)

    # Some flags to control the visibility of all of the paramters in the UI. 
    # Note: they don't control the actualy material parameters, only whether or 
    # not those parameters are being displayed. 
    Material.msfs_show_tint = bpy.props.BoolProperty(name="show_tint",default=False)
    Material.msfs_show_sss_color = bpy.props.BoolProperty(name="show_sss_color",default=False)

    Material.msfs_show_glass_parameters = bpy.props.BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_windshield_options = bpy.props.BoolProperty(name="show_glass_parameters",default=False)
    Material.msfs_show_decal_parameters = bpy.props.BoolProperty(name="show_decal_parameters",default=False)
    Material.msfs_show_fresnel_parameters = bpy.props.BoolProperty(name="show_fresnel_parameters",default=False)
    Material.msfs_show_parallax_parameters = bpy.props.BoolProperty(name="show_parallax_parameters",default=False)
    Material.msfs_show_geo_decal_parameters = bpy.props.BoolProperty(name="show_geo_decal_parameters",default=False)

    Material.msfs_show_albedo = bpy.props.BoolProperty(name="show_albedo",default=False)
    Material.msfs_show_metallic = bpy.props.BoolProperty(name="show_metallic",default=False)
    Material.msfs_show_normal = bpy.props.BoolProperty(name="show_normal",default=False)
    Material.msfs_show_emissive = bpy.props.BoolProperty(name="show_emissive",default=False)
    Material.msfs_show_detail_albedo = bpy.props.BoolProperty(name="show_detail_albedo",default=False)
    Material.msfs_show_detail_metallic = bpy.props.BoolProperty(name="show_detail_metallic",default=False)
    Material.msfs_show_detail_normal = bpy.props.BoolProperty(name="show_detail_normal",default=False)
    Material.msfs_show_blend_mask = bpy.props.BoolProperty(name="show_blend_mask",default=False)
    Material.msfs_show_anisotropic_direction = bpy.props.BoolProperty(name="show_anisotropic_direction",default=False)
    Material.msfs_show_clearcoat = bpy.props.BoolProperty(name="show_clearcoat",default=False)
    Material.msfs_show_behind_glass = bpy.props.BoolProperty(name="show_behind_glass",default=False)
    Material.msfs_show_wiper_mask = bpy.props.BoolProperty(name="show_wiper_mask",default=False)

    Material.msfs_show_blend_mode = bpy.props.BoolProperty(name="show_blend_mode",default=False)

    Material.msfs_show_draworder = bpy.props.BoolProperty(name="show_draworder",default=False)
    Material.msfs_show_no_cast_shadow = bpy.props.BoolProperty(name="show_no_cast_shadow",default=False)
    Material.msfs_show_double_sided = bpy.props.BoolProperty(name="show_double_sided",default=False)
    Material.msfs_show_responsive_aa = bpy.props.BoolProperty(name="show_responsive_aa",default=False)
    Material.msfs_show_day_night_cycle = bpy.props.BoolProperty(name="show_day_night_cycle",default=False)

    Material.msfs_show_collision_material = bpy.props.BoolProperty(name="show_collision_material",default=False)
    Material.msfs_show_road_material = bpy.props.BoolProperty(name="show_road_material",default=False)

    Material.msfs_show_ao_use_uv2 = bpy.props.BoolProperty(name="show_ao_use_uv2",default=False)
    Material.msfs_show_uv_clamp = bpy.props.BoolProperty(name="show_uv_clamp",default=False)

    Material.msfs_show_alpha_cutoff = bpy.props.BoolProperty(name="show_alpha_cutoff",default=False)
    Material.msfs_show_blend_threshold = bpy.props.BoolProperty(name="show_blend_threshold",default=False)
    Material.msfs_show_pearl = bpy.props.BoolProperty(name="show_pearl",default=False)

    # MSFS Material properties
    # The following variables are written into the glTF file when exporting.
    #Color blends:
    Material.msfs_color_albedo_mix = bpy.props.FloatVectorProperty(name="Albedo Color", subtype='COLOR', min=0.0, max=1.0,size=3,default=[1.0,1.0,1.0], description="The color value set here will be mixed in with the albedo value of the material.",update=update_color_albedo_mix)
    Material.msfs_color_emissive_mix = bpy.props.FloatVectorProperty(name="Emissive Color", subtype='COLOR', min=0.0, max=1.0, size=3,default=[0.0,0.0,0.0], description="The color value set here will be mixed in with the emissive value of the material.", update=update_color_emissive_mix)
    Material.msfs_color_alpha_mix = bpy.props.FloatProperty(name="Alpha multiplier", min=0, max=1, default=1, description="The alpha value set here will be mixed in with the Alpha value of the texture.",update=update_color_alpha_mix)
    Material.msfs_color_base_mix = bpy.props.FloatProperty(name="Albedo Color Mix", min=0, max=1, default=1, description="Mix factor for the Albedo Color with the Albedo Texture.",update=update_color_base_mix)
    Material.msfs_color_sss = bpy.props.FloatVectorProperty(name="SSS Color", subtype='COLOR',min=0.0, max=1.0,size=4, default=[1.0,1.0,1.0,1.0], description = "Use the color picker to set the color of the subsurface scattering.",update=update_color_sss)
    # Windshield
    Material.msfs_rain_drop_scale = FloatProperty(
        name="Rain Drop Scale",
        min=0.0,
        max=100.0,
        default=1.0
    )
    Material.msfs_wiper_1_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )
    Material.msfs_wiper_2_state = FloatProperty(
        name="Wiper 2 State",
        min=0.0,
        max=1.0,
        default=0.0
    )  # The 3DS Max plugin has up to 4 states, but the last 2 aren't visible
    Material.msfs_wiper_3_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )
    Material.msfs_wiper_4_state = FloatProperty(
        name="Wiper 1 State",
        min=0.0,
        max=1.0,
        default=0.0
    )

    #Glass parameters:
    Material.msfs_glass_reflection_mask_factor = bpy.props.FloatProperty(name="Reflection mask factor", min=0.0,max=1.0,default=1.0)
    Material.msfs_glass_deformation_factor = bpy.props.FloatProperty(name = "Deformation factor", min=0.0, max=1.0,default=0.0)

    #Pearl
    

    Material.msfs_use_pearl_effect = BoolProperty(
        name="Use Pearl Effect",
        default=False
    )
    Material.msfs_pearl_shift = FloatProperty(
        name="Color Shift",
        min=-999.0,
        max=999.0,
        default=0.0
    )
    Material.msfs_pearl_range = FloatProperty(
        name="Color Range",
        min=-999.0,
        max=999.0,
        default=0.0
    )
    Material.msfs_pearl_brightness = FloatProperty(
        name="Color Brightness",
        min=-1.0,
        max=1.0,
        default=0.0
    )

    #Decal parameters:
    Material.msfs_decal_blend_factor_color = bpy.props.FloatProperty(name="Color", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_metal = bpy.props.FloatProperty(name="Metal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_normal = bpy.props.FloatProperty(name="Normal", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_roughness = bpy.props.FloatProperty(name="Roughness", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_occlusion = bpy.props.FloatProperty(name="Occlusion", min=0.0,max=1.0,default=1.0)
    Material.msfs_decal_blend_factor_emissive = bpy.props.FloatProperty(name="Emissive", min=0.0,max=1.0,default=1.0)

    #Fresnel parameters:
    Material.msfs_fresnel_factor = bpy.props.FloatProperty(name="Fresnel factor", min=0.0,max=1.0,default=1.0)
    Material.msfs_fresnel_opacity_bias = bpy.props.FloatProperty(name="Fresnel opacity bias", min=0.0,max=1.0,default=1.0)

    #Parallax parameters:
    Material.msfs_parallax_scale = bpy.props.FloatProperty(name="Scale", min=0.0,max=1.0,default=0.0)
    Material.msfs_parallax_room_size_x = bpy.props.FloatProperty(name="X", min=0.0,default=0.5)
    Material.msfs_parallax_room_size_y = bpy.props.FloatProperty(name="Y", min=0.0,default=0.5)
    Material.msfs_parallax_room_number = bpy.props.FloatProperty(name="Rm number XY", min=0.0,default=1.0)
    Material.msfs_parallax_corridor = bpy.props.BoolProperty(name="Corridor", default=False)

    #Geo Decal Frosted parameters:
    Material.msfs_geo_decal_blend_factor_color = bpy.props.FloatProperty(name="Color", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_metal = bpy.props.FloatProperty(name="Metal", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_normal = bpy.props.FloatProperty(name="Normal", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_roughness = bpy.props.FloatProperty(name="Roughness", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_blast_sys = bpy.props.FloatProperty(name="Blast Sys.", min=0.0,max=1.0,default=1.0)
    Material.msfs_geo_decal_blend_factor_melt_sys = bpy.props.FloatProperty(name="Melt Sys", min=0.0,max=1.0,default=1.0)

    #Textures:
    Material.msfs_albedo_texture = PointerProperty(type = Image, name = "Albedo map", update = match_albedo)
    Material.msfs_metallic_texture = PointerProperty(type = Image, name = "Metallic map", update = match_metallic)
    Material.msfs_normal_texture = PointerProperty(type = Image, name = "Normal map", update = match_normal)
    Material.msfs_emissive_texture = PointerProperty(type = Image, name = "Emissive map", update = match_emissive)

    Material.msfs_detail_albedo_texture = PointerProperty(type = Image, name = "Detail Color map", update = match_detail_albedo)
    Material.msfs_detail_metallic_texture = PointerProperty(type = Image, name = "Detail Metallic map", update = match_detail_metallic)
    Material.msfs_detail_normal_texture = PointerProperty(type = Image, name = "Detail Normal map", update = match_detail_normal)

    Material.msfs_blend_mask_texture = PointerProperty(type = Image, name = "Blend mask", update = match_blend_mask)

    Material.msfs_anisotropic_direction_texture = PointerProperty(type = Image, name = "Anisotropic direction (RG)", update = match_anisotropic_direction)
    Material.msfs_clearcoat_texture = PointerProperty(type = Image, name = "Clearcoat amount (R), Clearcoat rough (G)", update = match_clearcoat)
    Material.msfs_behind_glass_texture = PointerProperty(type = Image, name = "Behind glass Albedo map", update = match_behind_glass)
    Material.msfs_wiper_mask_texture = PointerProperty(type = Image, name = "Wiper mask (RG)", update = match_wiper_mask)

    #Alpha mode:
    Material.msfs_blend_mode = bpy.props.EnumProperty(name="Blend mode",items=(('OPAQUE',"Opaque","Creates a fully non-transparent material."),
                                                                               ('MASKED',"Masked","This blend mode uses the alpha map to mask off parts of the material, but only if the alpha value exceeds the value set in the alpha cutoff parameter."),
                                                                               ('BLEND',"Blend","This blend mode uses the alpha map to gradually blend in the material. Use this for materials like glass."),
                                                                               ('DITHER',"Dither","Weird blend mode. But works well for hair. No visible effect in Blender."),), 
                                                                               default='OPAQUE',update=switch_msfs_blendmode)
    
    #Render parameters:
    Material.msfs_draw_order = bpy.props.IntProperty(name="Draw order",default = 0, min = 0)
    Material.msfs_no_cast_shadow = bpy.props.BoolProperty(name="No cast shadow",default=False)
    Material.msfs_double_sided = bpy.props.BoolProperty(name="Double sided",default=False,update=update_double_sided)
    Material.msfs_responsive_aa = bpy.props.BoolProperty(name="Responsive AA", default=False,description="")
    Material.msfs_day_night_cycle = bpy.props.BoolProperty(name="Day/Night cycle", default=False)

    #Gameplay parameters:
    Material.msfs_collision_material = bpy.props.BoolProperty(name="Collision material",default=False)
    Material.msfs_road_material = bpy.props.BoolProperty(name="Road material",default=False)

    #UV options:
    
    Material.msfs_uv_offset_u = FloatProperty(
        name="U",
        min=-10.0,
        max=10.0,
        default=0.0
    )
    Material.msfs_uv_offset_v = FloatProperty(
        name="V",
        min=-10.0,
        max=10.0,
        default=0.0
    )
    Material.msfs_uv_tiling_u = FloatProperty(
        name="U",
        min=-10.0,
        max=10.0,
        default=1.0
    )
    Material.msfs_uv_tiling_v = FloatProperty(
        name="V",
        min=-10.0,
        max=10.0,
        default=1.0
    )
    Material.msfs_uv_rotation = FloatProperty(
        name="UV Rotation",
        min=-360.0,
        max=360.0,
        default=0.0
    )
    Material.msfs_ao_use_uv2 = bpy.props.BoolProperty(name="AO use UV2",default=False)
    Material.msfs_uv_clamp_x = bpy.props.BoolProperty(name="X",default=False)
    Material.msfs_uv_clamp_y = bpy.props.BoolProperty(name="Y",default=False)
    Material.msfs_uv_clamp_z = bpy.props.BoolProperty(name="Z",default=False)

    #Material parameters
    Material.msfs_roughness_scale = bpy.props.FloatProperty(name="Roughness scale",min=0,max=1,default=1, update = update_roughness_scale)
    Material.msfs_metallic_scale = bpy.props.FloatProperty(name="Metallic scale",min=0,max=1,default=1, update = update_metallic_scale)
    Material.msfs_normal_scale = bpy.props.FloatProperty(name="Normal scale",min=0,default=1,update=update_normal_scale)
    Material.msfs_alpha_cutoff = bpy.props.FloatProperty(name="Alpha cutoff",min=0,max=1,default=0.1,update=update_alpha_cutoff)
    Material.msfs_detail_uv_scale = bpy.props.FloatProperty(name="Detail UV scale",min=0,default=1,update=update_detail_uv_scale)
    Material.msfs_detail_uv_offset_x = bpy.props.FloatProperty(name="X",min=-1,max=1,default=0,update=update_detail_uv_offset)
    Material.msfs_detail_uv_offset_y = bpy.props.FloatProperty(name="Y",min=-1,max=1,default=0,update=update_detail_uv_offset)
    Material.msfs_detail_normal_scale = bpy.props.FloatProperty(name="Detail normal scale",min=0,max=1,default=1)
    Material.msfs_blend_threshold = bpy.props.FloatProperty(name="Blend threshold",min=0,max=1,default=0.1)


