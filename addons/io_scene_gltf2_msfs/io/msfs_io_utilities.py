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
from mathutils import Vector, Quaternion, Matrix

from io_scene_gltf2.blender.com.gltf2_blender_math import (
    swizzle_yup_location,
    swizzle_yup_rotation,
)
from io_scene_gltf2.blender.com import gltf2_blender_math

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


def get_trs(node):
    if node.parent is None:
        trans, rot, sca = node.matrix_world.decompose()
    else:
        # Calculate local matrix
        trans, rot, sca = (
            node.parent.matrix_world.inverted_safe() @ node.matrix_world
        ).decompose()

    rot.normalize()

    trans = convert_swizzle_location(trans)
    rot = convert_swizzle_rotation(rot)
    sca = convert_swizzle_scale(sca)

    if node.instance_type == "COLLECTION" and node.instance_collection:
        offset = convert_swizzle_location(node.instance_collection.instance_offset)

        s = Matrix.Diagonal(sca).to_4x4()
        r = rot.to_matrix().to_4x4()
        t = Matrix.Translation(trans).to_4x4()
        o = Matrix.Translation(offset).to_4x4()
        m = t @ r @ s @ o

        trans = m.translation

    translation, rotation, scale = (None, None, None)
    trans[0], trans[1], trans[2] = (
        gltf2_blender_math.round_if_near(trans[0], 0.0),
        gltf2_blender_math.round_if_near(trans[1], 0.0),
        gltf2_blender_math.round_if_near(trans[2], 0.0),
    )
    rot[0], rot[1], rot[2], rot[3] = (
        gltf2_blender_math.round_if_near(rot[0], 1.0),
        gltf2_blender_math.round_if_near(rot[1], 0.0),
        gltf2_blender_math.round_if_near(rot[2], 0.0),
        gltf2_blender_math.round_if_near(rot[3], 0.0),
    )
    sca[0], sca[1], sca[2] = (
        gltf2_blender_math.round_if_near(sca[0], 1.0),
        gltf2_blender_math.round_if_near(sca[1], 1.0),
        gltf2_blender_math.round_if_near(sca[2], 1.0),
    )
    if trans[0] != 0.0 or trans[1] != 0.0 or trans[2] != 0.0:
        translation = [trans[0], trans[1], trans[2]]
    if rot[0] != 1.0 or rot[1] != 0.0 or rot[2] != 0.0 or rot[3] != 0.0:
        rotation = [rot[1], rot[2], rot[3], rot[0]]
    if sca[0] != 1.0 or sca[1] != 1.0 or sca[2] != 1.0:
        scale = [sca[0], sca[1], sca[2]]

    return translation, rotation, scale


def convert_swizzle_location(loc):
    """Convert a location from Blender coordinate system to glTF coordinate system."""
    return Vector((loc[0], loc[2], -loc[1]))


def convert_swizzle_rotation(rot):
    """
    Convert a quaternion rotation from Blender coordinate system to glTF coordinate system.

    'w' is still at first position.
    """
    return Quaternion((rot[0], rot[1], rot[3], -rot[2]))


def convert_swizzle_scale(scale):
    """Convert a scale from Blender coordinate system to glTF coordinate system."""
    return Vector((scale[0], scale[2], scale[1]))
