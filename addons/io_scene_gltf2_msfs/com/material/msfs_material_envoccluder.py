
from .msfs_material import *

class MSFS_EnvOccluder(MSFS_Material):

    def __init__(self, material):
        super(MSFS_EnvOccluder, self).__init__(material)

    def displayParams(self):
        self.material.msfs_show_tint = True
        self.material.msfs_show_sss_color = False

        self.material.msfs_show_glass_parameters = False
        self.material.msfs_show_decal_parameters = False
        self.material.msfs_show_fresnel_parameters = False
        self.material.msfs_show_parallax_parameters = False
        self.material.msfs_show_geo_decal_parameters = False

        self.material.msfs_show_albedo = False
        self.material.msfs_show_metallic = False
        self.material.msfs_show_normal = False
        self.material.msfs_show_emissive = False
        self.material.msfs_show_detail_albedo = False
        self.material.msfs_show_detail_metallic = False
        self.material.msfs_show_detail_normal = False
        self.material.msfs_show_blend_mask = False
        self.material.msfs_show_anisotropic_direction = False
        self.material.msfs_show_clearcoat = False
        self.material.msfs_show_behind_glass = False
        self.material.msfs_show_wiper_mask = False

        self.material.msfs_show_blend_mode = False
        self.material.use_backface_culling = not self.material.msfs_double_sided

        self.material.msfs_show_draworder = False
        self.material.msfs_show_no_cast_shadow = False
        self.material.msfs_show_double_sided = False
        self.material.msfs_show_responsive_aa = False
        self.material.msfs_show_day_night_cycle = False

        self.material.msfs_show_collision_material = False
        self.material.msfs_show_road_material = False

        self.material.msfs_show_ao_use_uv2 = False
        self.material.msfs_show_uv_clamp = False

        self.material.msfs_show_alpha_cutoff = False
        self.material.msfs_show_blend_threshold = False
        #New
        self.material.msfs_show_pearl = False
        self.material.msfs_show_windshield_options = False

    def customShaderTree(self):
        pass