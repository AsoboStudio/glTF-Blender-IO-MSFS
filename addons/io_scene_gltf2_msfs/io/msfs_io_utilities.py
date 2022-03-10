# glTF-Blender-IO-MSFS
# Copyright (C) 2022 The glTF-Blender-IO-MSFS authors

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
from mathutils import Vector

from io_scene_gltf2.blender.com.gltf2_blender_math import (
    swizzle_yup_location,
    swizzle_yup_rotation,
)


def get_flight_sim_location(node, parent_node):
    """
    For nodes such as a gizmo, we need to calculate location relative to the parent node

    :param node: the blender node we want to get the location of
    :param parent_node: the parent of the node
    """

    # Get parent node bounding box center
    local_bbox_center = 0.125 * sum(
        (Vector(b) for b in parent_node.bound_box), Vector()
    )
    global_bbox_center = (
        parent_node.matrix_world * local_bbox_center
    )  # TODO: do we need global? also order of matrix multiplication

    transformed_matrix = node.matrix_local.inverted() @ global_bbox_center

    loc = transformed_matrix.to_translation()

    return swizzle_yup_location(loc)


def get_flight_sim_rotation(node, parent_node):
    """
    For nodes such as a gizmo, we need to calculate rotation relative to the parent node

    :param node: the blender node we want to get the rotation of
    :param parent_node: the parent of the node
    """
    transformed_matrix = (
        node.matrix_local @ parent_node.matrix_local.inverted()
    )  # TODO: matrix order

    # TODO: matrix decomposition?

    return swizzle_yup_rotation(transformed_matrix.to_quaternion())


def is_default_rotation(rotation):
    return (
        rotation[0] == 0.0
        and rotation[1] == 0.0
        and rotation[2] == 0.0
        and (rotation[3] == 1.0 or rotation[3] == -1.0)
    )
