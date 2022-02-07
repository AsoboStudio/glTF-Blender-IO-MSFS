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

class MSFS_MaterialProperties(Enum):
    baseColor = 0, 'Base Color'
    emissive = 1, 'Emissive'
    metallic = 2, 'Metallic'
    roughness = 3, 'Roughness'
    alphaCutoff = 4, 'Alpha Cutoff'
    normalScale = 5, 'Normal Scale'
    detailUVScale= 6, 'Detail UV Scale'
    detailUVOffsetU= 7, 'Detail UV Offset U'
    detailUVOffsetV= 8, 'Detail UV Offset V'
    detailNormalScale= 9, 'Detail Normal Scale'
    blendThreshold= 10, 'Blend Threshold'
    emissiveMutliplier = 11 , "Emissive Mutliplier"
    alphaMode = 12, 'Alpha Mode'
    drawOrder = 13, 'Draw Order'
    dontCastShadows = 14, "Don't cast shadows"
    doubleSided = 15, 'Double Sided'
    dayNightCycle = 16, 'Day Night Cycle'
    collisionMaterial = 17, 'Collision Material'
    roadCollisionMaterial = 18, 'Road Collision Material'
    uvOffsetU = 19,'UV Offset U'
    uvOffsetV = 20,'UV Offset V'
    uvTilingU = 21,'UV Tiling U'
    uvTilingV = 22,'UV Tiling V'
    uvClampU = 23,"UV Clamp U"
    uvClampV = 24,"UV Clamp V"
    usePearlEffect = 25, 'Use Pearl Effect'
    pearlColorShift = 26, 'Color Shift'
    pearlColorRange = 27, 'Color Range'
    pearlColorBrightness = 28, 'Color Brightness'
    baseColorTex = 29, 'Base Color Texture'
    occlRoughMetalTex = 30, 'Occlusion(R) Roughness(G) Metallic(B) Texture'
    normalTex = 31,  'Normal Texture'
    emissiveTex = 32, 'Emissive Texture'
    detailColorAlphaTex = 33, 'Detail Color (RGB) Alpha(A) Texture'
    detailOcclRoughMetalTex = 34, 'Detail Occlusion(R) Roughness(G) Metallic(B) Texture'
    detailNormalTex = 35, 'Detail Normal Texture'
    blendMaskTex = 36, 'Blend Mask Texture'

    def index(self):
        return self.value[0]

    def name(self):
        return self.value[1]

class MSFS_ShaderNodes(Enum):
    materialOutput= 'Material Output'
    principledBSDF = 'Principled BSDF'
    glTFSettings = 'glTF Settings'
    baseColorTex = 'Base Color Texture'
    baseColorRGB = 'Base Color RGB'
    baseColorA = 'Base Color A'
    alphaCutoff = 'Alpha Cutoff'
    baseColorMulRGB = 'Base Color Multiplier RGB'
    baseColorMulA = 'Base Color Multiplier A'
    normalTex = 'Normal Texture'
    normalScale = 'Normal Scale'
    compTex = 'Occlusion(R) Roughness(G) Metallic(B)'
    compSeparate = 'SplitOcclMetalRough'
    roughnessScale = 'Roughness Scale'
    metallicScale = 'Metallic Scale'
    occlusionMul = 'Occlusion Multiplier'
    roughnessMul = 'Roughness Multiplier'
    metallicMul = 'Metallic Multiplier'
    emissiveTex = 'Emissive Texture'
    emissiveColor = "Emissive RGB"
    emissiveScale = 'Emissive Scale'
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
    blendCompMap = "Blend Occlusion(R) Roughness(G) Metallic(B) Map"
    vertexColor = "Vertex Color"

class MSFS_Material():

    bl_idname = 'MSFS_ShaderNodeTree'
        # Label for nice name display
    bl_label = "MSFS Shader Node Tree"

    bl_icon = 'SOUND'

    def __init__(self,material):
        self.material = material
        self.node_tree = self.material.node_tree
        self.nodes = self.material.node_tree.nodes
        self.links = material.node_tree.links
        

    def buildShaderTree(self): 
        self.cleanNodeTree()
        self.displayParams()
        self.createNodetree()
        self.refresh()       
        

    def cleanNodeTree(self):
        nodes = self.material.node_tree.nodes

        for idx,node in enumerate(nodes):
            print("Deleting: %s | %s"%(node.name,node.type))
            nodes.remove(node)

    def refresh(self):
        self.material.msfs_blend_mode = self.material.msfs_blend_mode
        self.material.msfs_color_albedo_mix = self.material.msfs_color_albedo_mix
        self.material.msfs_color_emissive_mix = self.material.msfs_color_emissive_mix
        self.material.msfs_roughness_scale = self.material.msfs_roughness_scale
        self.material.msfs_metallic_scale = self.material.msfs_metallic_scale
        self.material.msfs_normal_scale = self.material.msfs_normal_scale
        self.material.msfs_alpha_cutoff = self.material.msfs_alpha_cutoff
        self.material.msfs_detail_uv_scale = self.material.msfs_detail_uv_scale
        self.material.msfs_detail_uv_offset_x = self.material.msfs_detail_uv_offset_x
        self.material.msfs_detail_uv_offset_y = self.material.msfs_detail_uv_offset_y
        self.material.msfs_detail_normal_scale = self.material.msfs_detail_normal_scale
        self.material.msfs_blend_threshold = self.material.msfs_blend_threshold
        
        self.material.msfs_albedo_texture = self.material.msfs_albedo_texture
        self.material.msfs_metallic_texture = self.material.msfs_metallic_texture
        self.material.msfs_normal_texture = self.material.msfs_normal_texture
        self.material.msfs_metallic_texture = self.material.msfs_metallic_texture
        self.material.msfs_emissive_texture = self.material.msfs_emissive_texture
        self.material.msfs_detail_albedo_texture = self.material.msfs_detail_albedo_texture
        self.material.msfs_detail_metallic_texture = self.material.msfs_detail_metallic_texture
        self.material.msfs_detail_normal_texture = self.material.msfs_detail_normal_texture
        self.material.msfs_blend_mask_texture = self.material.msfs_blend_mask_texture

    def displayParams(self):
        self.material.msfs_show_tint = False
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

    def createNodetree(self):
        self.nodeOutputMaterial = self.addNode('ShaderNodeOutputMaterial', {'location':(1000.0,0.0),'hide' : False })
        self.nodebsdf = self.addNode('ShaderNodeBsdfPrincipled', {'location':(500.0,0.0), 'hide' : False})
        gltfSettingsNodeTree = bpy.data.node_groups.new('glTF Settings', 'ShaderNodeTree')
        gltfSettingsNodeTree.nodes.new('NodeGroupInput')
        gltfSettingsNodeTree.inputs.new('NodeSocketFloat','Occlusion')
        gltfSettingsNodeTree.inputs[0].default_value = (1.000)
        self.nodeglTFSettings = self.addNode('ShaderNodeGroup', {'location':(500.0,-800.0), 'hide' : False, 'name': MSFS_ShaderNodes.glTFSettings.value}) #CreateNewNode(Material,'ShaderNodeGroup',location=(offset[0]+1000,offset[1]+50))
        self.nodeglTFSettings.node_tree = gltfSettingsNodeTree
        self.innerLink('nodes["Principled BSDF"].outputs[0]', 'nodes["Material Output"].inputs[0]')
        self.makeOpaque()
        self.customShaderTree()

    def customShaderTree(self):
        raise NotImplementedError()

    def defaultShaderStree(self):
        
        #NODES

        #inputs
        self.nodeBaseColorTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.baseColorTex.value,'location':(-500,100.0)})  
        self.nodeBaseColorRGB = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.baseColorRGB.value,'location':(-500,50.0)})
        self.nodeBaseColorA = self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.baseColorA.value,'location':(-500,-200.0)})
        self.nodeBaseColorA.outputs[0].default_value = 1
        self.nodeCompTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.compTex.value,'location':(-800,-300.0)})
        self.nodeMetallicScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.metallicScale.value,'location':(-500,-400.0)})
        self.nodeRoughnessScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.roughnessScale.value,'location':(-500,-500.0)})
        self.nodeEmissiveTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.emissiveTex.value,'location':(-500,-600.0)})
        self.nodeemissiveColor = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.emissiveColor.value,'location':(-500,-700.0)})
        self.nodeEmissiveScale = self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.emissiveScale.value,'location':(-500,-800.0)})
        self.nodeNormalTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.normalTex.value,'location':(-500,-900.0)})
        self.nodeNormalScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.normalScale.value,'location':(-500,-1000.0)})
        self.nodeDetailColor =self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.detailColorTex.value,'location':(-500,0.0)})
        self.nodeDetailComp =self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.detailCompTex.value,'location':(-800,-350.0)})
        self.nodeDetailNormal =self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.detailNormalTex.value,'location':(-500,-1300.0)})
        self.nodeNormalScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.detailNormalScale.value,'location':(-500,-1400.0)})
        self.nodeBlendMask =self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.blendMaskTex.value,'location':(-500,-1500.0)})
        self.nodeDetailUVScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.detailUVScale.value,'location':(-1350,-600.0)})
        self.nodeDetailUVOffsetU =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.detailUVOffsetU.value,'location':(-1350,-700.0)})
        self.nodeDetailUVOffsetV =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.detailUVOffsetV.value,'location':(-1350,-800.0)})
        self.vertexColor = self.addNode('ShaderNodeVertexColor', { 'name': MSFS_ShaderNodes.vertexColor.value, 'location':(-1350,-200.0)})



        #uv
        uvMapNode =  self.addNode('ShaderNodeUVMap', { 'name':MSFS_ShaderNodes.uvMap.value , 'location':(-1350,-500.0) })
        combineVectorScale =  self.addNode('ShaderNodeCombineXYZ', { 'name':MSFS_ShaderNodes.combineUVScale.value , 'location':(-1100,-550.0) })
        combineVectorOffset =  self.addNode('ShaderNodeCombineXYZ', { 'name':MSFS_ShaderNodes.combineUVOffset.value , 'location':(-1100,-600.0) })
        mulUVScale =  self.addNode('ShaderNodeVectorMath', { 'name':MSFS_ShaderNodes.mulUVScale.value , 'operation':'MULTIPLY', 'location':(-900,-500.0) })
        addUVOffset =  self.addNode('ShaderNodeVectorMath', { 'name':MSFS_ShaderNodes.addUVOffset.value , 'operation':'ADD','location':(-800,-600.0) })

        #basecolor operators 
        mulBaseColorRGBNode =self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.baseColorMulRGB.value ,'blend_type':'MULTIPLY', 'location':(-150,50.0) })
        mulBaseColorRGBNode.inputs[0].default_value = 1
        mulBaseColorANode =self.addNode('ShaderNodeMath', { 'name':MSFS_ShaderNodes.baseColorMulA.value ,'operation':'MULTIPLY','location':(0,-100.0)})
        
        
        #emissive operators
        mulEmissiveNode = self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.emissiveMul.value,'location':(0.0,-550.0) })

        #comp operators
        splitCompNode= self.addNode('ShaderNodeSeparateRGB', { 'name':MSFS_ShaderNodes.compSeparate.value,'location':(-250.0,-300.0)})
        mulOcclNode=self.addNode('ShaderNodeMath', {'name':MSFS_ShaderNodes.occlusionMul.value ,'operation':'MULTIPLY','location':(0,-200.0) })
        mulOcclNode.inputs[0].default_value = 1.0
        mulMetalNode = self.addNode('ShaderNodeMath', { 'name':MSFS_ShaderNodes.roughnessMul.value ,'operation':'MULTIPLY','location':(0,-300.0) })
        mulMetalNode.inputs[0].default_value = 1.0
        mulRoughNode = self.addNode('ShaderNodeMath', { 'name':MSFS_ShaderNodes.metallicMul.value ,'operation':'MULTIPLY','location':(0,-400.0)})
        mulRoughNode.inputs[0].default_value = 1.0
        
        
        #normal operators
        normalMapNode = self.addNode('ShaderNodeNormalMap', { 'name':MSFS_ShaderNodes.normalMap.value,'location':(0.0,-900.0) })

        #detail color operators
        self.blendColorMapNode = self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.blendColorMap.value ,'blend_type':'MULTIPLY', 'location':(200,100.0) })
        self.blendColorMapNode.inputs[0].default_value = 1.0

        #detail comp operators
        blendCompMapNode = self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.blendCompMap.value ,'blend_type':'MULTIPLY', 'location':(-500,-325.0) })
        blendCompMapNode.inputs[0].default_value = 1.0

        #detail normal operators
        detailNormalMapNode = self.addNode('ShaderNodeNormalMap', { 'name':MSFS_ShaderNodes.detailNormalMap.value,'location':(0.0,-1300.0) })
        blendNormalMapNode = self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.blendNormalMap.value ,'blend_type':'ADD', 'location':(200,-1100.0) })
        blendNormalMapNode.inputs[0].default_value = 1.0
        
        #LINKS

        self.toggleVertexBlendMapMask( self.material.msfs_blend_mask_texture is None )

        #uv
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.combineUVScale.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.combineUVScale.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVScale.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.combineUVScale.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVOffsetU.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.combineUVOffset.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailUVOffsetV.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.combineUVOffset.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.uvMap.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.mulUVScale.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.combineUVScale.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.mulUVScale.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.mulUVScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.combineUVOffset.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.addUVOffset.value))

        #color RGB
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulRGB.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorRGB.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.baseColorMulRGB.value))
        #color A
        self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.baseColorTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulA.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorA.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value))
        

        #emissive
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.emissiveMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveColor.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.emissiveMul.value))


        #blend comp 
        # !!!! input orders matters for the exporter here
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendCompMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailCompTex.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendCompMap.value))

        #occlMetalRough
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.compSeparate.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.metallicMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.occlusionMul.value))
        self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.roughnessMul.value))
        self.innerLink('nodes["{0}"].outputs[2]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.metallicMul.value))
       

        #normal
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.normalMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.normalMap.value))

        #detail uv
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailColorTex.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailCompTex.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.addUVOffset.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailNormalTex.value))

        #detail normal
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.detailNormalMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.detailNormalMap.value))

        #blend color 
        # !!!! input orders matters for the exporter here
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulRGB.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendColorMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailColorTex.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendColorMap.value))

        #blend normal 
        # !!!! input orders matters for the exporter here
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalMap.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.blendNormalMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.detailNormalMap.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.blendNormalMap.value))


        #PrincipledBSDF connections
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value),      'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),      'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.occlusionMul.value),       'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.glTFSettings.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),       'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),        'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value),     'nodes["{0}"].inputs[22]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveMul.value),        'nodes["{0}"].inputs[19]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveScale.value),      'nodes["{0}"].inputs[20]'.format(MSFS_ShaderNodes.principledBSDF.value))

    def toggleVertexBlendMapMask(self, useVertex = True):

        return
        # vertexcolor mask
        if useVertex:
            self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value))
            self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value))
            self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.vertexColor.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value))
        else:
            self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendColorMap.value))
            self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendCompMap.value))
            self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.blendMaskTex.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.blendNormalMap.value))

        

    def value_set(self, obj, path, value):
        if '.' in path:
            path_prop, path_attr = path.rsplit('.', 1)
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            path_attr = path
        setattr(prop, path_attr, value)
    
    
    def addInput(self, sockettype, attrs):
        name = attrs.pop('name')
        socketInterface=self.node_tree.inputs.new(sockettype, name)
        socket=self.path_resolve(socketInterface.path_from_id())
        for attr in attrs:
            if attr in ['default_value', 'hide', 'hide_value', 'enabled']:
                self.value_set(socket, attr, attrs[attr])
            else:
                self.value_set(socketInterface, attr, attrs[attr])
        return socket
                   
    def getInputIndexByName(self,nodeName,inputName):
        node = self.getNode(nodeName)
        return node.inputs.find(inputName)

    def getOutputIndexByName(self,nodeName,outputName):
        node = self.getNode(nodeName)
        return node.outputs.find(outputName)

    def addSocket(self, is_output, sockettype, name):
        #for now duplicated socket names are not allowed
        if is_output==True:
            if self.node_tree.nodes['GroupOutput'].inputs.find(name)==-1:
                socket=self.node_tree.outputs.new(sockettype, name)
        elif is_output==False:
            if self.node_tree.nodes['GroupInput'].outputs.find(name)==-1:
                socket=self.node_tree.inputs.new(type=sockettype,name=name)
        return socket
       
    def addNode(self, nodetype, attrs):
        node=self.node_tree.nodes.new(nodetype)
        #make sure label and name are the same
        if 'name' in attrs and 'label' not in attrs:
            attrs['label'] = attrs['name'] 
        if 'hide' not in attrs:
            attrs['hide'] = True
        for attr in attrs:
            self.value_set(node, attr, attrs[attr])
        return node
   
    def getNode(self, nodename):
        if self.node_tree.nodes.find(nodename)>-1:
            return self.node_tree.nodes[nodename]
        return None
   
    def innerLink(self, socketin, socketout):
        SI=self.node_tree.path_resolve(socketin)
        SO=self.node_tree.path_resolve(socketout)
        self.node_tree.links.new(SI, SO)
       
    def free(self):
        if self.node_tree.users==1:
            bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
    
    def makeOpaque(self):
        self.material.blend_method = 'OPAQUE'

    def makeMasked(self):
        self.material.blend_method = 'CLIP'

    def makeAlphaBlend(self):
        self.material.blend_method = 'BLEND'

    def makeDither(self):
        #Since Eevee doesn't provide a dither mode, we'll just use alpha-blend instead.
        #It sucks, but what else is there to do?
        self.blend_method = 'BLEND'

    


