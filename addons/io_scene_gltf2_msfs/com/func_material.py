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

import bpy

class MaterialError(Exception):
    def __init__(self, msg, objs=None):
        self.msg = msg
        self.objs= objs

#class MaterialUtil():
def MakeOpaque(Material):
    #remove the alpha link:
    bsdf_node = Material.node_tree.nodes.get("bsdf")
    if bsdf_node != None:
        l = bsdf_node.inputs["Alpha"].links[0]
        Material.node_tree.links.remove(l)    

    Material.blend_method = 'OPAQUE'

def MakeMasked(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.net(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'CLIP'

def MakeTranslucent(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.new(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'BLEND'

def MakeDither(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    #Since Eevee doesn't provide a dither mode, we'll just use alpha-blend instead.
    #It sucks, but what else is there to do?
    #create the alpha link:
    bsdf_node = nodes.get("bsdf")
    alpha_multiply = nodes.get("alpha_multiply")
    if (bsdf_node != None and alpha_multiply != None):
        links.new(alpha_multiply.outputs["Value"],bsdf_node.inputs["Alpha"])

    Material.blend_method = 'BLEND'

# This function removes all nodes from the shader node tree
def RemoveShaderNodes(Material,keep_output=True):
    nodes = Material.node_tree.nodes
    output_node = None

    for idx,node in enumerate(nodes):
        if ((node.type != 'OUTPUT_MATERIAL') or (keep_output == False)):
            #removing node:
            print("Deleting: %s | %s"%(node.name,node.type))
            nodes.remove(node)
        else:
            output_node = node
    
    return output_node

# Find a node of a specific type
def FindNodeByType(Material, node_type):
    nodes = Material.node_tree.nodes
    for idx,node in enumerate(nodes):
        if node.type == node_type:
            return node
    return None
# Find a node of a specific name
def FindNodeByName(Material, node_name):
    nodes = Material.node_tree.nodes
    for idx,node in enumerate(nodes):
        if node.name == node_name:
            return node
    return None

# Create a new node of a specific type
def CreateNewNode(Material,node_type,label=None,location=(.0,.0)):
    new_node = None
    try:
        new_node = Material.node_tree.nodes.new(node_type)
        if label != None:
            new_node.name = label
            new_node.label = label
        new_node.location = location
    finally:
        print("New node '%s' of type '%s' created for material '%s'."%(new_node.name,node_type,Material.name))

    if new_node == None:
        msg = format("MATERIAL ERROR! A new output shader node could not be created for the material '%s'."%Material.name)
        raise MaterialError(msg)
    return new_node

def CreatePBRBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    # Base color
    base_color_node = CreateNewNode(Material,'ShaderNodeTexImage',"albedo",location=(offset[0],offset[1]))

    # color mixer
    base_color_tint = CreateNewNode(Material,'ShaderNodeRGB',"albedo_tint",location=(offset[0]+100,offset[1]+50))
    base_color_tint.hide = True
    base_color_tint.outputs[0].default_value[0]=Material.msfs_color_albedo_mix[0]
    base_color_tint.outputs[0].default_value[1]=Material.msfs_color_albedo_mix[1]
    base_color_tint.outputs[0].default_value[2]=Material.msfs_color_albedo_mix[2]
    base_color_tint.outputs[0].default_value[3]=Material.msfs_color_alpha_mix
    base_color_tint_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"albedo_tint_mix",location=(offset[0]+350,offset[1]+20))
    base_color_tint_mix.hide = True
    base_color_tint_mix.blend_type = 'MULTIPLY'
    base_color_tint_mix.inputs[0].default_value = 1.0
    base_color_tint_mix.inputs[1].default_value[0] = 1.0
    base_color_tint_mix.inputs[1].default_value[1] = 1.0
    base_color_tint_mix.inputs[1].default_value[2] = 1.0
    base_color_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"albedo_detail_mix",location=(offset[0]+550,offset[1]+20))
    base_color_detail_mix.hide = True
    base_color_detail_mix.blend_type = 'MULTIPLY'
    base_color_detail_mix.inputs[0].default_value = Material.msfs_color_base_mix
    base_color_detail_mix.inputs[2].default_value[0] = Material.msfs_color_albedo_mix[0]
    base_color_detail_mix.inputs[2].default_value[1] = Material.msfs_color_albedo_mix[1]
    base_color_detail_mix.inputs[2].default_value[2] = Material.msfs_color_albedo_mix[2]
    base_color_detail_mix.inputs[2].default_value[3] = Material.msfs_color_base_mix
    # base_color_detail_mix.inputs["Color2"].default_value = (1.0,1.0,1.0,1.0)

    # Assign texture, if already saved in msfs data:
    if Material.msfs_albedo_texture != None:
        if Material.msfs_albedo_texture.name != "":
            base_color_node.image = Material.msfs_albedo_texture
            links.new(base_color_node.outputs["Color"], base_color_tint_mix.inputs["Color2"])
            links.new(base_color_detail_mix.outputs["Color"], bsdf_node.inputs["Base Color"])

    #Create the Alpha path:
    alpha_multiply = CreateNewNode(Material,'ShaderNodeMath',"alpha_multiply",location=(offset[0]+550,offset[1]-350))
    alpha_multiply.hide = True
    alpha_multiply.operation = 'MULTIPLY'
    alpha_multiply.inputs[1].default_value = Material.msfs_color_alpha_mix
    alpha_multiply.inputs[0].default_value = 1.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], base_color_node.inputs["Vector"])
    #Create albedo links:
    #links.new(base_color_tint.outputs["Color"], base_color_detail_mix.inputs["Color2"])
    #links.new(base_color_tint.outputs["Color"], base_color_tint_mix.inputs["Color1"])
    links.new(base_color_tint_mix.outputs["Color"], base_color_detail_mix.inputs["Color1"])

    #Link the Alpha:
    links.new(base_color_node.outputs["Alpha"], alpha_multiply.inputs[0])


    # Metallic
    texture_metallic_node = CreateNewNode(Material,'ShaderNodeTexImage',"metallic",location=(offset[0],offset[1]-280))
    if Material.msfs_metallic_texture != None:
        if Material.msfs_metallic_texture.name != "":
            texture_metallic_node.image = Material.msfs_metallic_texture
    metallic_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"metallic_detail_mix",location=(offset[0]+350,offset[1]-305))
    metallic_detail_mix.hide = True
    metallic_detail_mix.blend_type = 'MIX'
    metallic_detail_mix.inputs[0].default_value = 0.0
    metallic_separate = CreateNewNode(Material,'ShaderNodeSeparateRGB',"metallic_sep",location=(offset[0]+550,offset[1]-305))
    metallic_separate.hide = True

    # Create a node group for the occlusion map
    #Let's see if the node tree already exists, if not create one.
    occlusion_node_tree = bpy.data.node_groups.get("glTF Settings")
    if occlusion_node_tree == None:
        #create a new node tree with one input for the occlusion:
        occlusion_node_tree = bpy.data.node_groups.new('glTF Settings', 'ShaderNodeTree')
        occlusion_node_tree.nodes.new('NodeGroupInput')
        occlusion_node_tree.inputs.new('NodeSocketFloat','Occlusion')
        occlusion_node_tree.inputs[0].default_value = (1.000)
    #2. place a new node group in the current node tree:
    occlusion_group = CreateNewNode(Material,'ShaderNodeGroup',location=(offset[0]+1000,offset[1]+50))
    occlusion_group.node_tree = occlusion_node_tree
    occlusion_group.width = 200.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], texture_metallic_node.inputs["Vector"])
    #Create metallic links:
    links.new(texture_metallic_node.outputs["Color"], metallic_detail_mix.inputs["Color1"])
    links.new(metallic_detail_mix.outputs["Color"], metallic_separate.inputs["Image"])
    links.new(metallic_separate.outputs[0], occlusion_group.inputs["Occlusion"])
    if Material.msfs_metallic_texture != None:
        if Material.msfs_metallic_texture.name != "":
            #link to bsdf
            if (bsdf_node != None and metallic_separate != None):
                links.new(metallic_separate.outputs[1], bsdf_node.inputs["Roughness"])
                links.new(metallic_separate.outputs[2], bsdf_node.inputs["Metallic"])


    # Normal map
    normal_node = CreateNewNode(Material,'ShaderNodeTexImage',"normal",location=(offset[0],offset[1]-900))
    normal_map_node = CreateNewNode(Material,'ShaderNodeNormalMap',"normal_map_node",location=(offset[0]+550,offset[1]-930))
    if Material.msfs_normal_texture != None:
        if Material.msfs_normal_texture.name != "":
            normal_node.image = Material.msfs_normal_texture
            links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])
    normal_map_node.inputs["Strength"].default_value = Material.msfs_normal_scale
    normal_map_node.hide = True
    normal_detail_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"normal_detail_mix",location=(offset[0]+350,offset[1]-926))
    normal_detail_mix.hide = True
    normal_detail_mix.blend_type = 'MIX'
    normal_detail_mix.use_clamp = True
    normal_detail_mix.inputs[0].default_value = 0.0

    #Link the UV:
    links.new(uv_node.outputs["UV"], normal_node.inputs["Vector"])
    #Create normal links:
    links.new(normal_node.outputs["Color"], normal_detail_mix.inputs["Color1"])
    links.new(normal_detail_mix.outputs["Color"], normal_map_node.inputs["Color"])
    #link to bsdf
    #links.new(normal_map_node.outputs["Normal"], bsdf_node.inputs["Normal"])


def CreateEmissiveBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Emissive
    emissive_node = CreateNewNode(Material,'ShaderNodeTexImage',"emissive",location=(offset[0],offset[1]))
    if Material.msfs_emissive_texture != None:
        if Material.msfs_emissive_texture.name != "":
            emissive_node.image = Material.msfs_emissive_texture
    # color mixer
    emissive_tint = CreateNewNode(Material,'ShaderNodeRGB',"emissive_tint",location=(offset[0]+100,offset[1]+50))
    emissive_tint.hide = True
    emissive_tint.outputs[0].default_value[0]=Material.msfs_color_emissive_mix[0]
    emissive_tint.outputs[0].default_value[1]=Material.msfs_color_emissive_mix[1]
    emissive_tint.outputs[0].default_value[2]=Material.msfs_color_emissive_mix[1]
    emissive_tint_mix = CreateNewNode(Material,'ShaderNodeMixRGB',"emissive_tint_mix",location=(offset[0]+350,offset[1]+20))
    emissive_tint_mix.hide = True
    emissive_tint_mix.blend_type = 'MULTIPLY'
    emissive_tint_mix.inputs[0].default_value = 1.0

    #Link UV:
    links.new(uv_node.outputs["UV"], emissive_node.inputs["Vector"])
    #Create metallic links:
    links.new(emissive_tint.outputs["Color"], emissive_tint_mix.inputs["Color1"])
    links.new(emissive_node.outputs["Color"], emissive_tint_mix.inputs["Color2"])


def CreateDetailBranch(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    # Detail texture nodes:
    detail_albedo_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_albedo",location=(offset[0],offset[1]))
    if Material.msfs_detail_albedo_texture != None:
        if Material.msfs_detail_albedo_texture.name != "":
            detail_albedo_node.image = Material.msfs_detail_albedo_texture
    detail_metallic_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_metallic",location=(offset[0],offset[1]-280))
    if Material.msfs_detail_metallic_texture != None:
        if Material.msfs_detail_metallic_texture.name != "":
            detail_metallic_node.image = Material.msfs_detail_metallic_texture
    detail_normal_node = CreateNewNode(Material,'ShaderNodeTexImage',"detail_normal",location=(offset[0],offset[1]-560))
    if Material.msfs_detail_normal_texture != None:
        if Material.msfs_detail_normal_texture.name != "":
            detail_normal_node.image = Material.msfs_detail_normal_texture

    # Create the scaling transform
    detail_uv_scale_node = CreateNewNode(Material, 'ShaderNodeMapping', 'detail_uv_scale', location=(offset[0]-200,offset[1]-195))
    detail_uv_scale_node.hide = True

    # Find the main pbr nodes:
    albedo_node_mix = nodes.get("albedo_detail_mix")
    metallic_node_mix = nodes.get("metallic_detail_mix")
    normal_node_mix = nodes.get("normal_detail_mix")

    #create the links, if possible and texture name is already set:
    if albedo_node_mix != None:
        if Material.msfs_detail_albedo_texture != None:
            if Material.msfs_detail_albedo_texture.name != "":
                links.new(detail_albedo_node.outputs["Color"],albedo_node_mix.inputs["Color2"])
    if metallic_node_mix != None:
        if Material.msfs_detail_metallic_texture != None:
            if Material.msfs_detail_metallic_texture.name != "":
                links.new(detail_metallic_node.outputs["Color"],metallic_node_mix.inputs["Color2"])
    if normal_node_mix != None:
        if Material.msfs_detail_normal_texture != None:
            if Material.msfs_detail_normal_texture.name != "":
                links.new(detail_normal_node.outputs["Color"],normal_node_mix.inputs["Color2"])

    links.new(uv_node.outputs["UV"],detail_uv_scale_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_albedo_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_metallic_node.inputs["Vector"])
    links.new(detail_uv_scale_node.outputs["Vector"],detail_normal_node.inputs["Vector"])

    detail_uv_scale_node.inputs["Scale"].default_value[0] = Material.msfs_detail_uv_scale
    detail_uv_scale_node.inputs["Scale"].default_value[1] = Material.msfs_detail_uv_scale
    detail_uv_scale_node.inputs["Scale"].default_value[2] = Material.msfs_detail_uv_scale

def CreateBlendMask(Material, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Blend Mask
    blend_mask = CreateNewNode(Material,'ShaderNodeTexImage',"blend_mask",location=(offset[0],offset[1]))
    if Material.msfs_blend_mask_texture != None:
        if Material.msfs_blend_mask_texture.name != "":
            blend_mask.image = Material.msfs_blend_mask_texture

    #Link UV:
    links.new(uv_node.outputs["UV"], blend_mask.inputs["Vector"])   #this might need to come from the detail uv transform instead.

    if Material.msfs_blend_mask_texture != None:
        if mat.msfs_blend_mask_texture.channels > 3:
            if albedo_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Alpha"],albedo_detail_mix.inputs["Fac"])
            if metallic_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Alpha"],metallic_detail_mix.inputs["Fac"])
            if normal_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Alpha"],normal_detail_mix.inputs["Fac"])
        else:
            if albedo_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Color"],albedo_detail_mix.inputs["Fac"])
            if metallic_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Color"],metallic_detail_mix.inputs["Fac"])
            if normal_detail_mix != None:
                links.new(nodes["blend_mask"].outputs["Color"],normal_detail_mix.inputs["Fac"])    

def CreateAnisotropicDirection(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

   # Blend Mask
    anisotropic_direction = CreateNewNode(Material,'ShaderNodeTexImage',"anisotropic_direction",location=(offset[0],offset[1]))
    if Material.msfs_anisotropic_direction_texture != None:
        if Material.msfs_anisotropic_direction_texture.name != "":
            anisotropic_direction.image = Material.msfs_anisotropic_direction_texture

    #Link UV:
    links.new(uv_node.outputs["UV"], anisotropic_direction.inputs["Vector"])   #this might need to come from the detail uv transform instead.

def CreateClearcoat(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    clearcoat = CreateNewNode(Material,'ShaderNodeTexImage',"clearcoat",location=(offset[0],offset[1]))
    clearcoat_sep = CreateNewNode(Material,'ShaderNodeSeparateRGB',"clearcoat_sep",location=(offset[0]+350,offset[1]))
    clearcoat_sep.hide = True
    links.new(clearcoat.outputs["Color"],clearcoat_sep.inputs["Image"])

    if Material.msfs_clearcoat_texture != None:
        if Material.msfs_clearcoat_texture.name != "":
            clearcoat.image = Material.msfs_clearcoat_texture
            #Create links:
            links.new(clearcoat_sep.outputs["R"],bsdf_node.inputs["Clearcoat"])
            links.new(clearcoat_sep.outputs["G"],bsdf_node.inputs["Clearcoat Roughness"])

    #Link UV:
    links.new(uv_node.outputs["UV"], clearcoat.inputs["Vector"])   #this might need to come from the detail uv transform instead.

def CreateWiperMask(Material, bsdf_node, offset=(0.0,0.0)):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(offset[0]-2000,offset[1]))

    wiper_mask = CreateNewNode(Material,'ShaderNodeTexImage',"wiper_mask",location=(offset[0],offset[1]))

    #Link UV:
    links.new(uv_node.outputs["UV"], wiper_mask.inputs["Vector"])

# The following functions create Blender shaders to represent the MSFS material presets
def CreateMSFSStandardShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSAnisotropicShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateAnisotropicDirection(Material,bsdf_node,(-1000,-700))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1250))
    CreateBlendMask(Material,(-1000,-900))

def CreateMSFSSSSShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))
    bsdf_node.inputs["Subsurface Color"].default_value = Material.msfs_color_sss

    bsdf_node.inputs["Subsurface"].default_value = 0.1

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    
def CreateMSFSGlassShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))
    
    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSDecalShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSClearcoatShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateClearcoat(Material, bsdf_node,(-1000,-700))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1350))
    CreateBlendMask(Material,(-1000,-1000))

def CreateMSFSFakeTerrainShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSFresnelShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSWindshieldShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))
    #CreateWiperMask(Material,(-1000,-950))

    Material.msfs_roughness_scale = 0.0
    Material.msfs_metallic_scale = 0.0
    Material.msfs_color_alpha_mix = 0.1
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSPortholeShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-1050))
    CreateBlendMask(Material,(-1000,-700))

def CreateMSFSParallaxShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))

    #For the behind-glass magic, we'll need some uv controls:
    uv_node = FindNodeByName(Material,"UV")
    if uv_node == None:
        uv_node = CreateNewNode(Material,'ShaderNodeUVMap',"UV",location=(-3000,500))
    behind_glass_uv_scale_node = CreateNewNode(Material, 'ShaderNodeMapping', 'behind_glass_uv_scale', location=(-1200,-795))
    behind_glass_uv_scale_node.hide = True

    # Add the behind-glass-albedo-emissive
    behind_glass_node = CreateNewNode(Material,'ShaderNodeTexImage',"behind_glass",location=(-1000,-750))
    if Material.msfs_behind_glass_texture != None:
        if Material.msfs_behind_glass_texture.name != "":
            behind_glass_node.image = Material.msfs_behind_glass_texture
            if nodes.get("albedo_detail_mix") != None:
                links.new(behind_glass_node.outputs["Color"], nodes.get("albedo_detail_mix").inputs["Color2"])
    # Grab the Emissive texture:
    emissive_node = FindNodeByName(Material,"emissive")
    links.new(uv_node.outputs["UV"],behind_glass_uv_scale_node.inputs["Vector"])
    links.new(behind_glass_uv_scale_node.outputs["Vector"],behind_glass_node.inputs["Vector"])

    if emissive_node != None:
        links.new(behind_glass_uv_scale_node.outputs["Vector"],emissive_node.inputs["Vector"])

def CreateMSFSGeoDecalShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateDetailBranch(Material,bsdf_node,(-1000,-500))

    #enable transparency:
    Material.msfs_blend_mode = 'BLEND'

def CreateMSFSHairShader(Material):
    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)

    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')

    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled','bsdf',location=(0,400))

    bsdf_node.inputs["Subsurface"].default_value = 0.2    

    #link to output
    links.new(bsdf_node.outputs["BSDF"], output_node.inputs["Surface"])

    CreatePBRBranch(Material,bsdf_node,(-1000,500))
    CreateEmissiveBranch(Material,bsdf_node,(-1000,-120))
    CreateAnisotropicDirection(Material, bsdf_node,(-1000,-400))

    Material.msfs_blend_mode = 'DITHER'

def CreateMSFSInvisibleShader(Material):

    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)
    
    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')
    
    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled',location=(0,400))
    bsdf_node.inputs["Alpha"].default_value = 0.5
    bsdf_node.inputs["Base Color"].default_value = (0.8,0.0,0.0,1.0)
    bsdf_node.inputs["Emission"].default_value = (0.8,0.0,0.0,1.0)

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #connect the nodes:
    links.new(output_node.inputs["Surface"], bsdf_node.outputs["BSDF"])

    #enable transparency:
    MakeTranslucent(Material)

def CreateMSFSEnvOccluderShader(Material):

    nodes = Material.node_tree.nodes
    links = Material.node_tree.links

    output_node = RemoveShaderNodes(Material,True)
    
    #check if there is an output node, create one if not:
    if output_node == None:
        output_node = CreateNewNode(Material,'ShaderNodeOutputMaterial')
    
    #create the main BSDF node:
    bsdf_node = CreateNewNode(Material,'ShaderNodeBsdfPrincipled',location=(0,400))
    bsdf_node.inputs["Alpha"].default_value = 0.3
    bsdf_node.inputs["Base Color"].default_value = (0.0,0.8,0.0,1.0)
    bsdf_node.inputs["Emission"].default_value = (0.0,0.8,0.0,1.0)

    bsdf_node.inputs["Subsurface"].default_value = 0.0    

    #connect the nodes:
    links.new(output_node.inputs["Surface"], bsdf_node.outputs["BSDF"])

    #enable transparency:
    MakeTranslucent(Material)
