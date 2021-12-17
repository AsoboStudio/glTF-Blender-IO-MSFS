import enum
import bpy
from enum import Enum

class AlphaModeSocket(bpy.types.NodeSocket):
    # Description string
    '''Custom Radio socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'AlphaModeSocket'
    # Label for nice name display
    bl_label = "AlphaMode Socket"

    # Enum items list
    my_items = (
        ('OPAQUE', "Opaque", "Where your feet are"),
        ('MASK', "Mask", "Where your head should be"),
        ('BLEND', "Blend", "Not right"),
        ('DITHER', "Dither", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Alpha Mode",
        description="Just an example",
        items=my_items,
        default='OPAQUE',
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


class MSFS_ShaderNodeTextureSampler(bpy.types.Node, bpy.types.ShaderNodeTree):
    # === Basics ===
    # Description string
    '''A custom Texture Sampler'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'MSFS_ShaderNodeTextureSampler'
    # Label for nice name display
    bl_label = "MSFS Texture Sample"
    # Icon identifier
    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new('NodeSocketImage', "Image")
        self.inputs.new('NodeSocketVector', "UV")

        self.outputs.new('NodeSocketColor', "Color")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        pass

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        pass
   
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


class MSFS_Standard(bpy.types.ShaderNodeCustomGroup):
    bl_name='MSFS_Standard'
    bl_label='MSFS_Standard'
    bl_icon='NONE'


    def init(self, context):
        self.getNodetree(self.name + '_node_tree')
        # self.inputs.new('AlphaModeSocket', "Alpha Mode")
        
        # self.inputs['Base Color'].default_value=[1,1,1,1]
        # self.inputs['Emissive'].default_value=[0,0,0,1]

    def update(self):
        pass
        # if self.inputs['Vector'].is_linked:
        #     self.inputs['HAS_Vector'].default_value=1
        # else:    
        #     self.inputs['HAS_Vector'].default_value=0
        #     pass

    def value_set(self, obj, path, value):
        if '.' in path:
            path_prop, path_attr = path.rsplit('.', 1)
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            path_attr = path
        setattr(prop, path_attr, value)

    def createNodetree(self, name) :
        self.node_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')
        #Nodes
        self.addNode('NodeGroupInput', { 'name':'GroupInput'  })
        self.addNode('NodeGroupOutput', { 'name':'GroupOutput'  })
        self.addNode('ShaderNodeBsdfPrincipled', { 'name':'PrincipledBSDF' })

        # self.addNode('ShaderNodeMath', { 'name':'Node13' ,'inputs[1].default_value':0.5 ,'operation':'ABSOLUTE' })
        nodeMulBaseColor = "MulBaseColor"
        nodeBaseColorTexSampler = "BaseColorTexSampler"
        self.addNode('ShaderNodeMath', { 'name':nodeMulBaseColor ,'operation':'MULTIPLY' })
        self.addNode('MSFS_ShaderNodeTextureSampler', { 'name':nodeBaseColorTexSampler})

        nodeMulEmissive = "MulEmissive"
        nodeEmissiveTexSampler = "EmissiveTexSampler"
        self.addNode('ShaderNodeMath', { 'name':nodeMulEmissive ,'operation':'MULTIPLY' })
        self.addNode('MSFS_ShaderNodeTextureSampler', { 'name':nodeEmissiveTexSampler})

        self.addNode('MSFS_ShaderNodeTextureSampler', { 'name':'OcclMetalRoughSampler'})
        self.addNode('ShaderNodeSeparateRGB', { 'name':'SplitOcclMetalRough'})
        self.addNode('ShaderNodeMath', { 'name':'MulOccl' ,'operation':'MULTIPLY' })
        self.addNode('ShaderNodeMath', { 'name':'MulMetal' ,'operation':'MULTIPLY' })
        self.addNode('ShaderNodeMath', { 'name':'MulRough' ,'operation':'MULTIPLY' })

        self.addNode('ShaderNodeMath', { 'name':'MulNormal' ,'operation':'MULTIPLY' })
        self.addNode('MSFS_ShaderNodeTextureSampler', { 'name':'NormalTexSampler'})
        
        #INPUTS
        #Base
        self.addInput('NodeSocketColor', {'name':MSFS_MaterialProperties.baseColor.name(), 'default_value':[1,1,1,1]})
        self.addInput('NodeSocketColor', {'name':MSFS_MaterialProperties.emissive.name(), 'default_value':[0,0,0,1]})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.metallic.name(), 'default_value':1,'min_value':0.0, 'max_value':1.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.roughness.name(), 'default_value':1,'min_value':0.0, 'max_value':1.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.alphaCutoff.name(), 'default_value':0.5,'min_value':0.0, 'max_value':1.0, 'hide': True}) # use settings?
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.normalScale.name(), 'default_value':1,'min_value':0.0, 'max_value':1.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.detailUVScale.name(), 'default_value':2,'min_value':0.01, 'max_value':100.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.detailUVOffsetU.name(), 'default_value':0,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.detailUVOffsetV.name(), 'default_value':0,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.detailNormalScale.name(), 'default_value':1,'min_value':0.0, 'max_value':1.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.blendThreshold.name(), 'default_value':0.1,'min_value':0.001, 'max_value':1.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.emissiveMutliplier.name(), 'default_value':1,'min_value':0.0, 'max_value':100, 'hide': True})
        #Alpha Mode
        self.addInput('AlphaModeSocket', {'name':MSFS_MaterialProperties.alphaMode.name(), 'hide': True}) # use settings?

        #Render Param
        self.addInput('NodeSocketInt',  {'name':MSFS_MaterialProperties.drawOrder.name(), 'default_value':0,'min_value':-999, 'max_value':999, 'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.dontCastShadows.name(), 'default_value':False,'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.doubleSided.name(), 'default_value':False,'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.dayNightCycle.name(), 'default_value':False,'hide': True})
        #Gameplay Param
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.collisionMaterial.name(), 'default_value':False,'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.roadCollisionMaterial.name(), 'default_value':False,'hide': True})
        #UVs Options
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.uvOffsetU.name(), 'default_value':0,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.uvOffsetV.name(), 'default_value':0,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.uvTilingU.name(), 'default_value':1,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.uvTilingV.name(), 'default_value':1,'min_value':-10.0, 'max_value':10.0, 'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.uvClampU.name(), 'default_value':False,'hide': True})
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.uvClampV.name(), 'default_value':False,'hide': True})
        #Pearl Param
        self.addInput('NodeSocketBool', {'name':MSFS_MaterialProperties.usePearlEffect.name(), 'default_value':False,'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.pearlColorShift.name(), 'default_value':0,'min_value':-999.0, 'max_value':999.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.pearlColorRange.name(), 'default_value':0,'min_value':-999.0, 'max_value':999.0, 'hide': True})
        self.addInput('NodeSocketFloat', {'name':MSFS_MaterialProperties.pearlColorBrightness.name(), 'default_value':0,'min_value':-1.0, 'max_value':1.0, 'hide': True})
        #textures
        
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.baseColorTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.occlRoughMetalTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.normalTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.emissiveTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.detailColorAlphaTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.detailOcclRoughMetalTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.detailNormalTex.name())
        self.addSocket(False, 'NodeSocketImage', MSFS_MaterialProperties.blendMaskTex.name())
        
        #LINKS
        #GroupInput indexes
        baseColorIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.baseColor.name())
        emissiveIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.emissive.name())
        metallicIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.metallic.name())
        roughnessIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.roughness.name())
        alphaCutoffIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.alphaCutoff.name())
        normalScaleIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.normalScale.name())
        detailUVScaleIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailUVScale.name())
        detailUVOffsetUIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailUVOffsetU.name())
        detailUVOffsetVIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailUVOffsetU.name())
        detailNormalScaleIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailNormalScale.name())
        blendThresholdIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.blendThreshold.name())
        emissiveMutliplierIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.emissiveMutliplier.name())
        alphaModeIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.alphaMode.name())
        drawOrderIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.drawOrder.name())
        dontCastShadowsIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.dontCastShadows.name())
        doubleSidedIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.doubleSided.name())
        dayNightCycleIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.dayNightCycle.name())
        collisionMaterialIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.collisionMaterial.name())
        roadCollisionMaterialIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.roadCollisionMaterial.name())
        uvOffsetUIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvOffsetU.name())
        uvOffsetVIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvOffsetV.name())
        uvTilingUIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvTilingU.name())
        uvTilingVIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvTilingV.name())
        uvClampUIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvClampU.name())
        uvClampVIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.uvClampV.name())
        usePearlEffectIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.usePearlEffect.name())
        pearlColorShiftIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.pearlColorShift.name())
        pearlColorRangeIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.pearlColorRange.name())
        pearlColorBrightnessIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.pearlColorBrightness.name())
        baseColorTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.baseColorTex.name())
        occlRoughMetalTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.occlRoughMetalTex.name())
        normalTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.normalTex.name())
        emissiveTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.emissiveTex.name())
        detailColorAlphaTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailColorAlphaTex.name())
        detailOcclRoughMetalTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailOcclRoughMetalTex.name())
        detailNormalTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.detailNormalTex.name())
        blendMaskTexIndex = self.getOutputIndexByName("GroupInput",MSFS_MaterialProperties.blendMaskTex.name())

        #GroupInput outputs
        baseColorOutput = self.getGroupInputOutputPath(baseColorIndex)
        emissiveOutput = self.getGroupInputOutputPath(emissiveIndex)
        metallicOutput = self.getGroupInputOutputPath(metallicIndex)
        roughnessOutput = self.getGroupInputOutputPath(roughnessIndex)
        alphaCutoffOutput = self.getGroupInputOutputPath(alphaCutoffIndex)
        normalScaleOutput = self.getGroupInputOutputPath(normalScaleIndex)
        detailUVScaleOutput = self.getGroupInputOutputPath(detailUVScaleIndex)
        detailUVOffsetUOutput = self.getGroupInputOutputPath(detailUVOffsetUIndex)
        detailUVOffsetVOutput = self.getGroupInputOutputPath(detailUVOffsetVIndex)
        detailNormalScaleOutput = self.getGroupInputOutputPath(detailNormalScaleIndex)
        blendThresholdOutput = self.getGroupInputOutputPath(blendThresholdIndex)
        emissiveMutliplierOutput = self.getGroupInputOutputPath(emissiveMutliplierIndex)
        alphaModeOutput = self.getGroupInputOutputPath(alphaModeIndex)
        drawOrderOutput = self.getGroupInputOutputPath(drawOrderIndex)
        dontCastShadowsOutput = self.getGroupInputOutputPath(dontCastShadowsIndex)
        doubleSidedOutput = self.getGroupInputOutputPath(doubleSidedIndex)
        dayNightCycleOutput = self.getGroupInputOutputPath(dayNightCycleIndex)
        collisionMaterialOutput = self.getGroupInputOutputPath(collisionMaterialIndex)
        roadCollisionMaterialOutput = self.getGroupInputOutputPath(roadCollisionMaterialIndex)
        uvOffsetUOutput = self.getGroupInputOutputPath(uvOffsetUIndex)
        uvOffsetVOutput = self.getGroupInputOutputPath(uvOffsetVIndex)
        uvTilingUOutput = self.getGroupInputOutputPath(uvTilingUIndex)
        uvTilingVOutput = self.getGroupInputOutputPath(uvTilingVIndex)
        uvClampUOutput = self.getGroupInputOutputPath(uvClampUIndex)
        uvClampVOutput = self.getGroupInputOutputPath(uvClampVIndex)
        usePearlEffectOutput = self.getGroupInputOutputPath(usePearlEffectIndex)
        pearlColorShiftOutput = self.getGroupInputOutputPath(pearlColorShiftIndex)
        pearlColorRangeOutput = self.getGroupInputOutputPath(pearlColorRangeIndex)
        pearlColorBrightnessOutput = self.getGroupInputOutputPath(pearlColorBrightnessIndex)
        baseColorTexOutput = self.getGroupInputOutputPath(baseColorTexIndex)
        occlRoughMetalTexOutput = self.getGroupInputOutputPath(occlRoughMetalTexIndex)
        normalTexOutput = self.getGroupInputOutputPath(normalTexIndex)
        emissiveTexOutput = self.getGroupInputOutputPath(emissiveTexIndex)
        detailColorAlphaTexOutput = self.getGroupInputOutputPath(detailColorAlphaTexIndex)
        detailOcclRoughMetalTexOutput = self.getGroupInputOutputPath(detailOcclRoughMetalTexIndex)
        detailNormalTexOutput = self.getGroupInputOutputPath(detailNormalTexIndex)
        blendMaskTexOutput = self.getGroupInputOutputPath(blendMaskTexIndex)

        #connections
        self.innerLink('nodes["PrincipledBSDF"].outputs[0]', 'nodes["GroupOutput"].inputs[0]')

        #color
        self.innerLink(baseColorOutput, 'nodes["MulBaseColor"].inputs[0]')
        self.innerLink(baseColorTexOutput, 'nodes["BaseColorTexSampler"].inputs[0]')
        self.innerLink('nodes["BaseColorTexSampler"].outputs[0]', 'nodes["MulBaseColor"].inputs[1]')
        

        #emissive
        self.innerLink(emissiveOutput, 'nodes["MulEmissive"].inputs[0]')
        self.innerLink(emissiveTexOutput, 'nodes["EmissiveTexSampler"].inputs[0]')
        self.innerLink('nodes["EmissiveTexSampler"].outputs[0]', 'nodes["MulEmissive"].inputs[1]')
        

        #occlMetalRough
        self.innerLink(roughnessOutput, 'nodes["MulRough"].inputs[0]')
        self.innerLink(metallicOutput, 'nodes["MulMetal"].inputs[0]')
        self.innerLink('nodes["MulBaseColor"].outputs[0]', 'nodes["MulOccl"].inputs[0]')
        self.innerLink(occlRoughMetalTexOutput, 'nodes["OcclMetalRoughSampler"].inputs[0]')
        self.innerLink('nodes["OcclMetalRoughSampler"].outputs[0]', 'nodes["SplitOcclMetalRough"].inputs[0]')
        self.innerLink('nodes["SplitOcclMetalRough"].outputs[0]', 'nodes["MulOccl"].inputs[1]')
        self.innerLink('nodes["SplitOcclMetalRough"].outputs[1]','nodes["MulMetal"].inputs[1]')
        self.innerLink('nodes["SplitOcclMetalRough"].outputs[2]', 'nodes["MulRough"].inputs[1]')

        #normal
        self.innerLink(normalTexOutput, 'nodes["NormalTexSampler"].inputs[0]')
        self.innerLink('nodes["NormalTexSampler"].outputs[0]', 'nodes["MulNormal"].inputs[1]')

        # todo: 
        # the MSFS_ShaderNodeTextureSampler is missing the operator that actually sample the texture
        # only some basics connections are done


        #PrincipledBSDF connections
        self.innerLink('nodes["MulEmissive"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[19]')
        self.innerLink('nodes["MulOccl"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[0]')
        self.innerLink('nodes["MulMetal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[6]')
        self.innerLink('nodes["MulRough"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[9]')
        self.innerLink('nodes["MulNormal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[22]')

    def getGroupInputOutputPath(self, propertyIndex):
        return 'nodes["GroupInput"].outputs[{}]'.format(propertyIndex)

    def getNodetree(self, name):
        if bpy.data.node_groups.find(name)==-1:
            self.createNodetree(name)
        else:
            self.node_tree=bpy.data.node_groups[name]

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
 
 
 
