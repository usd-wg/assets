# Source Files

This folder contains the souce files used to generate the maps and data. Some of these items may have scripts to automate export, while others are authored directly. The majority of these source files are temporary, and only used to generate data.

## Scene

To re-generate the USD files from Houdini, go to `/stage/OUT_export_scene` and click *Save to Disk*. When modifications are made directly to the USD files, please note those changes here to clarify expectations when re-generating data from the source files.

The output locations and other high-level info is controlled from `/stage/ctrl`.

## Maps

To re-generate the maps, Inkscape and OpenImageIO's oiiotool are required. The necessary fonts are included in the file, but Inkscape requires they be installed to the system first.

1. Export the maps using Inkscape from `maps.svg` as RGBA 8-bit, uncompressed .png; this is easiest done from the GUI. If you change the output names or locations, you'll need to update the Python script used in step 2.
2. Run the `generates_maps.py` script, which color-maps those generated images and converts them to ACEScg .exr images; that script also generates the UV Grid and Number Grid maps.

The .svg document has each maps resolution set by the page, with a DPI of 96. Most are 2048x2048, some 1024x1024, and the smaller emitter icons are 256x256. The easiest way to change the resolution, is to adjust the DPI on the Export dialog in Inkscape. For example, to output 4096x4096 maps, you would set the DPI to 192.

## Documentation

To update some of the figures:

1. Render all of the IMG-prefixed USD Render ROPs
2. Open `annotated_images.svg` in Inkscape.
3. Batch Export > Pages, and export all of the images.

The rest of the images were generated from screenshots manually. In the future perhaps those could be easily updated as well.

To re-render the cover image, some of the following texture maps need to be placed next to `setup.hip`, in a folder called *cover*:

* https://polyhaven.com/a/bark_willow
* https://ambientcg.com/view?id=Terrazzo009
* https://polyhaven.com/a/calathea_orbifolia_01

Thank you to PolyHaven and AmbientCG for generously sharing these Public Domain - CC0 assets!
