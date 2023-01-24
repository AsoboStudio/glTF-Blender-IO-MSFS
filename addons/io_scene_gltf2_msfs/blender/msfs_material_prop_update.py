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

from .msfs_material_function import MSFS_Material, MSFS_ShaderNodes

from .material.msfs_material_standard import MSFS_Standard
from .material.msfs_material_geo_decal import MSFS_Geo_Decal
from .material.msfs_material_geo_decal_frosted import MSFS_Geo_Decal_Frosted
from .material.msfs_material_windshield import MSFS_Windshield
from .material.msfs_material_porthole import MSFS_Porthole
from .material.msfs_material_glass import MSFS_Glass
from .material.msfs_material_clearcoat import MSFS_Clearcoat
from .material.msfs_material_parallax import MSFS_Parallax
from .material.msfs_material_anisotropic import MSFS_Anisotropic
from .material.msfs_material_hair import MSFS_Hair
from .material.msfs_material_sss import MSFS_SSS
from .material.msfs_material_invisible import MSFS_Invisible
from .material.msfs_material_fake_terrain import MSFS_Fake_Terrain
from .material.msfs_material_fresnel_fade import MSFS_Fresnel_Fade
from .material.msfs_material_environment_occluder import MSFS_Environment_Occluder
from .material.msfs_material_ghost import MSFS_Ghost


class MSFS_Material_Property_Update:
    @staticmethod
    def getMaterial(mat):
        if mat.msfs_material_type == "msfs_standard":
            return MSFS_Standard(mat)
        elif mat.msfs_material_type == "msfs_geo_decal":
            return MSFS_Geo_Decal(mat)
        elif mat.msfs_material_type == "msfs_geo_decal_frosted":
            return MSFS_Geo_Decal_Frosted(mat)
        elif mat.msfs_material_type == "msfs_windshield":
            return MSFS_Windshield(mat)
        elif mat.msfs_material_type == "msfs_porthole":
            return MSFS_Porthole(mat)
        elif mat.msfs_material_type == "msfs_glass":
            return MSFS_Glass(mat)
        elif mat.msfs_material_type == "msfs_clearcoat":
            return MSFS_Clearcoat(mat)
        elif mat.msfs_material_type == "msfs_parallax":
            return MSFS_Parallax(mat)
        elif mat.msfs_material_type == "msfs_anisotropic":
            return MSFS_Anisotropic(mat)
        elif mat.msfs_material_type == "msfs_hair":
            return MSFS_Hair(mat)
        elif mat.msfs_material_type == "msfs_sss":
            return MSFS_SSS(mat)
        elif mat.msfs_material_type == "msfs_invisible":
            return MSFS_Invisible(mat)
        elif mat.msfs_material_type == "msfs_fake_terrain":
            return MSFS_Fake_Terrain(mat)
        elif mat.msfs_material_type == "msfs_fresnel_fade":
            return MSFS_Fresnel_Fade(mat)
        elif mat.msfs_material_type == "msfs_environment_occluder":
            return MSFS_Environment_Occluder(mat)
        elif mat.msfs_material_type == "msfs_ghost":
            return MSFS_Ghost(mat)

    @staticmethod
    def update_msfs_material_type(self, context):
        msfs_mat = None
        if self.msfs_material_type == "msfs_standard":
            msfs_mat = MSFS_Standard(self, buildTree=True)
        elif self.msfs_material_type == "msfs_geo_decal":
            msfs_mat = MSFS_Geo_Decal(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_geo_decal_frosted":
            msfs_mat = MSFS_Geo_Decal_Frosted(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_windshield":
            msfs_mat = MSFS_Windshield(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
        elif self.msfs_material_type == "msfs_porthole":
            self.msfs_alpha_mode = "OPAQUE"
            msfs_mat = MSFS_Porthole(self, buildTree=True)
        elif self.msfs_material_type == "msfs_glass":
            msfs_mat = MSFS_Glass(self, buildTree=True)
            self.msfs_alpha_mode = "BLEND"
            self.msfs_metallic_factor = 0.0
        elif self.msfs_material_type == "msfs_clearcoat":
            msfs_mat = MSFS_Clearcoat(self, buildTree=True)
        elif self.msfs_material_type == "msfs_parallax":
            msfs_mat = MSFS_Parallax(self, buildTree=True)
            self.msfs_alpha_mode = "MASK"
        elif self.msfs_material_type == "msfs_anisotropic":
            msfs_mat = MSFS_Anisotropic(self, buildTree=True)
        elif self.msfs_material_type == "msfs_hair":
            msfs_mat = MSFS_Hair(self, buildTree=True)
        elif self.msfs_material_type == "msfs_sss":
            msfs_mat = MSFS_SSS(self, buildTree=True)
        elif self.msfs_material_type == "msfs_invisible":
            msfs_mat = MSFS_Invisible(self, buildTree=False)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_fake_terrain":
            msfs_mat = MSFS_Fake_Terrain(self, buildTree=True)
        elif self.msfs_material_type == "msfs_fresnel_fade":
            msfs_mat = MSFS_Fresnel_Fade(self, buildTree=True)
        elif self.msfs_material_type == "msfs_environment_occluder":
            msfs_mat = MSFS_Environment_Occluder(self, buildTree=False)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        elif self.msfs_material_type == "msfs_ghost":
            msfs_mat = MSFS_Ghost(self, buildTree=True)
            self.msfs_no_cast_shadow = True
            self.msfs_alpha_mode = "BLEND"
        else:
            msfs_mat = MSFS_Material(self)
            msfs_mat.revertToPBRShaderTree()
            return

    @staticmethod
    def update_base_color_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is None:
            return
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setBaseColorTex(self.msfs_base_color_texture)

    @staticmethod
    def update_comp_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is None:
            return
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setCompTex(self.msfs_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_normal_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is None:
            return
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setNormalTex(self.msfs_normal_texture)

    @staticmethod
    def update_emissive_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is None:
            return
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setEmissiveTexture(self.msfs_emissive_texture)

    @staticmethod
    def update_detail_color_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is None:
            return
        if type(msfs) is MSFS_Invisible:
            return
        if type(msfs) is MSFS_Parallax:
            nodes = self.node_tree.nodes
            links = self.node_tree.links

            # Try to generate the links:
            albedo_detail_mix = nodes.get("albedo_detail_mix")
            behind_glass = nodes.get("behind_glass")

            if behind_glass != None:
                self.node_tree.nodes[
                    "behind_glass"
                ].image = self.msfs_detail_color_texture
                if self.msfs_detail_color_texture.name != "":
                    # Create the link:
                    if behind_glass != None and albedo_detail_mix != None:
                        links.new(
                            behind_glass.outputs["Color"],
                            albedo_detail_mix.inputs["Color2"],
                        )
                else:
                    # unlink the separator:
                    if behind_glass != None and albedo_detail_mix != None:
                        l = albedo_detail_mix.inputs["Color2"].links[0]
                        links.remove(l)
        else:
            msfs.setDetailColorTex(self.msfs_detail_color_texture)

    @staticmethod
    def update_detail_comp_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            if type(msfs) is MSFS_Invisible:
                return
            msfs.setDetailCompTex(self.msfs_detail_occlusion_metallic_roughness_texture)

    @staticmethod
    def update_detail_normal_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if type(msfs) is MSFS_Invisible:
            return
        msfs.setDetailNormalTex(self.msfs_detail_normal_texture)

    @staticmethod
    def update_blend_mask_texture(self, context):
        nodes = self.node_tree.nodes
        blendTex = nodes.get(MSFS_ShaderNodes.blendMaskTex.value)
        if not blendTex:
            return
        blendTex.image = self.msfs_blend_mask_texture
        if self.msfs_material_type == "msfs_standard":
            msfs_mat = MSFS_Standard(self)
            msfs_mat = msfs_mat.toggleVertexBlendMapMask(
                self.msfs_blend_mask_texture is None
            )

    @staticmethod
    def update_extra_slot1_texture(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if type(msfs) is MSFS_Anisotropic or type(msfs) is MSFS_Hair:
            msfs.setAnisotropicTex(self.msfs_extra_slot1_texture)

    @staticmethod
    def update_dirt_texture(self, context):
        nodes = self.node_tree.nodes
        links = self.node_tree.links

        clearcoat = nodes.get("clearcoat")
        clearcoat_sep = nodes.get("clearcoat_sep")
        bsdf_node = nodes.get("bsdf")

        if clearcoat != None:
            self.node_tree.nodes["clearcoat"].image = self.msfs_dirt_texture
            self.node_tree.nodes[
                "clearcoat"
            ].image.colorspace_settings.name = "Non-Color"
            if clearcoat_sep != None and bsdf_node != None:
                if self.msfs_dirt_texture.name != "":
                    links.new(clearcoat_sep.outputs["R"], bsdf_node.inputs["Clearcoat"])
                    links.new(
                        clearcoat_sep.outputs["G"],
                        bsdf_node.inputs["Clearcoat Roughness"],
                    )
                else:
                    l = bsdf_node.inputs["Clearcoat"].links[0]
                    links.remove(l)
                    l = bsdf_node.inputs["Clearcoat Roughness"].links[0]
                    links.remove(l)

    @staticmethod
    def update_wiper_mask(self, context):
        nodes = self.node_tree.nodes
        links = self.node_tree.links

    @staticmethod
    def update_alpha_mode(self, context):
        msfs_mat = MSFS_Material(self)
        msfs_mat.setBlendMode(self.msfs_alpha_mode)

    # Update functions for the "tint" parameters:
    @staticmethod
    def update_base_color(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setBaseColor(self.msfs_base_color_factor)

    @staticmethod
    def update_emissive_color(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setEmissiveColor(self.msfs_emissive_factor)

    @staticmethod
    def update_emissive_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setEmissiveScale(self.msfs_emissive_scale)

    @staticmethod
    def update_metallic_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setMetallicScale(self.msfs_metallic_factor)

    @staticmethod
    def update_roughness_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setRoughnessScale(self.msfs_roughness_factor)

    @staticmethod
    def update_normal_scale(self, context):
        msfs = MSFS_Material_Property_Update.getMaterial(self)
        if msfs is not None:
            msfs.setNormalScale(self.msfs_normal_scale)

    @staticmethod
    def update_color_sss(self, context):
        if self.node_tree.nodes.get("Principled BSDF", None) != None:
            self.node_tree.nodes["Principled BSDF"].inputs.get(
                "Subsurface Color"
            ).default_value = self.msfs_sss_color

    @staticmethod
    def update_double_sided(self, context):
        self.use_backface_culling = not self.msfs_double_sided

    @staticmethod
    def update_alpha_cutoff(self, context):
        self.alpha_threshold = self.msfs_alpha_cutoff

    @staticmethod
    def update_detail_uv(self, context):
        nodes = self.node_tree.nodes
        detailUvScaleNode = nodes.get(MSFS_ShaderNodes.detailUVScale.value)
        detailUvOffsetUNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetU.value)
        detailUvOffsetVNode = nodes.get(MSFS_ShaderNodes.detailUVOffsetV.value)
        detailNormalScaleNode = nodes.get(MSFS_ShaderNodes.detailNormalScale.value)
        if (
            detailUvScaleNode
            and detailUvOffsetUNode
            and detailUvOffsetVNode
            and detailNormalScaleNode
        ):
            detailUvScaleNode.outputs[0].default_value = self.msfs_detail_uv_scale
            detailUvOffsetUNode.outputs[0].default_value = self.msfs_detail_uv_offset_u
            detailUvOffsetVNode.outputs[0].default_value = self.msfs_detail_uv_offset_v
            detailNormalScaleNode.outputs[
                0
            ].default_value = self.msfs_detail_normal_scale
