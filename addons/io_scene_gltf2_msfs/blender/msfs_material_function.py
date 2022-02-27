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

import bpy
from enum import Enum


class MSFS_ShaderNodes(Enum):
    materialOutput = "Material Output"
    principledBSDF = "Principled BSDF"
    glTFSettings = "glTF Settings"
    baseColorTex = "Base Color Texture"
    baseColorRGB = "Base Color RGB"
    baseColorA = "Base Color A"
    alphaCutoff = "Alpha Cutoff"
    baseColorMulRGB = "Base Color Multiplier RGB"
    baseColorMulA = "Base Color Multiplier A"
    normalTex = "Normal Texture"
    normalScale = "Normal Scale"
    compTex = "Occlusion(R) Roughness(G) Metallic(B)"
    compSeparate = "SplitOcclMetalRough"
    roughnessScale = "Roughness Scale"
    metallicScale = "Metallic Scale"
    occlusionMul = "Occlusion Multiplier"
    roughnessMul = "Roughness Multiplier"
    metallicMul = "Metallic Multiplier"
    emissiveTex = "Emissive Texture"
    emissiveColor = "Emissive RGB"
    emissiveScale = "Emissive Scale"
    emissiveMul = "Emissive Multiplier"
    normalMap = "Normal Map"
    detailColorTex = "Detail Color(RGBA)"
    detailCompTex = "Detail Occlusion(R) Roughness(G) Metallic(B)"
    detailNormalTex = "Detail Normal"
    blendMaskTex = "Blend Mask"
    detailNormalScale = "Detail Normal Scale"
    detailUVScale = "Detail UV Scale"
    detailUVOffsetU = "Detail UV Offset U"
    detailUVOffsetV = "Detail UV Offset V"
    uvMap = "UV Map"
    combineUVScale = "Combine UV Scale"
    combineUVOffset = "Combine UV Offset"
    mulUVScale = "Multiply UV Scale"
    addUVOffset = "Multiply UV Offset"
    detailNormalMap = "Detail Normal Map"
    blendNormalMap = "Blend Normal Map"
    blendColorMap = "Blend Color Map"
    blendAlphaMap = "Blend Alpha Map"
    blendCompMap = "Blend Occlusion(R) Roughness(G) Metallic(B) Map"
    vertexColor = "Vertex Color"


class MSFSMaterialPropertyUpdates:
    @staticmethod
    def update_msfs_material_type(material, context):
        # Overwrite some properties if on certain property
        if material.msfs_material_type == "msfs_windshield":
            material.msfs_metallic_factor = 0.0
        elif material.msfs_material_type == "msfs_glass":
            material.msfs_metallic_factor = 0.0
        elif material.msfs_material_type == "msfs_parallax":
            material.msfs_alpha_mode = "MASK"
        elif material.msfs_material_type == "msfs_ghost":
            material.msfs_no_cast_shadow = True
            material.msfs_alpha_mode = "BLEND"

        # Update node tree
        if material.msfs_material_type == "NONE":
            MSFSMaterialRendering.revert_to_default_tree(material)
        else:
            MSFSMaterialRendering.build_node_tree(material)

    @staticmethod
    def update_base_color_texture(material, context):
        if material.msfs_material_type != "msfs_invisible":
            nodeBaseColorTex = MSFSMaterialRendering.get_node(
                material, MSFS_ShaderNodes.baseColorTex.value
            )
            nodeBaseColorTex.image = material.msfs_base_color_texture
            MSFSMaterialRendering.update_color_links(material)

    @staticmethod
    def update_comp_texture(material, context):
        if material.msfs_material_type != "msfs_invisible":
            nodeCompTex = MSFSMaterialRendering.get_node(
                material, MSFS_ShaderNodes.compTex.value
            )
            nodeCompTex.image = material.msfs_occlusion_metallic_roughness_texture
            MSFSMaterialRendering.update_comp_links(material)

    @staticmethod
    def update_normal_texture(material, context):
        normalTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.normalTex.value
        )
        if not normalTex:
            return
        normalTex.image = material.msfs_normal_texture

    @staticmethod
    def update_emissive_texture(material, context):
        emissiveTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.emissiveTex.value
        )
        if not emissiveTex:
            return
        emissiveTex.image = material.msfs_emissive_texture

    @staticmethod
    def update_detail_color_texture(material, context):
        if material.msfs_material_type != "msfs_invisible":
            if (
                material.msfs_material_type == "msfs_parallax"
            ):  # Different rendering for material types
                albedo_detail_mix = MSFSMaterialRendering.get_node(
                    material, "albedo_detail_mix"
                )
                behind_glass = MSFSMaterialRendering.get_node(material, "behind_glass")

                if behind_glass != None:
                    material.node_tree.nodes[
                        "behind_glass"
                    ].image = material.msfs_detail_color_texture
                    if material.msfs_detail_color_texture.name != "":
                        # Create the link:
                        if behind_glass != None and albedo_detail_mix != None:
                            material.node_tree.links.new(
                                behind_glass.outputs["Color"],
                                albedo_detail_mix.inputs["Color2"],
                            )
                    else:
                        # unlink the separator:
                        if behind_glass != None and albedo_detail_mix != None:
                            l = albedo_detail_mix.inputs["Color2"].links[0]
                            material.node_tree.links.remove(l)
            else:
                nodeDetailColor = MSFSMaterialRendering.get_node(
                    material, MSFS_ShaderNodes.detailColorTex.value
                )
                nodeDetailColor.image = material.msfs_detail_color_texture
                MSFSMaterialRendering.update_color_links(material)

    @staticmethod
    def update_detail_comp_texture(material, context):
        if material.msfs_material_type != "msfs_invisible":
            nodeDetailCompTex = MSFSMaterialRendering.get_node(
                material, MSFS_ShaderNodes.detailCompTex.value
            )
            nodeDetailCompTex.image = (
                material.msfs_detail_occlusion_metallic_roughness_texture
            )
            MSFSMaterialRendering.update_comp_links(material)

    @staticmethod
    def update_detail_normal_texture(material, context):
        detailNormalTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailNormalTex.value
        )
        blendNormalMapNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.blendNormalMap.value
        )
        if not detailNormalTex:
            return
        detailNormalTex.image = material.msfs_detail_normal_texture
        blendNormalMapNode.inputs[0].default_value = (
            0 if material.msfs_detail_normal_texture == None else 1
        )

    @staticmethod
    def update_blend_mask_texture(material, context):
        blendTex = MSFSMaterialRendering.get_node(MSFS_ShaderNodes.blendMaskTex.value)
        if not blendTex:
            return
        blendTex.image = material.msfs_blend_mask_texture
        if material.msfs_material_type == "msfs_standard":
            MSFSMaterialRendering.toggle_vertex_blend_map_mask(
                material, material.msfs_blend_mask_texture is None
            )

    @staticmethod
    def update_wetness_ao_texture(material, context):
        if material.node_tree.nodes.get("anisotropic_direction", None) != None:
            material.node_tree.nodes[
                "anisotropic_direction"
            ].image = material.msfs_wetness_ao_texture
            material.node_tree.nodes[
                "anisotropic_direction"
            ].image.colorspace_settings.name = "Non-Color"

    @staticmethod
    def update_dirt_texture(material, context):
        clearcoat = MSFSMaterialRendering.get_node(material, "clearcoat")
        clearcoat_sep = MSFSMaterialRendering.get_node(material, "clearcoat_sep")
        bsdf_node = MSFSMaterialRendering.get_node(material, "bsdf")

        if clearcoat != None:
            material.node_tree.nodes[
                "clearcoat"
            ].image = material.msfs_wetness_ao_texture
            material.node_tree.nodes[
                "clearcoat"
            ].image.colorspace_settings.name = "Non-Color"

            if clearcoat_sep != None and bsdf_node != None:
                if material.msfs_wetness_ao_texture.name != "":
                    material.node_tree.links.new(
                        clearcoat_sep.outputs["R"], bsdf_node.inputs["Clearcoat"]
                    )
                    material.node_tree.links.new(
                        clearcoat_sep.outputs["G"],
                        bsdf_node.inputs["Clearcoat Roughness"],
                    )
                else:
                    l = bsdf_node.inputs["Clearcoat"].links[0]
                    material.node_tree.links.remove(l)
                    l = bsdf_node.inputs["Clearcoat Roughness"].links[0]
                    material.node_tree.links.remove(l)

    @staticmethod
    def update_alpha_mode(material, context):
        if material.msfs_alpha_mode == "BLEND":
            MSFSMaterialRendering.make_alpha_blend(material)
        elif material.msfs_alpha_mode == "MASKED":
            MSFSMaterialRendering.make_masked(material)
        elif material.msfs_alpha_mode == "DITHER":
            MSFSMaterialRendering.make_dither(material)
        else:
            MSFSMaterialRendering.make_opaque(material)

    @staticmethod
    def update_base_color(material, context):
        nodeBaseColorRGB = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorRGB.value
        )
        nodeBaseColorA = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorA.value
        )
        colorValue = nodeBaseColorRGB.outputs[0].default_value
        colorValue[0] = material.msfs_base_color_factor[0]
        colorValue[1] = material.msfs_base_color_factor[1]
        colorValue[2] = material.msfs_base_color_factor[2]
        nodeBaseColorA.outputs[0].default_value = material.msfs_base_color_factor[3]

        MSFSMaterialRendering.update_color_links(material)

    @staticmethod
    def update_emissive_color(material, context):
        nodeEmissiveColorRGB = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.emissiveColor.value
        )
        if not nodeEmissiveColorRGB:
            return
        emissiveValue = nodeEmissiveColorRGB.outputs[0].default_value
        emissiveValue[0] = material.msfs_emissive_factor[0]
        emissiveValue[1] = material.msfs_emissive_factor[1]
        emissiveValue[2] = material.msfs_emissive_factor[2]

    @staticmethod
    def update_emissive_scale(material, context):
        emissiveScale = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.emissiveScale.value
        )
        if not emissiveScale:
            return
        emissiveScale.outputs[0].default_value = material.msfs_emissive_scale

    @staticmethod
    def update_metallic_scale(material, context):
        nodeMetallicScale = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.metallicScale.value
        )
        nodeMetallicScale.outputs[0].default_value = material.msfs_metallic_factor
        MSFSMaterialRendering.update_comp_links(material)

    @staticmethod
    def update_roughness_scale(material, context):
        nodeRoughnessScale = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.roughnessScale.value
        )
        nodeRoughnessScale.outputs[0].default_value = material.msfs_roughness_factor
        MSFSMaterialRendering.update_comp_links(material)

    @staticmethod
    def update_normal_scale(material, context):
        node = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.normalScale.value
        )
        if node:
            node.outputs[0].default_value = material.msfs_normal_scale

    @staticmethod
    def update_color_sss(material, context):
        if material.node_tree.nodes.get("bsdf", None) != None:
            material.node_tree.nodes["bsdf"].inputs.get(
                "Subsurface Color"
            ).default_value = material.msfs_sss_color

    @staticmethod
    def update_double_sided(material, context):
        material.use_backface_culling = not material.msfs_double_sided

    @staticmethod
    def update_alpha_cutoff(material, context):
        material.alpha_threshold = material.msfs_alpha_cutoff

    @staticmethod
    def update_detail_uv(material, context):
        detailUvScaleNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailUVScale.value
        )
        detailUvOffsetUNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailUVOffsetU.value
        )
        detailUvOffsetVNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailUVOffsetV.value
        )
        detailNormalScaleNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailNormalScale.value
        )
        if (
            detailUvScaleNode
            and detailUvOffsetUNode
            and detailUvOffsetVNode
            and detailNormalScaleNode
        ):
            detailUvScaleNode.outputs[0].default_value = material.msfs_detail_uv_scale
            detailUvOffsetUNode.outputs[
                0
            ].default_value = material.msfs_detail_uv_offset_u
            detailUvOffsetVNode.outputs[
                0
            ].default_value = material.msfs_detail_uv_offset_v
            detailNormalScaleNode.outputs[
                0
            ].default_value = material.msfs_detail_normal_scale


class MSFSMaterialRendering:
    bl_label = "MSFS Shader Node Tree"

    @staticmethod
    def revert_to_default_tree(material):
        MSFSMaterialRendering.clean_node_tree(material)
        MSFSMaterialRendering.create_default_tree(material)

    @staticmethod
    def build_node_tree(material):
        MSFSMaterialRendering.clean_node_tree(material)
        MSFSMaterialRendering.create_node_tree(material)

    @staticmethod
    def clean_node_tree(material):
        nodes = material.node_tree.nodes

        for node in nodes:
            nodes.remove(node)

    @staticmethod
    def create_default_tree(material):
        nodeOutputMaterial = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeOutputMaterial",
            {"location": (1000.0, 0.0), "hide": False},
        )
        nodebsdf = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeBsdfPrincipled",
            {"location": (500.0, 0.0), "hide": False},
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["Principled BSDF"].outputs[0]',
            'nodes["Material Output"].inputs[0]',
        )
        MSFSMaterialRendering.make_opaque(material)

    @staticmethod
    def create_node_tree(material):
        nodeOutputMaterial = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeOutputMaterial",
            {"location": (1000.0, 0.0), "hide": False},
        )
        nodebsdf = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeBsdfPrincipled",
            {"location": (500.0, 0.0), "hide": False},
        )
        gltfSettingsNodeTree = bpy.data.node_groups.new(
            "glTF Settings", "ShaderNodeTree"
        )
        gltfSettingsNodeTree.nodes.new("NodeGroupInput")
        gltfSettingsNodeTree.inputs.new("NodeSocketFloat", "Occlusion")
        gltfSettingsNodeTree.inputs[0].default_value = 1.000
        nodeglTFSettings = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeGroup",
            {
                "location": (500.0, -800.0),
                "hide": False,
                "name": MSFS_ShaderNodes.glTFSettings.value,
            },
        )
        nodeglTFSettings.node_tree = gltfSettingsNodeTree
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["Principled BSDF"].outputs[0]',
            'nodes["Material Output"].inputs[0]',
        )
        MSFSMaterialRendering.make_opaque(material)

        # NODES

        # inputs
        nodeBaseColorTex = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.baseColorTex.value, "location": (-500, 100.0)},
        )
        nodeBaseColorRGB = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeRGB",
            {"name": MSFS_ShaderNodes.baseColorRGB.value, "location": (-500, 50.0)},
        )
        nodeBaseColorA = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.baseColorA.value, "location": (-500, -200.0)},
        )
        nodeBaseColorA.outputs[0].default_value = 1
        nodeCompTex = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.compTex.value, "location": (-800, -300.0)},
        )
        nodeMetallicScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.metallicScale.value, "location": (-500, -400.0)},
        )
        nodeRoughnessScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.roughnessScale.value, "location": (-500, -500.0)},
        )
        nodeEmissiveTex = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.emissiveTex.value, "location": (-500, -600.0)},
        )
        nodeemissiveColor = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeRGB",
            {"name": MSFS_ShaderNodes.emissiveColor.value, "location": (-500, -700.0)},
        )
        nodeEmissiveScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.emissiveScale.value, "location": (-500, -800.0)},
        )
        nodeNormalTex = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.normalTex.value, "location": (-500, -900.0)},
        )
        nodeNormalScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.normalScale.value, "location": (-500, -1000.0)},
        )
        nodeDetailColor = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.detailColorTex.value, "location": (-500, 0.0)},
        )
        nodeDetailCompTex = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.detailCompTex.value, "location": (-800, -350.0)},
        )
        nodeDetailNormal = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {
                "name": MSFS_ShaderNodes.detailNormalTex.value,
                "location": (-500, -1300.0),
            },
        )
        nodeNormalScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {
                "name": MSFS_ShaderNodes.detailNormalScale.value,
                "location": (-500, -1400.0),
            },
        )
        nodeBlendMask = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeTexImage",
            {"name": MSFS_ShaderNodes.blendMaskTex.value, "location": (-500, -1500.0)},
        )
        nodeDetailUVScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {"name": MSFS_ShaderNodes.detailUVScale.value, "location": (-1350, -600.0)},
        )
        nodeDetailUVOffsetU = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {
                "name": MSFS_ShaderNodes.detailUVOffsetU.value,
                "location": (-1350, -700.0),
            },
        )
        nodeDetailUVOffsetV = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeValue",
            {
                "name": MSFS_ShaderNodes.detailUVOffsetV.value,
                "location": (-1350, -800.0),
            },
        )
        vertexColor = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeVertexColor",
            {"name": MSFS_ShaderNodes.vertexColor.value, "location": (-1350, -200.0)},
        )

        # uv
        uvMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeUVMap",
            {"name": MSFS_ShaderNodes.uvMap.value, "location": (-1350, -500.0)},
        )
        combineVectorScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeCombineXYZ",
            {
                "name": MSFS_ShaderNodes.combineUVScale.value,
                "location": (-1100, -550.0),
            },
        )
        combineVectorOffset = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeCombineXYZ",
            {
                "name": MSFS_ShaderNodes.combineUVOffset.value,
                "location": (-1100, -600.0),
            },
        )
        mulUVScale = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeVectorMath",
            {
                "name": MSFS_ShaderNodes.mulUVScale.value,
                "operation": "MULTIPLY",
                "location": (-900, -500.0),
            },
        )
        addUVOffset = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeVectorMath",
            {
                "name": MSFS_ShaderNodes.addUVOffset.value,
                "operation": "ADD",
                "location": (-800, -600.0),
            },
        )

        # basecolor operators
        mulBaseColorRGBNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMixRGB",
            {
                "name": MSFS_ShaderNodes.baseColorMulRGB.value,
                "blend_type": "MULTIPLY",
                "location": (0, 50.0),
            },
        )
        mulBaseColorRGBNode.inputs[0].default_value = 1
        mulBaseColorANode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMath",
            {
                "name": MSFS_ShaderNodes.baseColorMulA.value,
                "operation": "MULTIPLY",
                "location": (0, -100.0),
            },
        )

        # emissive operators
        mulEmissiveNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMixRGB",
            {"name": MSFS_ShaderNodes.emissiveMul.value, "location": (0.0, -550.0)},
        )

        # comp operators
        splitCompNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeSeparateRGB",
            {"name": MSFS_ShaderNodes.compSeparate.value, "location": (-250.0, -300.0)},
        )
        mulOcclNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMath",
            {
                "name": MSFS_ShaderNodes.occlusionMul.value,
                "operation": "MULTIPLY",
                "location": (0, -200.0),
            },
        )
        mulOcclNode.inputs[0].default_value = 1.0
        mulMetalNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMath",
            {
                "name": MSFS_ShaderNodes.roughnessMul.value,
                "operation": "MULTIPLY",
                "location": (0, -300.0),
            },
        )
        mulMetalNode.inputs[0].default_value = 1.0
        mulRoughNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMath",
            {
                "name": MSFS_ShaderNodes.metallicMul.value,
                "operation": "MULTIPLY",
                "location": (0, -400.0),
            },
        )
        mulRoughNode.inputs[0].default_value = 1.0

        # normal operators
        normalMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeNormalMap",
            {"name": MSFS_ShaderNodes.normalMap.value, "location": (0.0, -900.0)},
        )

        # detail alpha Operator
        blendAlphaMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMath",
            {
                "name": MSFS_ShaderNodes.blendAlphaMap.value,
                "operation": "MULTIPLY",
                "location": (-150, 0.0),
            },
        )
        blendAlphaMapNode.inputs[0].default_value = 1.0
        # detail color operators
        blendColorMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMixRGB",
            {
                "name": MSFS_ShaderNodes.blendColorMap.value,
                "blend_type": "MULTIPLY",
                "location": (-150, 100.0),
            },
        )
        blendColorMapNode.inputs[0].default_value = 1.0

        # detail comp operators
        blendCompMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMixRGB",
            {
                "name": MSFS_ShaderNodes.blendCompMap.value,
                "blend_type": "MULTIPLY",
                "location": (-500, -325.0),
            },
        )
        blendCompMapNode.inputs[0].default_value = 1.0

        # detail normal operators
        detailNormalMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeNormalMap",
            {
                "name": MSFS_ShaderNodes.detailNormalMap.value,
                "location": (0.0, -1300.0),
            },
        )
        blendNormalMapNode = MSFSMaterialRendering.add_node(
            material,
            "ShaderNodeMixRGB",
            {
                "name": MSFS_ShaderNodes.blendNormalMap.value,
                "blend_type": "ADD",
                "location": (200, -1100.0),
            },
        )
        blendNormalMapNode.inputs[0].default_value = 1.0

        # LINKS

        MSFSMaterialRendering.toggle_vertex_blend_map_mask(
            material, material.msfs_blend_mask_texture is None
        )

        MSFSMaterialRendering.update_color_links(material)
        MSFSMaterialRendering.update_comp_links(material)

        # uv
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.combineUVScale.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.combineUVScale.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.combineUVScale.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVOffsetU.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.combineUVOffset.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVOffsetV.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.combineUVOffset.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.uvMap.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.mulUVScale.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.combineUVScale.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.mulUVScale.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.mulUVScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.combineUVOffset.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.addUVOffset.value),
        )

        # emissive
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.emissiveMul.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveColor.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.emissiveMul.value),
        )

        # blend normal
        # !!!! input orders matters for the exporter here
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalMap.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendNormalMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalMap.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendNormalMap.value),
        )

        # normal
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.normalMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.normalMap.value),
        )

        # detail uv
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailColorTex.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailCompTex.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailNormalTex.value),
        )

        # detail normal
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.detailNormalMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailNormalMap.value),
        )

        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value),
            'nodes["{0}"].inputs[22]'.format(MSFS_ShaderNodes.principledBSDF.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveMul.value),
            'nodes["{0}"].inputs[19]'.format(MSFS_ShaderNodes.principledBSDF.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveScale.value),
            'nodes["{0}"].inputs[20]'.format(MSFS_ShaderNodes.principledBSDF.value),
        )

    @staticmethod
    def update_color_links(material):
        # relink nodes

        nodeBaseColorRGB = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorRGB.value
        )
        nodeBaseColorA = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorA.value
        )
        nodeBaseColorTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorTex.value
        )
        nodeDetailColor = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailColorTex.value
        )
        mulBaseColorRGBNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorMulRGB.value
        )
        mulBaseColorANode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.baseColorMulA.value
        )
        blendColorMapNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.blendColorMap.value
        )
        blendAlphaMapNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.blendAlphaMap.value
        )

        # !!!! input orders matters for the exporter here
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendColorMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailColorTex.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendColorMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.baseColorMulRGB.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.baseColorTex.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendAlphaMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.detailColorTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendAlphaMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorA.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulA.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorRGB.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulRGB.value),
        )

        if not nodeBaseColorTex.image and not nodeDetailColor.image:
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorRGB.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorA.value),
                'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        elif nodeBaseColorTex.image and not nodeDetailColor.image:
            blendColorMapNode.blend_type = "ADD"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(
                    MSFS_ShaderNodes.baseColorMulRGB.value
                ),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.baseColorTex.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),
                'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        elif not nodeBaseColorTex.image and nodeDetailColor.image:
            blendColorMapNode.blend_type = "ADD"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(
                    MSFS_ShaderNodes.baseColorMulRGB.value
                ),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.detailColorTex.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),
                'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        else:
            blendColorMapNode.blend_type = "MULTIPLY"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(
                    MSFS_ShaderNodes.baseColorMulRGB.value
                ),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendAlphaMap.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),
            )

    @staticmethod
    def update_comp_links(material):
        nodeCompTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.compTex.value
        )
        nodeDetailCompTex = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.detailCompTex.value
        )
        nodeRoughnessScale = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.roughnessScale.value
        )
        nodeMetallicScale = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.metallicScale.value
        )
        blendCompMapNode = MSFSMaterialRendering.get_node(
            material, MSFS_ShaderNodes.blendCompMap.value
        )

        # blend comp
        # !!!! input orders matters for the exporter here
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compTex.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendCompMap.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailCompTex.value),
            'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendCompMap.value),
        )

        # occlMetalRough
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.compSeparate.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessScale.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compSeparate.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.occlusionMul.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.compSeparate.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.roughnessMul.value),
        )
        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[2]'.format(MSFS_ShaderNodes.compSeparate.value),
            'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.metallicMul.value),
        )

        if not nodeCompTex.image and not nodeDetailCompTex.image:
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessScale.value),
                'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicScale.value),
                'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        elif nodeCompTex.image and not nodeDetailCompTex.image:
            blendCompMapNode.blend_type = "ADD"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),
                'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),
                'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        elif not nodeCompTex.image and nodeDetailCompTex.image:
            blendCompMapNode.blend_type = "ADD"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),
                'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),
                'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
        else:
            blendCompMapNode.blend_type = "MULTIPLY"
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),
                'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),
                'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value),
            )

        MSFSMaterialRendering.inner_link(
            material,
            'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.occlusionMul.value),
            'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.glTFSettings.value),
        )

    @staticmethod
    def toggle_vertex_blend_map_mask(material, useVertex=True):
        # vertexcolor mask
        if useVertex:
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value),
            )
        else:
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value),
            )
            MSFSMaterialRendering.inner_link(
                material,
                'nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value),
                'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value),
            )

    @staticmethod
    def value_set(obj, path, value):
        if "." in path:
            path_prop, path_attr = path.rsplit(".", 1)
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            path_attr = path
        setattr(prop, path_attr, value)

    @staticmethod
    def add_node(material, nodetype, attrs):
        node = material.node_tree.nodes.new(nodetype)
        # make sure label and name are the same
        if "name" in attrs and "label" not in attrs:
            attrs["label"] = attrs["name"]
        if "hide" not in attrs:
            attrs["hide"] = True
        for attr in attrs:
            MSFSMaterialRendering.value_set(node, attr, attrs[attr])
        return node

    @staticmethod
    def get_node(material, nodename):
        if material.node_tree.nodes.find(nodename) > -1:
            return material.node_tree.nodes[nodename]
        return None

    @staticmethod
    def inner_link(material, socketin, socketout):
        SI = material.node_tree.path_resolve(socketin)
        SO = material.node_tree.path_resolve(socketout)
        material.node_tree.links.new(SI, SO)

    @staticmethod
    def free(material):
        if material.node_tree.users == 1:
            bpy.data.node_groups.remove(material.node_tree, do_unlink=True)

    @staticmethod
    def make_opaque(material):
        material.blend_method = "OPAQUE"

    @staticmethod
    def make_masked(material):
        material.blend_method = "CLIP"

    @staticmethod
    def make_alpha_blend(material):
        material.blend_method = "BLEND"

    @staticmethod
    def make_dither(material):
        # Since Eevee doesn't provide a dither mode, we'll just use alpha-blend instead.
        # It sucks, but what else is there to do?
        material.blend_method = "BLEND"
