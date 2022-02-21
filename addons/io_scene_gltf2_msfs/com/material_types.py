# from . import msfs_material
import bpy

# class Material:
#     def get_blender_values(mat, property):
#         keys = property.__dict__.keys()
#         values = {}
#         for key in keys:
#             values[key] = getattr(mat, key)

#         return values
# class Standard:
#     def __init__(self):

#         # layout = gltf schema for standard
#         # sync between bpy/data
#         # create/export

#         self.uv_options = msfs_material.AsoboMaterialUVOptions()

# class Standard:

#     def uiOptions():


class MSFS_PT_material(bpy.types.Panel):
    bl_label = "MSFS Material Params"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw_prop(self, layout, mat, prop, enabled=True):
        if enabled:
            layout.prop(mat, prop)
    
    def draw(self, context):
        layout = self.layout

        mat = context.active_object.active_material

        if mat:
            self.draw_prop(layout, mat, "msfs_material_type")

            if mat.msfs_material_type != "NONE":
                self.draw_prop(layout, mat, "msfs_base_color_factor")
                self.draw_prop(layout, mat, "msfs_emissive_factor", enabled=(mat.msfs_material_type not in ["msfs_invisible", "msfs_environment_occluder"]))

                # TODO: sections
                # alpha mode
                self.draw_prop(layout, mat, "msfs_alpha_mode")

                # render param
                self.draw_prop(layout, mat, "msfs_draw_order")
                self.draw_prop(layout, mat, "msfs_no_cast_shadow")
                self.draw_prop(layout, mat, "msfs_double_sided")
                self.draw_prop(layout, mat, "msfs_day_night_cycle")

                # gameplay param
                # self.draw_prop(layout, mat, "msfs_")
                # self.draw_prop(layout, mat, "msfs_day_night_cycle")


