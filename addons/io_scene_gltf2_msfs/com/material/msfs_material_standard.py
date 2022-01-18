from .msfs_material import *


class MSFS_Standard(MSFS_Material):

    def __init__(self, material):
        super(MSFS_Standard, self).__init__(material)

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
        self.material.msfs_show_anisotropic_direction = False
        self.material.msfs_show_clearcoat = False
        self.material.msfs_show_behind_glass = False
        self.material.msfs_show_wiper_mask = False

        self.material.msfs_show_blend_mode = True
        self.material.use_backface_culling = not self.material.msfs_double_sided

        self.material.msfs_show_draworder = True
        self.material.msfs_show_no_cast_shadow = True
        self.material.msfs_show_double_sided = True
        self.material.msfs_show_responsive_aa = False
        self.material.msfs_show_day_night_cycle = True

        self.material.msfs_show_collision_material = True
        self.material.msfs_show_road_material = True

        self.material.msfs_show_ao_use_uv2 = True
        self.material.msfs_show_uv_clamp = True

        self.material.msfs_show_alpha_cutoff = True
        self.material.msfs_show_blend_threshold = True
        #New
        self.material.msfs_show_pearl = True
        self.material.msfs_show_windshield_options = False

    def refresh(self):
        self.material.msfs_albedo_texture = self.material.msfs_albedo_texture
        self.material.msfs_color_albedo_mix = self.material.msfs_color_albedo_mix

    def createNodetree(self) :
        super().createNodetree()
        # self.node_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')
        
        #NODES

        #inputs
        self.nodeBaseColorTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.baseColorTex.value,'location':(-500,0.0)})
        self.nodeBaseColorRGB = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.baseColorRGB.value,'location':(-500,-100.0)})
        self.nodeBaseColorA = self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.baseColorA.value,'location':(-500,-200.0)})
        self.nodeBaseColorA.outputs[0].default_value = 1
        self.nodeCompTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.compTex.value,'location':(-500,-300.0)})
        self.nodeMetallicScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.metallicScale.value,'location':(-500,-400.0)})
        self.nodeRoughnessScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.roughnessScale.value,'location':(-500,-500.0)})
        self.nodeEmissiveTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.emissiveTex.value,'location':(-500,-600.0)})
        self.nodeemissiveColor = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.emissiveColor.value,'location':(-500,-700.0)})
        self.nodeEmissiveScale = self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.emissiveScale.value,'location':(-500,-800.0)})
        self.nodeNormalTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.normalTex.value,'location':(-500,-900.0)})
        self.nodeNormalScale =self.addNode('ShaderNodeValue', { 'name': MSFS_ShaderNodes.normalScale.value,'location':(-500,-1000.0)})

        #basecolor operators 
        mulBaseColorRGBNode =self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.baseColorMulRGB.value ,'blend_type':'MULTIPLY', 'location':(0,0.0) })
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
        
        #LINKS

        #color RGB
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulRGB.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorRGB.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.baseColorMulRGB.value))
        #color A
        self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.baseColorTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMulA.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorA.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value))
        

        #emissive
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.emissiveMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveColor.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.emissiveMul.value))

        #occlMetalRough
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compTex.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.compSeparate.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.metallicMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.occlusionMul.value))
        self.innerLink('nodes["{0}"].outputs[1]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.roughnessMul.value))
        self.innerLink('nodes["{0}"].outputs[2]'.format(MSFS_ShaderNodes.compSeparate.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.metallicMul.value))
       

        #normal
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalTex.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.normalMap.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalScale.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.normalMap.value))



        #PrincipledBSDF connections
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulRGB.value),    'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMulA.value),      'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value))
        # self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.occlusionMul.value),       'nodes["{0}"].inputs[21]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.roughnessMul.value),       'nodes["{0}"].inputs[9]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.metallicMul.value),        'nodes["{0}"].inputs[6]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.normalMap.value),          'nodes["{0}"].inputs[22]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveMul.value),        'nodes["{0}"].inputs[19]'.format(MSFS_ShaderNodes.principledBSDF.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.emissiveScale.value),      'nodes["{0}"].inputs[20]'.format(MSFS_ShaderNodes.principledBSDF.value))