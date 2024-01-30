#!/usr/bin/env python3

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="This script generates cards for a given USD file and associates them with the file.")
    parser.add_argument('--usd-file', 
                        type=str, 
                        help='The USD file you want to add cards to. If USDZ is input, a new USD file will be created to wrap the existing one called <input>_Cards.usd')
    parser.add_argument('--dome-light',
                        type=str,
                        help='The path to the dome light HDR image to use, if any')
    parser.add_argument('--create-usdz-result', 
                        action='store_true',
                        help='Returns the resulting files as a new usdz file called <input>_Cards.usdz')
    parser.add_argument('--output-extension', 
                    type=str, 
                    help='The file extension of the output image you want (exr, png..). If using exr, make sure your usd install includes OpenEXR',
                    default='png')
    parser.add_argument('--verbose', 
                        action='store_true',
                        help='Prints out the steps as they happen')
    parser.add_argument('--apply-cards', 
                        action='store_true',
                        help='Saves the images as the cards for the given USD file.')
    parser.add_argument('--render-purposes', 
                        type=str,
                        help='A comma separated list of render purposes to include in the thumbnail. Valid values are: default, render, proxy, guide.',
                        default='default')
    parser.add_argument('--image-width',
                        type=int,
                        help='The width of the image to generate. Default is 2048.',
                        default=2048)
    parser.add_argument('--directory', 
                        type=str,
                        help='A directory to generate thumbnails for all .usd, .usda, .usdc, and .usdz files. When a directory is supplied, usd-file is ignored.')
    parser.add_argument('--recursive', 
                        action='store_true',
                        help='Will recursively search all directories underneath a given directory, requires a directory to be set.')

    
    return parser.parse_args()
