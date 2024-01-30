#!/usr/bin/env python3

from pxr import Usd, UsdGeom, UsdUtils

from collections import namedtuple
from camera.cameraManager import setup_cameras
from camera.renderManger import run_os_specific_command, take_snapshots
from utils.arg_parser import parse_args
from pathlib import Path
import os

Card = namedtuple('Card', ['name', 'horizontalIndex', 'verticalIndex', 'sign', 'rotations', 'translationIndex', 'parentPath', 'usdFileName'])
Rotation = namedtuple('Rotation', ['index', 'amount'])

cards = [
    Card('XPos', 2, 1, 1, [Rotation(0, 90), Rotation(1, 90)], 0, None, None),
    Card('XNeg', 2, 1, -1, [Rotation(0, 90), Rotation(1, 270)], 0, None, None),
    Card('YPos', 2, 0, 1, [Rotation(1, 180), Rotation(0, 270)], 1, None, None),
    Card('YNeg', 2, 0, -1, [Rotation(0, 90)], 1, None, None),
    Card('ZPos', 0, 1, 1, [], 2, None, None),
    Card('ZNeg', 0, 1, -1, [Rotation(2, 180), Rotation(1, 180)], 2, None, None)
]

CARDS_LAYER_SUFFIX_USDA = "_Cards.usda"
CARDS_LAYER_SUFFIX = "_Cards"
EXTENSIONS = ('.usd', '.usda', '.usdc', '.usdz')

def generate_card_images(usd_file, subject_stage, dome_light, output_extension, verbose, apply_cards, render_purposes, image_width):

    if apply_cards:
        if verbose: 
            print("Step 1: Applying cards default values...")
        apply_cards_defaults(subject_stage)

    if verbose: 
        print("Step 2: Setting up the cameras...")

    setup_cameras(subject_stage, usd_file, cards, dome_light, render_purposes)
    
    if verbose:
        print("Step 3: Taking the snapshots...")

    usd_file_path = Path(usd_file)

    for i, card in enumerate(cards):
        cards[i] = card._replace(parentPath=usd_file_path.parent, usdFileName=usd_file_path.stem)

    image_names = take_snapshots(cards, output_extension, image_width)

    return image_names

def apply_cards_defaults(subject_stage):
    subject_root_prim = subject_stage.GetDefaultPrim()
    subject_root_prim.SetMetadata("kind", "component")
    UsdGeom.ModelAPI.Apply(subject_root_prim)
    geom_model_api = UsdGeom.ModelAPI(subject_root_prim)
    geom_model_api.CreateModelApplyDrawModeAttr(False)
    geom_model_api.CreateModelCardGeometryAttr("box")
    geom_model_api.CreateModelDrawModeAttr("cards")
    geom_model_api.CreateModelDrawModeColorAttr((1, 0, 0))

def link_images_to_subject(subject_stage, images):
    subject_root_prim = subject_stage.GetDefaultPrim()
    
    geom_model_api = UsdGeom.ModelAPI(subject_root_prim)
    geom_model_api.CreateModelCardTextureXPosAttr(images[0])
    geom_model_api.CreateModelCardTextureXNegAttr(images[1])
    geom_model_api.CreateModelCardTextureYPosAttr(images[2])
    geom_model_api.CreateModelCardTextureYNegAttr(images[3])
    geom_model_api.CreateModelCardTextureZPosAttr(images[4])
    geom_model_api.CreateModelCardTextureZNegAttr(images[5])
    geom_model_api.CreateModelApplyDrawModeAttr(True)
    
def create_usdz_wrapper_stage(usdz_file, usdz_wrapper_name):
    existing_stage = Usd.Stage.Open(usdz_file)
    new_stage = Usd.Stage.CreateNew(usdz_wrapper_name)
    
    UsdUtils.CopyLayerMetadata(existing_stage.GetRootLayer(), new_stage.GetRootLayer())

    new_stage.GetRootLayer().subLayerPaths = [usdz_file]
    
    return new_stage

def zip_results(usd_file, images, is_usdz):
    file_list = [usd_file] + images

    usdPath = Path(usd_file)

    if is_usdz:
        file_list.append(usd_file.replace(usdPath.suffix, CARDS_LAYER_SUFFIX_USDA))
        
    usdz_file = usd_file.replace(usdPath.suffix, CARDS_LAYER_SUFFIX)
    cmd = ["usdzip", "-r", usdz_file] + file_list
    run_os_specific_command(cmd)

def generate_cards_for_single_asset(usd_file, args):
    usdz_wrapper_name = usd_file.split('.')[0] + CARDS_LAYER_SUFFIX_USDA
    is_usdz = ".usdz" in usd_file
    subject_stage = create_usdz_wrapper_stage(usd_file, usdz_wrapper_name) if is_usdz and args.apply_cards else Usd.Stage.Open(usd_file)
    file_to_sublayer = usdz_wrapper_name if is_usdz and args.apply_cards else usd_file

    images = generate_card_images(file_to_sublayer, subject_stage, args.dome_light, args.output_extension, args.verbose, args.apply_cards, args.render_purposes, args.image_width)

    if args.apply_cards:
        if args.verbose:
            print("Step 4: Linking cards to subject...")
        stripped_image_paths = [image.replace(str(Path(usd_file).parent), "").lstrip('/') for image in images]
        link_images_to_subject(subject_stage, stripped_image_paths)

    if args.create_usdz_result:
        if args.verbose:
            print("Step 5: Zipping cards as usdz...")
        
        zip_results(args.usd_file, images, args.is_usdz)

    subject_stage.GetRootLayer().Save()

if __name__ == "__main__":
    args = parse_args()

    if args.directory and args.recursive:
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                if file.endswith(EXTENSIONS):
                    file_path = os.path.join(root, file)
                    if args.verbose:
                        print(f"Processing {file_path}...")
                    try: 
                        generate_cards_for_single_asset(file_path, args)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
    elif args.directory:
        for file in os.listdir(args.directory):
            if file.endswith(EXTENSIONS):
                file_path = os.path.join(args.directory, file)
                if args.verbose:
                    print(f"Processing {file_path}...")
                try: 
                    generate_cards_for_single_asset(file_path, args)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    elif args.usd_file:
        usd_file = args.usd_file
        generate_cards_for_single_asset(usd_file, args)
    else:
        print("Either --usd-file or --directory must be set.")