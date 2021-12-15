import bpy
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
   


class MSFS_Standard(bpy.types.ShaderNodeCustomGroup):
    bl_name='MSFS_Standard'
    bl_label='MSFS_Standard'
    bl_icon='NONE'

    def init(self, context):
        self.getNodetree(self.name + '_node_tree')
        # self.inputs.new('AlphaModeSocket', "Alpha Mode")
        self.inputs['Base Color'].default_value=[1,1,1,1]
        self.inputs['Emissive'].default_value=[0,0,0,1]

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
        # self.addNode('ShaderNodeTexCoord', { 'name':'Node0'  })
        # self.addNode('ShaderNodeMixRGB', { 'name':'Node1'  })
        # self.addNode('ShaderNodeValue', { 'name':'Node4' ,'outputs[0].default_value':1  })
        # self.addNode('ShaderNodeMath', { 'name':'Node7' ,'operation':'DIVIDE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node8' ,'operation':'DIVIDE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node9' ,'operation':'DIVIDE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node10' ,'operation':'DIVIDE' })
        # self.addNode('ShaderNodeSeparateXYZ', { 'name':'Node11'  })
        # self.addNode('ShaderNodeMath', { 'name':'Node12' ,'operation':'MODULO' })
        # self.addNode('ShaderNodeMath', { 'name':'Node13' ,'inputs[1].default_value':0.5 ,'operation':'ABSOLUTE' })
        # self.addNode('ShaderNodeSeparateXYZ', { 'name':'Node14'  })
        # self.addNode('ShaderNodeMath', { 'name':'Node15' ,'operation':'MODULO' })
        # self.addNode('ShaderNodeMath', { 'name':'Node16' ,'inputs[1].default_value':0.5 ,'operation':'ABSOLUTE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node17' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node18' ,'inputs[1].default_value':0.5 ,'operation':'ABSOLUTE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node19' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node20' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node21' ,'inputs[1].default_value':0.5 ,'operation':'ABSOLUTE' })
        # self.addNode('ShaderNodeMath', { 'name':'Node22' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node23' ,'operation':'MINIMUM' })
        # self.addNode('ShaderNodeMath', { 'name':'Node24' ,'operation':'MINIMUM' })
        # self.addNode('ShaderNodeMath', { 'name':'Node25' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node26' ,'operation':'MULTIPLY' })
        # self.addNode('ShaderNodeMath', { 'name':'Node27' ,'operation':'ADD' })
        # self.addNode('ShaderNodeMath', { 'name':'Node28' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node29' ,'operation':'SUBTRACT' })
        # self.addNode('ShaderNodeMath', { 'name':'Node30' ,'operation':'DIVIDE','use_clamp':1  })
        # self.addNode('ShaderNodeMath', { 'name':'Node31' ,'operation':'GREATER_THAN' })
        #Sockets
        self.addSocket(False, 'NodeSocketColor',   'Base Color')
        self.addSocket(False, 'NodeSocketColor',   'Emissive')
        self.addSocket(False, 'NodeSocketTexture', 'Base Color Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Occlusion(R) Roughness(G) Metallic(B) Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Normal Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Emissive Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Detail Color (RGB) Alpha(A) Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Detail Occlusion(R) Roughness(G) Metallic(B) Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Detail Normal Texture')
        self.addSocket(False, 'NodeSocketTexture', 'Blend Mask Texture')
        #Links
        # self.innerLink('nodes["Node0"].outputs[3]', 'nodes["Node1"].inputs[1]')
        self.innerLink('nodes["GroupInput"].outputs[0]', 'nodes["PrincipledBSDF"].inputs[0]')
        self.innerLink('nodes["PrincipledBSDF"].outputs[0]', 'nodes["GroupOutput"].inputs[0]')
        # self.innerLink('nodes["GroupInput"].outputs[4]', 'nodes["Node7"].inputs[0]')
        # self.innerLink('nodes["Node4"].outputs[0]', 'nodes["Node7"].inputs[1]')
        # self.innerLink('nodes["GroupInput"].outputs[5]', 'nodes["Node8"].inputs[0]')
        # self.innerLink('nodes["Node4"].outputs[0]', 'nodes["Node8"].inputs[1]')
        # self.innerLink('nodes["GroupInput"].outputs[2]', 'nodes["Node9"].inputs[0]')
        # self.innerLink('nodes["Node4"].outputs[0]', 'nodes["Node9"].inputs[1]')
        # self.innerLink('nodes["GroupInput"].outputs[3]', 'nodes["Node10"].inputs[0]')
        # self.innerLink('nodes["Node4"].outputs[0]', 'nodes["Node10"].inputs[1]')
        # self.innerLink('nodes["Node1"].outputs[0]', 'nodes["Node11"].inputs[0]')
        # self.innerLink('nodes["Node11"].outputs[0]', 'nodes["Node12"].inputs[0]')
        # self.innerLink('nodes["GroupInput"].outputs[2]', 'nodes["Node12"].inputs[1]')
        # self.innerLink('nodes["Node12"].outputs[0]', 'nodes["Node13"].inputs[0]')
        # self.innerLink('nodes["Node1"].outputs[0]', 'nodes["Node14"].inputs[0]')
        # self.innerLink('nodes["GroupInput"].outputs[3]', 'nodes["Node15"].inputs[1]')
        # self.innerLink('nodes["Node15"].outputs[0]', 'nodes["Node16"].inputs[0]')
        # self.innerLink('nodes["Node13"].outputs[0]', 'nodes["Node17"].inputs[0]')
        # self.innerLink('nodes["Node9"].outputs[0]', 'nodes["Node17"].inputs[1]')
        # self.innerLink('nodes["Node17"].outputs[0]', 'nodes["Node18"].inputs[0]')
        # self.innerLink('nodes["Node9"].outputs[0]', 'nodes["Node19"].inputs[0]')
        # self.innerLink('nodes["Node18"].outputs[0]', 'nodes["Node19"].inputs[1]')
        # self.innerLink('nodes["Node16"].outputs[0]', 'nodes["Node20"].inputs[0]')
        # self.innerLink('nodes["Node10"].outputs[0]', 'nodes["Node20"].inputs[1]')
        # self.innerLink('nodes["Node20"].outputs[0]', 'nodes["Node21"].inputs[0]')
        # self.innerLink('nodes["Node10"].outputs[0]', 'nodes["Node22"].inputs[0]')
        # self.innerLink('nodes["Node21"].outputs[0]', 'nodes["Node22"].inputs[1]')
        # self.innerLink('nodes["Node19"].outputs[0]', 'nodes["Node23"].inputs[0]')
        # self.innerLink('nodes["Node22"].outputs[0]', 'nodes["Node23"].inputs[1]')
        # self.innerLink('nodes["GroupInput"].outputs[2]', 'nodes["Node24"].inputs[0]')
        # self.innerLink('nodes["GroupInput"].outputs[3]', 'nodes["Node24"].inputs[1]')
        # self.innerLink('nodes["Node24"].outputs[0]', 'nodes["Node25"].inputs[0]')
        # self.innerLink('nodes["Node7"].outputs[0]', 'nodes["Node25"].inputs[1]')
        # self.innerLink('nodes["Node8"].outputs[0]', 'nodes["Node26"].inputs[0]')
        # self.innerLink('nodes["Node25"].outputs[0]', 'nodes["Node26"].inputs[1]')
        # self.innerLink('nodes["Node7"].outputs[0]', 'nodes["Node27"].inputs[0]')
        # self.innerLink('nodes["Node26"].outputs[0]', 'nodes["Node27"].inputs[1]')
        # self.innerLink('nodes["Node23"].outputs[0]', 'nodes["Node28"].inputs[0]')
        # self.innerLink('nodes["Node7"].outputs[0]', 'nodes["Node28"].inputs[1]')
        # self.innerLink('nodes["Node27"].outputs[0]', 'nodes["Node29"].inputs[0]')
        # self.innerLink('nodes["Node7"].outputs[0]', 'nodes["Node29"].inputs[1]')
        # self.innerLink('nodes["Node28"].outputs[0]', 'nodes["Node30"].inputs[0]')
        # self.innerLink('nodes["Node29"].outputs[0]', 'nodes["Node30"].inputs[1]')
        # self.innerLink('nodes["Node23"].outputs[0]', 'nodes["Node31"].inputs[0]')
        # self.innerLink('nodes["Node7"].outputs[0]', 'nodes["Node31"].inputs[1]')
        # self.innerLink('nodes["Node30"].outputs[0]', 'nodes["GroupOutput"].inputs[0]')
        # self.innerLink('nodes["Node31"].outputs[0]', 'nodes["GroupOutput"].inputs[1]')
    def getNodetree(self, name):
        if bpy.data.node_groups.find(name)==-1:
            self.createNodetree(name)
        else:
            self.node_tree=bpy.data.node_groups[name]
                   
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
 
 
 
