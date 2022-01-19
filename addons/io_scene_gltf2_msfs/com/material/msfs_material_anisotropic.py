
from .msfs_material import *

class MSFS_Anisotropic(MSFS_Material):

    def __init__(self, material):
        super(MSFS_Anisotropic, self).__init__(material)

    def displayParams(self):
        self.material.msfs_show_tint = True
        self.material.msfs_show_sss_color = False

        self.material.msfs_show_glass_parameters = False
        self.material.msfs_show_decal_parameters = False
        self.material.msfs_show_fresnel_parameters = False
        self.material.msfs_show_parallax_parameters = False
        self.material.msfs_show_geo_decal_parameters = False

        self.material.msfs_show_albedo = True
        self.material.msfs_show_metallic = True
        self.material.msfs_show_normal = True
        self.material.msfs_show_emissive = True
        self.material.msfs_show_detail_albedo = True
        self.material.msfs_show_detail_metallic = True
        self.material.msfs_show_detail_normal = True
        self.material.msfs_show_blend_mask = True
        self.material.msfs_show_anisotropic_direction = True
        self.material.msfs_show_clearcoat = False
        self.material.msfs_show_behind_glass = False
        self.material.msfs_show_wiper_mask = False

        self.material.msfs_show_blend_mode = True
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
        super(MSFS_Anisotropic, self).defaultShaderStree()
    