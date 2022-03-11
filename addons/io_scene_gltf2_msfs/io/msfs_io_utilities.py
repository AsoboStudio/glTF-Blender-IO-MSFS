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
from mathutils import Vector, Quaternion

from io_scene_gltf2.blender.com.gltf2_blender_math import (
    swizzle_yup_location,
    swizzle_yup_rotation,
)


def get_bounding_box_center(obj):
    """
    Calculate the center of a mesh

    :param obj: a blender object
    :return: a translation Vector
    """
    local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
    global_bbox_center = obj.matrix_world @ local_bbox_center

    return global_bbox_center


def get_flight_sim_location(node, parent_node):
    """
    For nodes such as a gizmo, we need to calculate location relative to the parent node

    :param node: the blender node we want to get the location of
    :param parent_node: the parent of the node
    :return: location as type list
    """
    global_bbox_center = get_bounding_box_center(parent_node)

    loc = node.matrix_local.inverted() @ global_bbox_center

    return list(swizzle_yup_location(loc))


def get_flight_sim_rotation(node, parent_node):
    """
    For nodes such as a gizmo, we need to calculate rotation relative to the parent node

    :param node: the blender node we want to get the rotation of
    :param parent_node: the parent of the node
    :return: rotation as type list
    """
    transformed_matrix = node.matrix_local @ parent_node.matrix_local.inverted()

    return list(swizzle_yup_rotation(transformed_matrix.to_quaternion()))


def is_default_rotation(rotation):
    """
    Check if object rotation is default

    :param rotation: a quaternion
    :return: bool
    """
    return (
        (rotation[0] == 1.0 or rotation[0] == -1.0)
        and rotation[1] == 0.0
        and rotation[2] == 0.0
        and rotation[3] == 0.0
    )


def gltf_location_to_blender(loc):
    """
    Convert glTF location to a blender Vector

    :param loc: glTF location
    :return: Vector
    """
    return Vector(loc)


def gltf_rotation_to_blender(rot):
    """
    Convert glTF rotation to a blender Quaternion

    :param rot: glTF rotation
    :return: Quaternion
    """
    return Quaternion((rot[3], rot[0], rot[1], rot[2]))
