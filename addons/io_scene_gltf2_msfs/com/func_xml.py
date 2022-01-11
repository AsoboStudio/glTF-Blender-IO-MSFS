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

import xml.etree.ElementTree as etree
import re

def parse_xml_behavior(filename):
    print("Parsing <%s>..."%filename)
    number_of_behaviors = 0

#    parser = etree.XMLParser(encoding="utf-8")

#    try:
#        tree = etree.parse(filename, parser)
#    except FileNotFoundError:
#        msg = "Couldn't read the XML file under: <%s>"%filename
#        return -1
#    root = tree.getroot()

    with open(filename) as f:
        try:
            xml = f.read()
        except:
            msg= "Couldn't read the XML file under: <%s>"%filename
            print(msg)
            return 0
    
    #We need to remove the xml node to continue.
    xml = re.sub('<[?]xml.*[?]>', '', xml)

    #Since Asobo doesn't stick to conventions, we need to add a root-node to the file:
    xml = '<root>'+xml+'</root>'

    root = etree.fromstring(xml.lstrip())

    for element in root:
        if element.tag == "Template":
            if 'Name' in element.attrib:
                behavior = bpy.context.scene.msfs_behavior.add()
                behavior.name = element.attrib['Name']
                behavior.source_file = filename
                number_of_behaviors += 1
        elif element.tag == "ModelInfo":
            for animation in element:
                if animation.tag == "Animation":
                    if 'name' in animation.attrib:
                        behavior = bpy.context.scene.msfs_behavior.add()
                        behavior.name = animation.attrib['name']
                        if 'length' in animation.attrib:
                            behavior.anim_length = int(animation.attrib['length'])
                        behavior.source_file = filename
                        number_of_behaviors += 1
        elif element.tag == "ModelBehaviors":
            for component in element:
                if component.tag == "Component":
                    for template in component:
                        if template.tag == "UseTemplate":
                            if 'ANIM_NAME' in template.attrib:
                                behavior = bpy.context.scene.msfs_behavior.add()
                                behavior.name = animation.attrib['ANIM_NAME']
                                behavior.source_file = filename
                                number_of_behaviors += 1


    msg = "Appended %i behaviors."%number_of_behaviors
    print(msg)

    return number_of_behaviors





