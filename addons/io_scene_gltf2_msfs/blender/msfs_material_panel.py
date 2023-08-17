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

from .msfs_material_prop_update import MSFS_Material_Property_Update
from bpy.types import Material

def equality_check(arr1, arr2, size1, size2):
   if (size1 != size2):
      return False
   for i in range(0, size2):
      # blender pyhon color channel issues in floats ???
      if (int(arr1[i] * 10000000)/10000000 != int(arr2[i] * 10000000)/10000000):
         return False
   return True

class MSFS_OT_MigrateColorFixData(bpy.types.Operator): # TODO: Remove eventually
    """This addon changes the color nodes, metallic, roughness values to the BSDF color if there is no link input"""

    bl_idname = "msfs.migrate_colorfix_data"
    bl_label = "Change Material to BSDF Data Pre-Migrate"


    @staticmethod
    def old_material_values_diff(mat):
        #print("Called")
        found_diff = False
        # there could be a chance that there are msfs values and BSDF non default values
        nodes = mat.node_tree.nodes
        bsdfnodes = [n for n in nodes 
                if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
        temp_alpha = 1.0
        if mat.msfs_material_mode == "NONE" and mat.msfs_material_type == "NONE":
            base_color_default = [0.8,0.8,0.8,1.0]
            for principled in bsdfnodes:
                if not principled.inputs[0].links:
                    # check base color not default
                    # get BSDF base Color value
                    BSDF_Base_Color = principled.inputs[0].default_value
                    #print(BSDF_Base_Color[0], base_color_default[0], BSDF_Base_Color[1], base_color_default[1], BSDF_Base_Color[2], base_color_default[2], BSDF_Base_Color[3], base_color_default[3])
                    if not equality_check(BSDF_Base_Color, base_color_default, len(BSDF_Base_Color), len(base_color_default)):
                        found_diff = True

            return found_diff
        # some devs potentially set the material, but destroy the nodes - and the system thinks that a proper MSFS material is there
        # check to see if a common node is there (albedo_tint or Base color). - if none there, then check BSDF values
        bad_material_setup = True
        print("old_albedo_tint_color_diff - START check nodes - type, mode", mat, mat.msfs_material_type, mat.msfs_material_mode)
        try:
            if mat.msfs_material_mode != "NONE" and mat.node_tree.nodes["albedo_tint"] is not None:
                bad_material_setup = False
                #print("checked mode")
        except:
            pass
        finally:
            try:
                if mat.msfs_material_type != "NONE" and mat.node_tree.nodes["Base Color RGB"] is not None:
                    bad_material_setup = False
                    #print("checked type")
            except:
                pass
            finally:
                pass
        if bad_material_setup and mat.msfs_material_mode != "NONE":
            bad_material_setup = False

        print("old_albedo_tint_color_diff - nodes checked and is bad", mat, mat.msfs_material_type, mat.msfs_material_mode, bad_material_setup )
        if ((bad_material_setup and mat.msfs_material_type != "NONE") or (mat.msfs_material_mode == "NONE" and mat.msfs_material_type != "NONE") or (not bad_material_setup and mat.msfs_material_mode != "NONE")
                    or (bad_material_setup and mat.msfs_material_type == "NONE" and mat.msfs_material_mode == "NONE")):
            print("old_albedo_tint_color_diff - looking mat, type, mode, and is bad", mat, mat.msfs_material_type, mat.msfs_material_mode, bad_material_setup)
            for principled in bsdfnodes:
                if not principled.inputs[0].links:
                    # now get albedo_tint node and check color same as Base Color on BSDF
                    # get albedo_tint node
                    #print("old_albedo_tint_color_diff - mat", mat)
                    try:
                        if mat.node_tree.nodes["albedo_tint"] is not None:
                            # get alpha for later input 21 alpha check
                            temp_alpha = mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3]
                            # get color
                            albedo_tint_checkval = mat.node_tree.nodes["albedo_tint"].outputs[0].default_value
                            #print("old_albedo_tint_color_diff - albedo tint color", albedo_tint_checkval, temp_alpha)
                            # get BSDF base Color value
                            BSDF_Base_Color = principled.inputs["Base Color"].default_value
                            #print("old_albedo_tint_color_diff - BSDF to albedo tint color", BSDF_Base_Color[0], albedo_tint_checkval[0], BSDF_Base_Color[1], albedo_tint_checkval[1], BSDF_Base_Color[2], albedo_tint_checkval[2], BSDF_Base_Color[3], albedo_tint_checkval[3])
                            if not equality_check(BSDF_Base_Color, albedo_tint_checkval, len(BSDF_Base_Color), len(albedo_tint_checkval)):
                                found_diff = True
                            print("old_albedo_tint_color_diff - diff now alphas", found_diff, principled.inputs[21].default_value, temp_alpha, mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3])
                            # check the alphas - if an input to alpha then use node alpha - if no inputs use BSDF alpha - won't get here if no albedo_tint
                            if not principled.inputs[0].links and not principled.inputs[21].links and principled.inputs[21].default_value != temp_alpha:
                                found_diff = True
                            print("old_albedo_tint_color_diff - alpha diff", found_diff)
                    except:
                        try:
                            if mat.msfs_material_type != "NONE":
                                BSDF_Base_Color = principled.inputs["Base Color"].default_value
                                #print("old_albedo_tint_color_diff - BSDF to MSFS base color", BSDF_Base_Color[0], mat.msfs_base_color_factor[0], BSDF_Base_Color[1], mat.msfs_base_color_factor[1], BSDF_Base_Color[2], mat.msfs_base_color_factor[2], BSDF_Base_Color[3], mat.msfs_base_color_factor[3])
                                if not equality_check(BSDF_Base_Color, mat.msfs_base_color_factor, len(BSDF_Base_Color), len(mat.msfs_base_color_factor)):
                                    found_diff = True
                                if not principled.inputs[0].links and not principled.inputs[21].links and principled.inputs[21].default_value != temp_alpha:
                                    found_diff = True
                                print("old_albedo_tint_color_diff - alpha diff", found_diff)
                        except:
                            pass

                    finally:
                        pass

                #print("after node - diff", found_diff)
                if mat.msfs_material_type == "NONE" or bad_material_setup or (mat.msfs_material_mode != "NONE" and not bad_material_setup):
                    #print("old_albedo_tint_color_diff - values", principled.inputs[6].default_value, principled.inputs[9].default_value, principled.inputs[20].default_value, principled.inputs[21].default_value)
                    # input 6 Metallic
                    if not principled.inputs[6].links and principled.inputs[6].default_value != mat.msfs_metallic_factor:
                        found_diff = True
                    #print("after met", found_diff, mat.msfs_metallic_factor, principled.inputs[6].default_value)
                    # input 9 Roughness
                    if not principled.inputs[9].links and principled.inputs[9].default_value != mat.msfs_roughness_factor:
                        found_diff = True
                    #print("after rough", found_diff)
                    # input 20 Emissive Scale
                    if not principled.inputs[20].links and principled.inputs[20].default_value != mat.msfs_emissive_scale:
                        found_diff = True
                    print("after emmisive - diff", found_diff, principled.inputs[6].default_value, principled.inputs[9].default_value, principled.inputs[20].default_value, principled.inputs[21].default_value)
        #print("on return - diff", found_diff)
        return found_diff


    def execute(self, context):
        mat = context.active_object.active_material
        found_diff = False
        nodes = mat.node_tree.nodes
        bsdfnodes = [n for n in nodes 
                if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
        temp_alpha = 1.0
        for principled in bsdfnodes:
            #print("old_albedo_tint_color_diff - execute - principled", principled)
            if not principled.inputs[0].links:
                # now get albedo_tint node and check color same as Base Color on BSDF
                # get albedo_tint node
                try:
                    if mat.node_tree.nodes["albedo_tint"] is not None:
                        # get alpha for later input 21 alpha check
                        temp_alpha = mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3]
                        # get color
                        albedo_tint_checkval = mat.node_tree.nodes["albedo_tint"].outputs[0].default_value
                        # get BSDF base Color value
                        BSDF_Base_Color = principled.inputs["Base Color"].default_value
                        #print("old_albedo_tint_color_diff - execute - BSDF color", BSDF_Base_Color)
                        if not equality_check(BSDF_Base_Color, albedo_tint_checkval, len(BSDF_Base_Color), len(albedo_tint_checkval)):
                            mat.node_tree.nodes["albedo_tint"].outputs[0].default_value = BSDF_Base_Color
                            mat.msfs_base_color_factor = BSDF_Base_Color
                        # input 21 Alpha
                        # check the alphas - if an input to alpha then use node alpha - if no inputs use BSDF alpha - won't get here if no albedo_tint
                        if not principled.inputs[0].links and not principled.inputs[21].links and principled.inputs[21].default_value != temp_alpha:
                            print("old_albedo_tint_color_diff - execute - Alpha", mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3], principled.inputs[21].default_value)
                            # make alpha value from BSDF input(21)
                            mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3] = principled.inputs[21].default_value
                            principled.inputs["Base Color"].default_value[3] = principled.inputs[21].default_value
                            print("old_albedo_tint_color_diff - execute - Alpha out", mat.node_tree.nodes["albedo_tint"].outputs[0].default_value[3], principled.inputs[21].default_value)
                except:
                    try:
                        if mat.msfs_material_type != "NONE":
                            BSDF_Base_Color = principled.inputs["Base Color"].default_value
                            #print("old_albedo_tint_color_diff - execute - BSDF to MSFS base color", BSDF_Base_Color[0], mat.msfs_base_color_factor[0], BSDF_Base_Color[1], mat.msfs_base_color_factor[1], BSDF_Base_Color[2], mat.msfs_base_color_factor[2], BSDF_Base_Color[3], mat.msfs_base_color_factor[3])
                            if not equality_check(BSDF_Base_Color, mat.msfs_base_color_factor, len(BSDF_Base_Color), len(mat.msfs_base_color_factor)):
                                mat.msfs_base_color_factor = BSDF_Base_Color
                            # make Base Color alpha value BSDF - there is no albedo_tint here
                            if not principled.inputs[0].links and not principled.inputs[21].links and principled.inputs[21].default_value != temp_alpha:
                                principled.inputs["Base Color"].default_value[3] = principled.inputs[21].default_value
                        elif mat.msfs_material_type == "NONE" and mat.msfs_material_mode == "NONE":
                            # SPECIAL now if you have had msfs properties values - assume msfs_standard - make a wild guess because there was data here from before.
                            try:
                                print("old_albedo_tint_color_diff - execute - simple values BSDF to msfs_*")
                                mat.msfs_base_color_factor = principled.inputs["Base Color"].default_value
                                mat.msfs_emissive_factor = principled.inputs["Emission"].default_value
                                mat.mat.msfs_metallic_factor = principled.inputs[6].default_value
                                mat.mat.msfs_roughness_factor = principled.inputs[9].default_value
                            except:
                                print("old_albedo_tint_color_diff - execute - old_properties - Error - BSDF properties found skipping")

                    except:
                        pass

                finally:
                    pass

            # input 6 Metallic
            if principled.inputs[6].default_value != mat.msfs_metallic_factor:
                mat.msfs_metallic_factor = principled.inputs[6].default_value
            # input 9 Roughness
            if principled.inputs[9].default_value != mat.msfs_roughness_factor:
                mat.msfs_roughness_factor = principled.inputs[9].default_value
            # input 20 Emissive Scale
            if principled.inputs[20] != mat.msfs_emissive_scale:
                mat.msfs_emissive_scale = principled.inputs[20].default_value
        return {"FINISHED"}


class MSFS_OT_MigrateEmissiveFixData(bpy.types.Operator): # TODO: Remove eventually
    """This addon changes the emissive nodes to the BSDF emissive if there is no link input"""

    bl_idname = "msfs.migrate_emissivefix_data"
    bl_label = "Change Emissive to BSDF Data Pre-Migrate"


    @staticmethod
    def old_emissive_tint_color_diff(mat):
        #if mat.msfs_material_type == "NONE":
        nodes = mat.node_tree.nodes
        bsdfnodes = [n for n in nodes 
                if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
        for principled in bsdfnodes:
            if not principled.inputs[0].links:
                # now get albedo_tint node and check color same as Base Color on BSDF
                # get albedo_tint node
                #print("old_emissive_tint_color_diff - mat", mat)
                try:
                    if mat.node_tree.nodes["emissive_tint"] is not None:
                        # get color
                        emissive_tint_checkval = mat.node_tree.nodes["emissive_tint"].outputs[0].default_value
                        #print("old_emissive_tint_color_diff - albedo tint color", emissive_tint_checkval)
                        # get BSDF base Color value
                        BSDF_Emission = principled.inputs["Emission"].default_value
                        #print("old_emissive_tint_color_diff - BSDF emission", BSDF_Emission[0], emissive_tint_checkval[0], BSDF_Emission[1], emissive_tint_checkval[1], BSDF_Emission[2], emissive_tint_checkval[2], BSDF_Emission[3], emissive_tint_checkval[3])
                        if not equality_check(BSDF_Emission, emissive_tint_checkval, len(BSDF_Emission), len(emissive_tint_checkval)):
                           return True
                except:
                    pass
                finally:
                    pass
        return False


    def execute(self, context):
        mat = context.active_object.active_material
        #if mat.msfs_material_type == "NONE":
        nodes = mat.node_tree.nodes
        bsdfnodes = [n for n in nodes 
                if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
        for principled in bsdfnodes:
            if not principled.inputs[0].links:
                # now get emissive_tint node and check color same as Base Color on BSDF
                # get emissive_tint node
                #print("old_emissive_tint_color_diff execute - mat", mat)
                if mat.node_tree.nodes["emissive_tint"] is not None:
                    # get color
                    emissive_tint_checkval = mat.node_tree.nodes["emissive_tint"].outputs[0].default_value
                    # get BSDF base Color value
                    BSDF_Emission = principled.inputs["Emission"].default_value
                    #print("old_albedo_tint_color_diff execute - BSDF color", BSDF_Emission)
                    if not equality_check(BSDF_Emission, emissive_tint_checkval, len(BSDF_Emission), len(emissive_tint_checkval)):
                       mat.node_tree.nodes["emissive_tint"].outputs[0].default_value = BSDF_Emission
                       # should add like too to make button go away
        return {"FINISHED"}


class MSFS_OT_MigrateMaterialData(bpy.types.Operator): # TODO: Remove eventually
    """This addon changes some of the internal property names. This current material has older properties, and is able to be migrated.\nWARNING: This removes all the old properties from the material"""

    bl_idname = "msfs.migrate_material_data"
    bl_label = "Migrate Material Data"

    old_property_to_new_mapping = {
        "msfs_color_sss": "msfs_sss_color",
        "msfs_use_pearl_effect ": "msfs_use_pearl",
        "msfs_decal_color_blend_factor": "msfs_base_color_blend_factor",
        "msfs_decal_metal_blend_factor": "msfs_metallic_blend_factor",
        "msfs_decal_normal_blend_factor": "msfs_normal_blend_factor",
        "msfs_decal_roughness_blend_factor": "msfs_roughness_blend_factor",
        "msfs_decal_occlusion_blend_factor": "msfs_occlusion_blend_factor",
        "msfs_decal_emissive_blend_factor": "msfs_emissive_blend_factor",
        "msfs_fresnel_opacity_bias": "msfs_fresnel_opacity_offset",
        "msfs_parallax_room_number": "msfs_parallax_room_number_xy",
        "msfs_geo_decal_blend_factor_color": "msfs_base_color_blend_factor",
        "msfs_geo_decal_blend_factor_metal": "msfs_metallic_blend_factor",
        "msfs_geo_decal_blend_factor_normal": "msfs_normal_blend_factor",
        "msfs_geo_decal_blend_factor_roughness": "msfs_roughness_blend_factor",
        "msfs_geo_decal_blend_factor_blast_sys": "msfs_occlusion_blend_factor",
        "msfs_geo_decal_blend_factor_melt_sys": "msfs_emissive_blend_factor",
        "msfs_draw_order": "msfs_draw_order_offset",
        "msfs_road_material": "msfs_road_collision_material",
        "msfs_uv_clamp_x": "msfs_clamp_uv_x",
        "msfs_uv_clamp_y": "msfs_clamp_uv_y",
        "msfs_uv_clamp_z": "msfs_clamp_uv_z",
        "msfs_roughness_scale": "msfs_roughness_factor",
        "msfs_metallic_scale": "msfs_metallic_factor",
        "msfs_detail_uv_offset_x": "msfs_detail_uv_offset_u",
        "msfs_detail_uv_offset_y": "msfs_detail_uv_offset_v",
        "msfs_blend_threshold": "msfs_detail_blend_threshold",
        "msfs_albedo_texture": "msfs_base_color_texture",
        "msfs_metallic_texture": "msfs_occlusion_metallic_roughness_texture",
        "msfs_comp_texture": "msfs_occlusion_metallic_roughness_texture",
        "msfs_detail_albedo_texture": "msfs_detail_color_texture",
        "msfs_detail_metallic_texture": "msfs_detail_occlusion_metallic_roughness_texture",
        "msfs_anisotropic_direction_texture": "msfs_extra_slot1_texture",
        "msfs_clearcoat_texture": "msfs_dirt_texture",
        "msfs_behind_glass_texture": "msfs_detail_color_texture",
        "msfs_decal_blend_factor_color": "msfs_decal_color_blend_factor",
        "msfs_decal_blend_factor_roughness": "msfs_roughness_blend_factor",
        "msfs_decal_blend_factor_metal": "msfs_metallic_blend_factor",
        "msfs_decal_blend_factor_occlusion": "msfs_occlusion_blend_factor",
        "msfs_decal_blend_factor_normal": "msfs_normal_blend_factor",
        "msfs_decal_blend_factor_emissive": "msfs_emissive_blend_factor",
        "windshield": "msfs_windshield",
        "geo_decal": "msfs_base_color_blend_factor",
    }
    #"msfs_color_base_mix": " - related to vertex alpha node"
    #"msfs_decal_blend_factor_color": "msfs_decal_color_blend_factor",
    #"msfs_decal_blend_factor_roughness": "msfs_roughness_blend_factor",
    #"msfs_decal_blend_factor_metal": "msfs_metallic_blend_factor",
    #"msfs_decal_blend_factor_occlusion": "msfs_occlusion_blend_factor",
    #"msfs_decal_blend_factor_normal": "msfs_normal_blend_factor",
    #"msfs_decal_blend_factor_emissive": "msfs_emissive_blend_factor",
    #"windshield": "msfs_windshield",
    #"geo_decal": "msfs_base_color_blend_factor",
    # (yes without the msfs_   - vitus legacy)

    # not implemented
    # msfs_wiper_mask_texture, msfs_responsive_aa, msfs_ao_use_uv2 

    @staticmethod
    def old_properties_present(mat):
        if len(mat.keys()) > 0: # Don't unnecessarily loop if we have no properties on the material
            for old_property in MSFS_OT_MigrateMaterialData.old_property_to_new_mapping:
                if mat.get(old_property) is not None:
                    return True
        return False


    def execute(self, context):
        mat = context.active_object.active_material
        for (
            old_property,
            new_property,
        ) in MSFS_OT_MigrateMaterialData.old_property_to_new_mapping.items():
            if mat.get(old_property) is not None:
                # msfs_behind_glass_texture and msfs_detail_albedo_texture are special cases as they are they write to the same property
                if mat.get("msfs_material_mode") == "msfs_windshield" and old_property == "msfs_behind_glass_texture":
                    continue
                if mat.get("msfs_material_mode") == "msfs_parallax" and old_property == "msfs_detail_albedo_texture":
                    continue
                try:
                    #print("execute - make change", new_property, old_property)
                    mat[new_property] = mat[old_property]
                    #print("execute - make change new old", mat[new_property], mat[old_property])
                except:
                    print("execute - ERROR did not carry over", mat, old_property, new_property)

                del mat[old_property]

        # Base color is a special case - can only have 3 values, we need 4
        base_color = [1,1,1,1]
        alpha = 1
        if mat.get("msfs_color_alpha_mix"):
            alpha = mat.get("msfs_color_alpha_mix")
            base_color[3] = alpha
        else:
            print("execute - no msfs_color_alpha_mix", mat)
            try:
                n = mat.node_tree.nodes["albedo_tint"]
                #print(n, n.outputs[0], n.outputs[0].default_value)
                base_color[3] = n.outputs[0].default_value[3]
                #print(base_color)
            except:
                print("execute - Base Color Alpha - Error - albedo_tint not found skipping")
                try:
                    nodes = mat.node_tree.nodes
                    bsdfnodes = [n for n in nodes 
                            if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
                    for principled in bsdfnodes:
                        BSDF_Base_Color = principled.inputs["Base Color"].default_value
                        print("MSFS_OT_MigrateMaterialData execute - BSDF to MSFS base color alpha", BSDF_Base_Color[0], mat.msfs_base_color_factor[0], BSDF_Base_Color[1], mat.msfs_base_color_factor[1], BSDF_Base_Color[2], mat.msfs_base_color_factor[2], BSDF_Base_Color[3], mat.msfs_base_color_factor[3])
                        base_color[3] = principled.inputs["Base Color"].default_value[3]
                except:
                    print("execute - Base Color Alpha - Error - BSDF Base Color not found skipping")
            finally:
                pass

        if mat.get("msfs_color_albedo_mix"):
            base_color = list(mat.get("msfs_color_albedo_mix"))
            if len(base_color) == 3:
                base_color.append(alpha)
        else:
            print("execute - no msfs_color_albedo_mix", mat)
            try:
                n = mat.node_tree.nodes["albedo_tint"]
                #print(n, n.outputs[0], n.outputs[0].default_value)
                base_color = n.outputs[0].default_value
                #print(base_color)
            except:
                print("execute - Base Color - Error - albedo_tint not found skipping")
                try:
                    nodes = mat.node_tree.nodes
                    bsdfnodes = [n for n in nodes 
                            if isinstance(n, bpy.types.ShaderNodeBsdfPrincipled)]
                    for principled in bsdfnodes:
                        BSDF_Base_Color = principled.inputs["Base Color"].default_value
                        print("MSFS_OT_MigrateMaterialData execute - BSDF to MSFS base color", BSDF_Base_Color[0], mat.msfs_base_color_factor[0], BSDF_Base_Color[1], mat.msfs_base_color_factor[1], BSDF_Base_Color[2], mat.msfs_base_color_factor[2], BSDF_Base_Color[3], mat.msfs_base_color_factor[3])
                        base_color = BSDF_Base_Color
                except:
                    print("execute - Base Color - Error - BSDF Base Color not found skipping")
                    pass
            finally:
                pass
        mat.msfs_base_color_factor = base_color

        # Emissive factor is also a special case - old material system had 4 floats, we only need 3
        if mat.get("msfs_color_emissive_mix"):
            mat.msfs_emissive_factor = mat.get("msfs_color_emissive_mix")[0:3]
        else:
            try:
                #print("execute - no msfs_color_albedo_mix", mat)
                n = mat.node_tree.nodes["emissive_tint"]
                #print(n, n.outputs[0], n.outputs[0].default_value)
                emissive_color = n.outputs[0].default_value[0:3]
                #print(emissive_color)
                mat.msfs_emissive_factor = emissive_color
            except:
                print("execute - Emissive Color - Error - emissive_tint not found skipping")
                try:
                    print("MSFS_OT_MigrateMaterialData execute - BSDF to MSFS emissive color", BSDF_Base_Color[0], mat.msfs_emissive_factor[0], BSDF_Base_Color[1], mat.msfs_emissive_factor[1], BSDF_Base_Color[2], mat.msfs_emissive_factor[2], BSDF_Base_Color[3], mat.msfs_emissive_factor[3])
                    emissive_color = principled.inputs["Emission"].default_value
                    mat.msfs_emissive_factor = emissive_color
                except:
                    pass
            finally:
                pass

        # Do our enums manually as only their index of the value are stored - not the string
        if mat.get("msfs_blend_mode"):
            print("execute - msfs_blend_mode migrate check", mat.get("msfs_blend_mode"))
            old_alpha_order = [
                "OPAQUE",
                "MASK",  # Changed from old version - matches new name
                "BLEND",
                "DITHER",
            ]
            mat.msfs_alpha_mode = old_alpha_order[mat["msfs_blend_mode"]]

            del mat["msfs_blend_mode"]

        if mat.get("msfs_material_mode"):
            old_material_older = [  # Assuming the user uninstalled the old plugin, the index of the value will be stored instead of the name of the current material. Replicate the order here
                "NONE",
                "msfs_standard",
                "msfs_anisotropic",
                "msfs_sss",
                "msfs_glass",
                "msfs_geo_decal",  # Changed from old version - matches new name
                "msfs_clearcoat",
                "msfs_environment_occluder",  # Changed from old version - matches new name
                "msfs_fake_terrain",
                "msfs_fresnel_fade",  # Changed from old version - matches new name
                "msfs_windshield",
                "msfs_porthole",
                "msfs_parallax",
                "msfs_geo_decal_frosted",  # Changed from old version - matches new name
                "msfs_hair",
                "msfs_invisible",
                "msfs_ghost",  # added because my legacy mod has it????
            ]
            mat.msfs_material_type = old_material_older[mat["msfs_material_mode"]]

            del mat["msfs_material_mode"]

        print("Migrate material - Update Other properties", mat)
        MSFS_Material_Property_Update.update_msfs_material_type(mat, context)

        print("Migrate material - Done")
        return {"FINISHED"}


class MSFS_PT_Material(bpy.types.Panel):
    bl_label = "MSFS Material Params"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw_prop(self, layout, mat, prop, enabled=True, visible=True, text=""):
        if visible:
            column = layout.column()
            if text:
                column.prop(mat, prop, text=text)
            else:
                column.prop(mat, prop)

            column.enabled = enabled

    def draw_texture_prop(self, layout, mat, prop, enabled=True, visible=True, text=""):
        if visible:
            column = layout.column()
            if text:
                column.label(text=text)

            column.template_ID(mat, prop, new="image.new", open="image.open")
            column.enabled = enabled

    def draw(self, context):
        layout = self.layout
        # Disabled animation UI until material animations are properly implemented
        # layout.use_property_split = True
        # layout.use_property_decorate = True

        mat = context.active_object.active_material

        if mat:
            # if MSFS_OT_MigrateModeData.old_mode_diff(mat):
                # layout.operator(MSFS_OT_MigrateModeData.bl_idname)

            if MSFS_OT_MigrateColorFixData.old_material_values_diff(mat):
                layout.operator(MSFS_OT_MigrateColorFixData.bl_idname)

            if MSFS_OT_MigrateEmissiveFixData.old_emissive_tint_color_diff(mat):
                layout.operator(MSFS_OT_MigrateEmissiveFixData.bl_idname)

            if MSFS_OT_MigrateMaterialData.old_properties_present(mat):
                layout.operator(MSFS_OT_MigrateMaterialData.bl_idname)

            #print("MSFS_PT_Material draw", mat.msfs_material_type)

            self.draw_prop(layout, mat, "msfs_material_type")
            if mat.msfs_material_type == "NONE" and mat.msfs_material_mode != "NONE":
                self.draw_prop(layout, mat, "msfs_material_mode", enabled=False)

            if mat.msfs_material_type != "NONE" or mat.msfs_material_mode != "NONE":
                self.draw_prop(layout, mat, "msfs_base_color_factor")
                self.draw_prop(
                    layout,
                    mat,
                    "msfs_emissive_factor",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_invisible", "msfs_environment_occluder"]
                    ),
                )

                # Alpha mode
                box = layout.box()
                box.label(text="Alpha Mode")
                box.enabled = mat.msfs_material_type in [
                    "msfs_standard",
                    "msfs_anisotropic",
                    "msfs_hair",
                    "msfs_sss",
                    "msfs_fresnel_fade",
                    "msfs_clearcoat",
                ]
                self.draw_prop(box, mat, "msfs_alpha_mode")

                # Render params
                box = layout.box()
                box.label(text="Render Parameters")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_draw_order_offset")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_no_cast_shadow",
                    enabled=(mat.msfs_material_type != "msfs_ghost"),
                )
                self.draw_prop(box, mat, "msfs_double_sided")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_day_night_cycle",
                    enabled=(mat.msfs_material_type == "msfs_standard"),
                )
                self.draw_prop(box, mat, "msfs_disable_motion_blur")

                # Gameplay params
                box = layout.box()
                box.label(text="Gameplay Parameters")
                box.enabled = mat.msfs_material_type != "msfs_environment_occluder"
                self.draw_prop(box, mat, "msfs_collision_material")
                self.draw_prop(box, mat, "msfs_road_collision_material")

                # UV options
                box = layout.box()
                box.label(text="UV Options")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_uv_offset_u")
                self.draw_prop(box, mat, "msfs_uv_offset_v")
                self.draw_prop(box, mat, "msfs_uv_tiling_u")
                self.draw_prop(box, mat, "msfs_uv_tiling_v")
                self.draw_prop(box, mat, "msfs_uv_rotation")

                # UV clamp
                box = layout.box()
                box.label(text="UV Clamp")
                box.enabled = mat.msfs_material_type != "msfs_environment_occluder"
                self.draw_prop(box, mat, "msfs_clamp_uv_x")
                self.draw_prop(box, mat, "msfs_clamp_uv_y")

                # General params
                box = layout.box()
                box.label(text="General Parameters")
                box.enabled = mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]
                self.draw_prop(box, mat, "msfs_metallic_factor")
                self.draw_prop(box, mat, "msfs_roughness_factor")
                self.draw_prop(box, mat, "msfs_normal_scale")
                self.draw_prop(
                    box,
                    mat,
                    "msfs_alpha_cutoff",
                    enabled=(
                        mat.msfs_material_type
                        in [
                            "msfs_standard",
                            "msfs_anisotropic",
                            "msfs_hair",
                            "msfs_sss",
                            "msfs_fresnel_fade",
                            "msfs_clearcoat",
                        ]
                        and mat.msfs_alpha_mode == "MASK"
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_scale",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_offset_u",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_uv_offset_v",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_normal_scale",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_parallax", "msfs_fresnel_fade", "msfs_sss"]
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_detail_blend_threshold",
                    enabled=(
                        mat.msfs_material_type not in ["msfs_fresnel_fade", "msfs_sss"]
                        and mat.msfs_blend_mask_texture is not None
                    ),
                )
                self.draw_prop(
                    box,
                    mat,
                    "msfs_emissive_scale",
                    enabled=(
                        mat.msfs_material_type
                        not in ["msfs_invisible", "msfs_environment_occluder"]
                    ),
                )

                # Decal params
                if mat.msfs_material_type in [
                    "msfs_geo_decal",
                    "msfs_geo_decal_frosted",
                ]:
                    box = layout.box()
                    box.label(text="Decal Blend Factors")
                    box.enabled = mat.msfs_material_type in [
                        "msfs_geo_decal",
                        "msfs_geo_decal_frosted",
                    ]
                    self.draw_prop(box, mat, "msfs_base_color_blend_factor")
                    self.draw_prop(box, mat, "msfs_roughness_blend_factor")
                    self.draw_prop(box, mat, "msfs_metallic_blend_factor")
                    self.draw_prop(
                        box,
                        mat,
                        "msfs_occlusion_blend_factor",
                        text="Blast Sys Blend Factor"
                        if mat.msfs_material_type == "msfs_geo_decal_frosted"
                        else "",
                    )
                    self.draw_prop(box, mat, "msfs_normal_blend_factor")
                    self.draw_prop(
                        box,
                        mat,
                        "msfs_emissive_blend_factor",
                        text="Melt Sys Blend Factor"
                        if mat.msfs_material_type == "msfs_geo_decal_frosted"
                        else "",
                    )

                # SSS params - enabled
                if mat.msfs_material_type in ["msfs_sss", "msfs_hair"]:
                    box = layout.box()
                    box.label(text="SSS Parameters")
                    box.enabled = (mat.msfs_material_type  == "msfs_sss") or (mat.msfs_material_type == "msfs_hair")
                    self.draw_prop(
                        box, mat, "msfs_sss_color", enabled=True
                    )

                # Glass params
                if mat.msfs_material_type == "msfs_glass":
                    box = layout.box()
                    box.label(text="Glass Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_glass"
                    self.draw_prop(box, mat, "msfs_glass_reflection_mask_factor")
                    self.draw_prop(box, mat, "msfs_glass_deformation_factor")

                # Parallax params
                if mat.msfs_material_type == "msfs_parallax":
                    box = layout.box()
                    box.label(text="Parallax Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_parallax"
                    self.draw_prop(box, mat, "msfs_parallax_scale")
                    self.draw_prop(box, mat, "msfs_parallax_room_size_x")
                    self.draw_prop(box, mat, "msfs_parallax_room_size_y")
                    self.draw_prop(box, mat, "msfs_parallax_room_number_xy")
                    self.draw_prop(box, mat, "msfs_parallax_corridor")

                # Fresnel params
                if mat.msfs_material_type == "msfs_fresnel_fade":
                    box = layout.box()
                    box.label(text="Fresnel Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_fresnel_fade"
                    self.draw_prop(box, mat, "msfs_fresnel_factor")
                    self.draw_prop(box, mat, "msfs_fresnel_opacity_offset")

                # Ghost params
                if mat.msfs_material_type == "msfs_ghost":
                    box = layout.box()
                    box.label(text="Ghost Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_ghost"
                    self.draw_prop(box, mat, "msfs_ghost_bias")
                    self.draw_prop(box, mat, "msfs_ghost_power")
                    self.draw_prop(box, mat, "msfs_ghost_scale")

                # Windshield params
                if mat.msfs_material_type == "msfs_windshield":
                    box = layout.box()
                    box.label(text="Windshield Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_windshield"
                    self.draw_prop(box, mat, "msfs_rain_drop_scale")
                    self.draw_prop(box, mat, "msfs_wiper_1_state")
                    self.draw_prop(box, mat, "msfs_wiper_2_state")
                    self.draw_prop(box, mat, "msfs_wiper_3_state", visible=False)
                    self.draw_prop(box, mat, "msfs_wiper_4_state", visible=False)

                # Pearl params
                if mat.msfs_material_type == "msfs_standard":
                    box = layout.box()
                    box.label(text="Pearl Parameters")
                    box.enabled = mat.msfs_material_type == "msfs_standard"
                    self.draw_prop(box, mat, "msfs_use_pearl")
                    self.draw_prop(box, mat, "msfs_pearl_shift")
                    self.draw_prop(box, mat, "msfs_pearl_range")
                    self.draw_prop(box, mat, "msfs_pearl_brightness")

                # Textures
                if mat.msfs_material_type not in [
                    "msfs_invisible",
                    "msfs_environment_occluder",
                ]:
                    box = layout.box()
                    box.label(text="Textures")

                    # In the 3DS Max exporter, the textures have different display names depending on material type and other properties used. We replicate that process here
                    base_color_tex_name = "Base Color"
                    occlusion_metallic_roughness_texture_name = (
                        "Occlusion (R), Roughness (G), Metallic (B)"
                    )
                    normal_texture_name = "Normal"
                    blend_mask_texture_name = "Blend Mask"
                    dirt_texture_name = "Clearcoat amount (R), Clearcoat rough (G)"
                    extra_slot1_texture = "Extra Slot 1"
                    emissive_texture_name = "Emissive"
                    detail_color_texture_name = "Secondary Color (RGB), Alpha (A)"
                    detail_occlusion_metallic_roughness_texture_name = (
                        "Secondary Occ (R), Rough (G), Metal (B)"
                    )
                    detail_normal_texture_name = "Secondary Normal"

                    if mat.msfs_blend_mask_texture is None:
                        detail_color_texture_name = "Detail Color (RGB), Alpha (A)"
                        detail_normal_texture_name = "Detail Normal"
                        detail_occlusion_metallic_roughness_texture_name = (
                            "Detail Occlusion (R), Roughness (G), Metallic (B)"
                        )

                    if mat.msfs_material_type == "msfs_windshield":
                        emissive_texture_name = "Secondary Details(A)"
                        extra_slot1_texture = "Wiper Mask (RG)"
                        detail_color_texture_name = (
                            "Details Scratch(R), Icing Mask(Dirt)(G), Fingerprints(B)"
                        )
                        detail_normal_texture_name = "Icing Normal (use DetailMap UV)"
                    elif mat.msfs_material_type == "msfs_geo_decal_frosted":
                        detail_occlusion_metallic_roughness_texture_name = (
                            "Melt pattern (R), Roughness (G), Metallic (B)"
                        )
                    elif mat.msfs_material_type == "msfs_parallax":
                        base_color_tex_name = "Front Glass Color"
                        normal_texture_name = "Front Glass Normal"
                        detail_color_texture_name = (
                            "Behind Glass Color (RGB), Alpha (A)"
                        )
                        emissive_texture_name = (
                            "Emissive Ins Window (RGB), offset Time (A)"
                        )
                    elif mat.msfs_material_type in ["msfs_anisotropic", "msfs_hair"]:
                        extra_slot1_texture = "Anisotropic direction (RG)"

                    self.draw_texture_prop(
                        box, mat, "msfs_base_color_texture", text=base_color_tex_name
                    )
                    self.draw_texture_prop(
                        box,
                        mat,
                        "msfs_occlusion_metallic_roughness_texture",
                        text=occlusion_metallic_roughness_texture_name
                    )
                    self.draw_texture_prop(
                        box, mat, "msfs_normal_texture", text=normal_texture_name
                    )
                    self.draw_texture_prop(
                        box, mat, "msfs_emissive_texture", text=emissive_texture_name
                    )

                    if mat.msfs_material_type not in [
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_color_texture",
                            text=detail_color_texture_name,
                        )
                    if mat.msfs_material_type not in [
                        "msfs_parallax",
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_normal_texture",
                            text=detail_normal_texture_name,
                        )
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_detail_occlusion_metallic_roughness_texture",
                            text=detail_occlusion_metallic_roughness_texture_name,
                        )
                    if mat.msfs_material_type not in [
                        "msfs_geo_decal_frosted",
                        "msfs_parallax",
                        "msfs_hair",
                        "msfs_sss",
                        "msfs_fresnel_fade",
                        "msfs_ghost",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_blend_mask_texture",
                            text=blend_mask_texture_name,
                        )
                    if mat.msfs_material_type in [
                        "msfs_winshield",
                        "msfs_anisotropic",
                        "msfs_hair",
                    ]:
                        self.draw_texture_prop(
                            box,
                            mat,
                            "msfs_extra_slot1_texture",
                            text=extra_slot1_texture,
                        )
                    if mat.msfs_material_type == "msfs_clearcoat":
                        self.draw_texture_prop(
                            box, mat, "msfs_dirt_texture", text=dirt_texture_name
                        )
