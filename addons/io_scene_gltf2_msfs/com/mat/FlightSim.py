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
        layout.label(text="text")
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

        self.outputs.new('AlphaModeSocket', "Color")

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


class MSFS_MaterialParams_Panel(bpy.types.Panel):
    bl_label = "MSFS Material Properties"
    bl_idname = "MSFS_MaterialParams_props"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        mat = context.active_object.active_material

        layout = self.layout
        
        if mat:
            box=layout.box()

            subbox=box.box()
            subbox.label(text="Color multipliers",icon='COLOR')
            row = subbox.row()
            row.prop(mat, 'msfs_baseColor')


            box.label(text="Texture maps",icon='TEXTURE')
            box.label(text = "Albedo:")
            box.template_ID(mat, "msfs_baseColorTex", new = "image.new", open = "image.open")
            
class MSFS_PropertyBinder():

    def match_baseColorTex(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        msfs_material = nodes.get("MSFS_Standard")
        albedoTexImageNode = msfs_material.getNode(MSFS_MaterialProperties.baseColorTex.name())
        albedoTexImageNode.image =  mat.msfs_baseColorTex   

    def match_baseColor(self, context):
        mat = context.active_object.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        msfs_material = nodes.get("MSFS_Standard")
        baseColorNode = msfs_material.getNode(MSFS_MaterialProperties.baseColor.name())
        baseColorNode.image =  mat.msfs_baseColorTex   

    bpy.types.Material.msfs_baseColor = bpy.props.FloatVectorProperty(name = "Base Color", subtype='COLOR', min=0.0, max=1.0,size=4,default=[1.0,1.0,1.0,1.0], description="The color value set here will be mixed in with the albedo value of the material.", update = match_baseColor)
    bpy.types.Material.msfs_baseColorTex = bpy.props.PointerProperty(type = bpy.types.Image, name = "Base Color map", update = match_baseColorTex)  

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

    def update(self):
        pass

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
        
        #NODES
        groupInputNode = self.addNode('NodeGroupInput', { 'name':'GroupInput', 'location':(-500.0,0.0)})
        groupOutputNode = self.addNode('NodeGroupOutput', { 'name':'GroupOutput','location':(700.0,0.0) })
        self.addNode('ShaderNodeBsdfPrincipled', { 'name':'PrincipledBSDF','location':(400.0,0.0) })

        self.nodeBaseColorTex = self.addNode('ShaderNodeTexImage', { 'name': MSFS_MaterialProperties.baseColorTex.name()})
        self.nodeBaseColor = self.addNode('ShaderNodeRGB', { 'name': MSFS_MaterialProperties.baseColor.name() })
        
        mulBaseColorNode =self.addNode('ShaderNodeMixRGB', { 'name':"MulBaseColor",'blend_type':'MULTIPLY' })
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
        self.innerLink('nodes["PrincipledBSDF"].outputs[0]', 'nodes["GroupOutput"].inputs[0]')

        #color
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_MaterialProperties.baseColorTex.name()), 'nodes["MulBaseColor"].inputs[2]')
        self.innerLink('nodes["{0}"].outputs[0]'.format(MSFS_MaterialProperties.baseColor.name()), 'nodes["MulBaseColor"].inputs[1]')
        

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
        self.innerLink('nodes["MulBaseColor"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[0]')

        # self.innerLink('nodes["MulEmissive"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[19]')
        # self.innerLink('nodes["MulOccl"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[0]')
        # self.innerLink('nodes["MulMetal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[6]')
        # self.innerLink('nodes["MulRough"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[9]')
        # self.innerLink('nodes["MulNormal"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[22]')

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


 
 
