[![MSFS](misc/msfs_logo.png)](https://www.flightsimulator.com/)[![ASOBO](misc/asobo_logo.png)](https://www.asobostudio.com/)

FlightSim Blender glTF 2.0 Importer and Exporter
======================================

This repository represents an alpha version of the official FlightSim-Blender Import/Export plugin. The flight sim community has already developed and forked the original project many times, and Asobo's intention is to fully support Blender with the contributions of all the developers that already developed many features in different unofficial Blender plugins.

Asobo especially thanks:

Vitus of [Wing42](https://wing42.com/), [tml1024](https://github.com/tml1024), [ronh991](https://github.com/ronh991), [pepperoni505](https://github.com/pepperoni505) of [FlyByWire](https://flybywiresim.com/)


Installation
===========
Option 1

1. Download the latest release
2. Decompress the file
3. Open the `addons` folder
4. Copy-paste the `io_scene_gltf2_msfs` folder into your Blender installation's `scripts/addons/` folder.
   1. Windows: this will usually be in `C:\Program Files\Blender Foundation\Blender 3.1\3.1\scripts\addons\`.
   2. Mac OS X: this will be in your Library (Press the Option key when in Finder's `Go` menu to open your Library folder): `\Users\<username>\Library\Application Support\Blender\3.1\scripts\addons\`.
   
Option 2

1. Download the latest release
2. Decompress the file
3. Open the `addons` folder
4. Use windows file manager and right-click and send to compressed file.
   Use the compressed zip file and then in Blender menu Edit Preferences
   Select the install option and navigate to the zip file you just created.
   Install this zip file.
   Enable the addon by checking the checkbox.
   Close the preferences dialog

Migration of Legacy blend file MSFS Material types/modes 
to ASOBO exporter MSFS Material types/Modes
========================================================

Every effort has been made to allow legacy blend files to be used by this exporter.
The legacy blend files contain data that is used to create gltf ver 2.0 files
for use in the Microsoft Flight Simulator.  The ASOBO version of the exporter uses the
Khronos default code and adds hooks to this code for the ASOBO extensions used in the gltf files.
The legacy exporter had hard coded the required extensions.
The ASOBO exporter now has a much more complex and versitile material node structure
seen in the Shader tab/window in Blender.

Migrate from Legacy Exporter
============================

Open your blend file.
Select an object/node/mesh
Open the MSFS Material Panel
You will see a migrate button above the MSFS Material drop down button.
DO NOT Select a MSFS Material from the drop down, this will erase the existing legacy
data and you will lose all your material settings.
Click on the migrate button
Your existing legacy material Type/mode will conovert to the new ASOBO material shader node
structure.

Figure 1 Before migration

Figure 2 After Migration

Every effort has been made to copy all the settings from the legacy node structure to
the ASOBO exporter shader node structure, but you can see in the pictures the ASOBO node 
structure is more complete and there are a lot more nodes.  Sometimes developers have made 
changes to the legacy bsdf node and not reflected those changes in the panel data. A
lot of the variables that are migrated come from the legacy panel data, so there are
situations where your material will not look correct.  At this time you need to compare
your legacy blend file to the new file, so open your legacy blend file in another blender program
and compare the MSFS Material panel values.  Adjust acordingly.

Each MSFS material will need to be migrated, but any mesh nodes associated to that material 
will be migrated, so you only have to worry about one material, not all the mesh nodes.

You may also notice that some material panel parameters show data but cannot be adjusted, this is in
keeping with the ASOBO 3DS Max exporter.  Raise an issue if this is not to your requirements.

WARNING
=======

After migration SAVE YOUR FILE AS A NEW FILE and keep your legacy blend file for future reference.

