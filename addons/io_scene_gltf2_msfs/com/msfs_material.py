import bpy
from enum import Enum 

# Derived from the Node base type.

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
    baseColorTex = 'Base Color Texture'
    baseColorRGB = 'Base Color RGB'
    baseColorA = 'Base Color RGB'
    baseColorMul = 'Base Color Multiplier'


class MSFS_Material():

    def __init__(self, material):
        self.material = material
        self.node_tree = material.node_tree
        self.nodes = material.node_tree.nodes
        self.links = material.node_tree.links
        self.cleanNodeTree()
        self.displayParams()
        self.createNodetree()

    def cleanNodeTree(self):
        nodes = self.material.node_tree.nodes

        for idx,node in enumerate(nodes):
            print("Deleting: %s | %s"%(node.name,node.type))
            nodes.remove(node)

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
        self.nodeOutputMaterial = self.addNode('ShaderNodeOutputMaterial', {'location':(700.0,0.0) })
        self.nodebsdf = self.addNode('ShaderNodeBsdfPrincipled', {'location':(400.0,0.0) })

        self.innerLink('nodes["Principled BSDF"].outputs[0]', 'nodes["Material Output"].inputs[0]')

        

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

    def createNodetree(self) :
        super().createNodetree()
        # self.node_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')
        
        #NODES
        self.nodeOutputMaterial = self.addNode('ShaderNodeOutputMaterial', {'location':(700.0,0.0) })
        self.nodebsdf = self.addNode('ShaderNodeBsdfPrincipled', {'location':(400.0,0.0) })

        self.nodeBaseColorTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_ShaderNodes.baseColorTex.value})
        self.nodeBaseColorRGB = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.baseColorRGB.value })
        self.nodeBaseColorA = self.addNode('ShaderNodeRGB', { 'name': MSFS_ShaderNodes.baseColorA.value })
        
        mulBaseColorNode =self.addNode('ShaderNodeMixRGB', { 'name':MSFS_ShaderNodes.baseColorMul.value ,'blend_type':'MULTIPLY' })
        mulBaseColorNode.inputs[0].default_value = 1.0

        # nodeMulEmissive = "MulEmissive"
        # self.addNode('ShaderNodeMixRGB', { 'name':nodeMulEmissive ,'blend_type':'MULTIPLY' })

        # self.addNode('ShaderNodeSeparateRGB', { 'name':'SplitOcclMetalRough'})
        # mulOcclNode=self.addNode('ShaderNodeMixRGB', { 'name':'MulOccl' ,'blend_type':'MULTIPLY' })
        # mulOcclNode.inputs[0].default_value = 1.0
        # self.addNode('ShaderNodeMixRGB', { 'name':'MulMetal' ,'blend_type':'MULTIPLY' })
        # self.addNode('ShaderNodeMixRGB', { 'name':'MulRough' ,'blend_type':'MULTIPLY' })

        # self.addNode('ShaderNodeMixRGB', { 'name':'MulNormal' ,'blend_type':'MULTIPLY' })
        
        
        
        #LINKS
        # self.innerLink('nodes["Principled BSDF"].outputs[0]', 'nodes["Material Output"].inputs[0]')

        #color
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorTex.value), 'nodes["{0}"].inputs[2]'.format(MSFS_ShaderNodes.baseColorMul.value))
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorRGB.value), 'nodes["{0}"].inputs[1]'.format(MSFS_ShaderNodes.baseColorMul.value))
        

        # #emissive
        # self.innerLink(emissiveOutput, 'nodes["MulEmissive"].inputs[1]')
        # self.innerLink(emissiveTexOutput, 'nodes["MulEmissive"].inputs[2]')
        

        # #occlMetalRough
        # self.innerLink(roughnessOutput, 'nodes["MulRough"].inputs[1]')
        # self.innerLink(metallicOutput, 'nodes["MulMetal"].inputs[1]')
        # self.innerLink('nodes["MulBaseColor"].outputs[0]', 'nodes["MulOccl"].inputs[1]')
        # self.innerLink(occlRoughMetalTexOutput, 'nodes["SplitOcclMetalRough"].inputs[0]')
        # self.innerLink('nodes["SplitOcclMetalRough"].outputs[0]', 'nodes["MulOccl"].inputs[2]')
        # self.innerLink('nodes["SplitOcclMetalRough"].outputs[1]','nodes["MulMetal"].inputs[2]')
        # self.innerLink('nodes["SplitOcclMetalRough"].outputs[2]', 'nodes["MulRough"].inputs[2]')

        # #normal
        # self.innerLink(normalTexOutput, 'nodes["MulNormal"].inputs[1]')


        #PrincipledBSDF connections
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_ShaderNodes.baseColorMul.value), 'nodes["{0}"].inputs[0]'.format(MSFS_ShaderNodes.principledBSDF.value))

        # self.innerLink('nodes["MulEmissive"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[19]')
        # self.innerLink('nodes["MulOccl"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[0]')
        # self.innerLink('nodes["MulMetal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[6]')
        # self.innerLink('nodes["MulRough"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[9]')
        # self.innerLink('nodes["MulNormal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[22]')
