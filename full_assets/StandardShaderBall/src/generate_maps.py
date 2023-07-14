#!/bin/env python3
#
# Generates the texture maps and uvgrid and other utility textures/images.
#
# The BASE_MAPS are exported from the maps.svg file using Inkscape, as uncompressed
# sRGB 8-bit .png files. In the future, it'd be nice to include that process in this
# script. Those .png files are 2048x2048@96dpi currently. Adjust the DPI in the export
# dialog to change the resolution; 4k would be 192dpi.
#
# `oiiotool` is expected to be available in the system search path.
#
# Usage: `python3 generate_maps.py`
#
# Note that some of the logic assumes that the UVMAP_RES is divisible by UVMAP_TILES

import os
from subprocess import Popen
from pathlib import Path
import string
import sys

# Shared globals
OIIOTOOL        = 'hoiiotool'
CWD             = Path(__file__).parent
UVMAP_FONT      = str((CWD / 'fonts/Roboto/Roboto-Bold.ttf').resolve())
UVMAP_THIN_FONT = str((CWD / 'fonts/Roboto/Roboto-Regular.ttf').resolve())
NUMBER_FONT     = str((CWD / 'fonts/Lato/Lato-Regular.ttf').resolve())
SSS_BAR_FONT    = str((CWD / 'fonts/Lato/Lato-Regular.ttf').resolve())
DEST_DIR        = str((CWD / '../maps').resolve())
EXR_TYPE        = "half"

# UV grid map globals
UVMAP_TILES     = 10
UVMAP_RES       = 200 * UVMAP_TILES

# Other map globals
BASE_MAPS       = [
    '_emitter_bulb_and_ribbon.png',
    '_emitter_bulb.png',
    '_emitter_ribbon.png',
    '_neutral.png',
    '_wall_back.png',
    '_wall_front.png',
    '_wall_left.png',
    '_wall_right.png',
    '_wall_top.png'
]

MAP_COLOR1       = '0.625,0.625,0.625'
MAP_COLOR2       = '0.18,0.18,0.18'

SSS_BAR_BASE_MAP = str((CWD / '_sss_bars.png').resolve())
SSS_MAP_COLOR1   = '0.4,0.4,0.4'
SSS_MAP_COLOR2   = '0.025,0.025,0.025'


#
# Generate UV Grid
#

def oiio_uv_grid_map(oiio_cmd, tiles=10, resolution=2000, font=UVMAP_FONT, thin_font=UVMAP_THIN_FONT):
    """
    Appends the necessary parts to the cmd list to generate the alternating grid.
    """

    # Array of ascii uppercase letters in reverse order
    letters = string.ascii_uppercase[:tiles][::-1]

    tileres = int(resolution/tiles)

    # These arbitrary scales are chosen to look nice
    fontsize      = int(tileres * 0.3625)
    #num_fontsize  = int(tileres * 0.3)
    num_fontsize  = int(tileres * 0.2)
    thin_fontsize = int(tileres * 0.1)

    # Add images onto the oiiotool's stack
    for y in range(tiles):
        for x in range(tiles):

            # The letter for this tile label
            letter = letters[y]
            # Padded numbers
            num = ("%02d") % (x + 1)

            white  = '1.0,1.0,1.0'
            yellow = '1.0,1.0,0.0'
            black  = '0.0,0.0,0.0'

            # Setup the empty canvas of the image
            oiio_cmd.append(f'--pattern constant:color={black},0.0 {tileres}x{tileres} 4')

            # Dark centre lines drawn first since we want the borders to overwrite them
            oiio_cmd.append(f'--line:color={black},0.4 0,{{TOP.height*0.5}},{{TOP.width-1}},{{TOP.height*0.5}}')
            oiio_cmd.append(f'--line:color={black},0.4 {{TOP.width*0.5}},0,{{TOP.width*0.5}},{{TOP.height-1}}')

            # Draw two white squares inside each other at the border
            oiio_cmd.append(f'--line:color={white},1.0 0,0,{{TOP.width-1}},0,{{TOP.width-1}},{{TOP.height-1}},0,{{TOP.height-1}},0,0,{{TOP.width-1}},0')
            oiio_cmd.append(f'--line:color={white},1.0 1,1,{{TOP.width-2}},1,{{TOP.width-2}},{{TOP.height-2}},1,{{TOP.height-2}},1,1,{{TOP.width-2}},1')

            # Only print the tile labels on the diagonals for a less crowded layout
            if ((x + y) % 2 == 1):
                # Letters are in white
                oiio_cmd.append(f'--text:x={{TOP.width*0.25}}:y={{TOP.height*0.5}}:color={white},1.0:xalign=center:yalign=center:font={font}:size={fontsize} "{letter}"')
                # Numbers are in yellow
                oiio_cmd.append(f'--text:x={{TOP.width*0.75}}:y={{TOP.height*0.25}}:color={yellow},1.0:xalign=center:yalign=center:font={font}:size={num_fontsize} "{num}"')

            # Corner box and UV Coordinates should only have one decimal point
            uv_coord = ("%0.1f, %0.1f") % (float(x)/tiles, float(tiles - y - 1)/tiles)
            oiio_cmd.append(f'--text:x=24:y={{TOP.height-16}}:color={white},1.0:xalign=left:yalign=base:font={thin_font}:size={thin_fontsize} "{uv_coord}"')
            # Add a "." to indicate the origin of the tile
            oiio_cmd.append(f'--text:x=1:y={{TOP.height-6}}:color={white},1.0:xalign=left:yalign=base:font={thin_font}:size={fontsize} "."')

    # Tile the stack's images into a grid
    oiio_cmd.append(f'--mosaic {tiles}x{tiles}')

    return oiio_cmd


# Call the grid function to build that part of the oiiotool command
oiio_cmd = oiio_uv_grid_map([f'{OIIOTOOL}'], tiles=UVMAP_TILES, resolution=UVMAP_RES)

# Creates the background color grid by making a small images, and scaling it up
blue   = '0.0,0.0,0.5'
green  = '0.0,0.5,0.0'
yellow = '0.5,0.5,0.0'
red    = '0.5,0.0,0.0'
oiio_cmd.append(f'--pattern fill:bottomleft={blue}:topleft={green}:topright={yellow}:bottomright={red} {UVMAP_TILES}x{UVMAP_TILES} 3')

print("Generating UV Grid...", end='', flush=True)

# The '--over' overlays the mosaic onto the colour grid
oiio_cmd.append(f'--resize:filter=box {UVMAP_RES}x{UVMAP_RES} --ch R,G,B,A=1.0 --over')
oiio_cmd.append(f'--ch R,G,B -o:type={EXR_TYPE} {DEST_DIR}/uvgrid.exr')

Popen(' '.join(oiio_cmd), shell=True).wait()

print("done.")


#
# Ground Number Grid
#

print("Generating Number Grid", end='', flush=True)

padding  = 2
tileres  = 298
fontsize = 110
white    = '1.0,1.0,1.0'
black    = '0.0,0.0,0.0'

# Split the initial images into rows, as Popen() doesn't allow the super-long oiiotool command, shell=True).wait()
for x in range(24,-1,-1):
    oiio_cmd = [f'{OIIOTOOL}']
    for i in range(x*25+1,x*25+26):
        oiio_cmd.append(f'--pattern constant:color={white},1.0 {tileres}x{tileres} 4')
        number = str(i).zfill(3)
        oiio_cmd.append(f'--text:x={{TOP.width*0.5}}:y={{TOP.height*0.5}}:color={black},1.0:xalign=center:yalign=center:font={NUMBER_FONT}:size={fontsize} "{number}"')
    oiio_cmd.append(f'--mosaic:pad={padding} 25x1')
    oiio_cmd.append(f'--ch R,G,B -o:type={EXR_TYPE} {DEST_DIR}/part_{x}.exr')
    # Status update
    print(".", end='', flush=True)
    Popen(' '.join(oiio_cmd), shell=True).wait()

# Merge the parts, and apply the color map
oiio_cmd = [f'{OIIOTOOL}']
for x in range(24,-1,-1):
    oiio_cmd.append(f'{DEST_DIR}/part_{x}.exr')
oiio_cmd.append(f'--mosaic:pad={padding} 1x25')
oiio_cmd.append(f'--colormap {MAP_COLOR2},{MAP_COLOR1}')
oiio_cmd.append(f'--pattern constant:color={MAP_COLOR2} "{{TOP.width+2*1}}x{{TOP.height+2*1}}" "{{TOP.nchannels}}" --paste "+1+1" ')
oiio_cmd.append(f'--ch R,G,B -o:type={EXR_TYPE} {DEST_DIR}/ground.ACEScg.exr')
Popen(' '.join(oiio_cmd), shell=True).wait()

# Clean-up the temporary part images
for x in range(0,26):
    try:
        os.remove(f'{DEST_DIR}/part_{x}.exr')
    except:
        pass

print("done.")


#
# Generate SSS Bars Map
#

print("Generating SSS Bars Map...", end='', flush=True)

oiio_cmd = [f'{OIIOTOOL}']
oiio_cmd.append(f'{SSS_BAR_BASE_MAP}')
oiio_cmd.append(f'--colormap {SSS_MAP_COLOR1},{SSS_MAP_COLOR2}')
oiio_cmd.append(f'--ch R,G,B -o:type={EXR_TYPE} {DEST_DIR}/sss_bars.ACEScg.exr')

Popen(' '.join(oiio_cmd), shell=True).wait()

print("done.")


#
# Convert the SVG-generated Maps to EXR
#

print("Generating Wall and Emitter Maps", end='', flush=True)

for base_map in BASE_MAPS:
    oiio_cmd = [f'{OIIOTOOL}']
    map_png = (CWD / base_map).resolve()
    exr_name = base_map.replace('.png','.exr')[1:]
    oiio_cmd.append(f'-i {map_png}')
    # We don't need to color map the emitter maps
    if not 'emitter' in base_map:
        oiio_cmd.append(f'--colormap {MAP_COLOR1},{MAP_COLOR2}')
        exr_name = base_map.replace('.png','.ACEScg.exr')[1:]
    oiio_cmd.append(f'--ch R,G,B -o:type={EXR_TYPE} {DEST_DIR}/{exr_name}')
    # Status update
    print(".", end='', flush=True)
    Popen(' '.join(oiio_cmd), shell=True).wait()

print("done.")
