#!/usr/bin/env python3

from pxr import Usd, UsdGeom, UsdMedia, Sdf, Gf, UsdUtils, UsdLux
import subprocess
import math
import os
import sys
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="This script takes a thumbnail image of the given USD file supplied and associates it with the file.")
    parser.add_argument('usd_file', 
                        type=str, 
                        help='The USD file you want to add a thumbnail to. If USDZ is input, a new USD file will be created to wrap the existing one called <input>_Thumbnail.usd')
    parser.add_argument('--dome-light',
                        type=str,
                        help='The path to the dome light HDR image to use, if any')
    parser.add_argument('--create-usdz-result', 
                        action='store_true',
                        help='Returns the resulting files as a new usdz file called <input>_Thumbnail.usdz')
    parser.add_argument('--width',
                        type=int,
                        help='The width of the image to generate. Default is 2048.',
                        default=2048)
    parser.add_argument('--height',
                        type=int,
                        help='The height of the image to generate. Default is 2048. If height is not specified, the image is square.')
    parser.add_argument('--output-extension', 
                        type=str, 
                        help='The file extension of the output image you want (exr, png..). If using exr, make sure your usd install includes OpenEXR',
                        default='png')
    parser.add_argument('--verbose', 
                        action='store_true',
                        help='Prints out the steps as they happen')
    parser.add_argument('--apply-thumbnail', 
                        action='store_true',
                        help='Saves the image as the thumbnail for the given USD file.')
    return parser.parse_args()

THUMBNAIL_LAYER_SUFFIX = "_Thumbnail.usda"
DEFAULT_THUMBNAIL_FILENAME = "default_thumbnail.usda"
THUMBNAIL_FOLDER_NAME = "renders"

def generate_thumbnail(usd_file, verbose, extension):
    if verbose: 
        print("Step 1: Setting up the camera...")
    
    subject_stage = Usd.Stage.Open(usd_file)
    subject_file = usd_file

    setup_camera(subject_stage, subject_file, UsdGeom.GetStageUpAxis(subject_stage) == 'Z')
    
    if verbose:
        print("Step 2: Taking the snapshot...")
    
    Path(THUMBNAIL_FOLDER_NAME).mkdir(parents=True, exist_ok=True)

    image_path = os.path.join(THUMBNAIL_FOLDER_NAME, create_image_filename(usd_file, extension)).replace("\\", "/")
    image_name = take_snapshot(image_path)

    return image_name


def setup_camera(subject_stage, usd_file, is_z_up):
    camera_stage = create_camera(UsdGeom.GetStageUpAxis(subject_stage))
    move_camera(camera_stage, subject_stage, is_z_up)

    # check if string is not empty
    if args.dome_light:
        add_domelight(camera_stage, is_z_up)

    sublayer_subject(camera_stage, usd_file)

def create_camera(up_axis):
    stage = Usd.Stage.CreateNew(DEFAULT_THUMBNAIL_FILENAME)

    # Set metadata on the stage.
    stage.SetDefaultPrim(stage.DefinePrim('/ThumbnailGenerator', 'Xform'))
    stage.SetMetadata('metersPerUnit', 0.01)

    UsdGeom.SetStageUpAxis(stage, up_axis) 

    # Define the "MainCamera" under the "ThumbnailGenerator".
    camera = UsdGeom.Camera.Define(stage, '/ThumbnailGenerator/MainCamera')

    # Set the camera attributes.
    camera.CreateFocusDistanceAttr(168.60936)
    camera.CreateFStopAttr(0)
    camera.CreateHorizontalApertureAttr(24)
    camera.CreateHorizontalApertureOffsetAttr(0)
    camera.CreateProjectionAttr("perspective")
    camera.CreateVerticalApertureAttr(24)
    camera.CreateVerticalApertureOffsetAttr(0)
    
    if args.height:
        camera.CreateHorizontalApertureAttr(24 * args.width / args.height)

    return stage

def move_camera(camera_stage, subject_stage, is_z_up):
    camera_prim = UsdGeom.Camera.Get(camera_stage, '/ThumbnailGenerator/MainCamera')
    camera_translation = create_camera_translation_and_clipping(subject_stage, camera_prim, is_z_up)
    apply_camera_transforms(camera_stage, camera_prim, camera_translation, is_z_up)

def add_domelight(camera_stage, is_z_up):
    UsdLux.DomeLight.Define(camera_stage, '/ThumbnailGenerator/DomeLight')
    domeLight = UsdLux.DomeLight(camera_stage.GetPrimAtPath('/ThumbnailGenerator/DomeLight'))
    domeLight.CreateTextureFileAttr().Set(args.dome_light)
    domeLight.CreateTextureFormatAttr().Set("latlong")

    if (is_z_up):
        xformRoot = UsdGeom.Xformable(domeLight.GetPrim())
        xformRoot.AddRotateXOp().Set(90)

def create_camera_translation_and_clipping(subject_stage, camera_prim, is_z_up):
    bounding_box = get_bounding_box(subject_stage)
    min_bound = bounding_box.GetMin()
    max_bound = bounding_box.GetMax()

    subject_center = (min_bound + max_bound) / 2.0
    
    center_of_thumbnail_face = Gf.Vec3d(subject_center[0], min_bound[1], subject_center[2]) if is_z_up else Gf.Vec3d(subject_center[0], subject_center[1], max_bound[2])

    # Conversion from mm to cm
    distance = get_distance_to_camera(min_bound, max_bound, camera_prim, is_z_up)
    distanceInCm = distance / 10.0
    
    cameraPosition = center_of_thumbnail_face + get_camera_translation(distanceInCm, is_z_up)

    clipIndex = 1 if is_z_up else 2

    if args.verbose:
        print("Calculating clipping planes... " + str(clippingPlanes))

    # We're extending the clipping planes in both directions to accommodate for different fields of view
    nearClip = (distanceInCm + min_bound[clipIndex]) * 0.5
    farClip = (distanceInCm + max_bound[clipIndex]) * 2
    nearClip = max(nearClip, 0.0000001)
    clippingPlanes = Gf.Vec2f(nearClip, farClip)
    camera_prim.GetClippingRangeAttr().Set(clippingPlanes)

    return cameraPosition

def get_bounding_box(subject_stage):
    bboxCache = UsdGeom.BBoxCache(Usd.TimeCode(0.0), [UsdGeom.Tokens.default_])
    # Compute the bounding box for all geometry under the root
    root = subject_stage.GetPseudoRoot()
    return bboxCache.ComputeWorldBound(root).GetBox()

def get_distance_to_camera(min_bound, max_bound, camera_prim, is_z_up):
    focal_length = camera_prim.GetFocalLengthAttr().Get()
    horizontal_aperture = camera_prim.GetHorizontalApertureAttr().Get()
    vertical_aperture = camera_prim.GetVerticalApertureAttr().Get()

    verticalIndex = 2 if is_z_up else 1

    distance_to_capture_horizontal = calculate_field_of_view_distance(horizontal_aperture, (max_bound[0] - min_bound[0]) * 10, focal_length)
    distance_to_capture_vertical = calculate_field_of_view_distance(vertical_aperture, (max_bound[verticalIndex] - min_bound[verticalIndex]) * 10, focal_length)

    return max(distance_to_capture_horizontal, distance_to_capture_vertical)

def calculate_field_of_view_distance(sensor_size, object_size, focal_length):
    return calculate_camera_distance(object_size, calculate_field_of_view(focal_length, sensor_size))
    
def calculate_field_of_view(focal_length, sensor_size):
    # Focal length and sensor size should be in the same units (e.g., mm)
    field_of_view = 2 * math.atan(sensor_size / (2 * focal_length))
    return field_of_view

def calculate_camera_distance(subject_size, field_of_view):
    # Subject size and field of view should be in the same units (e.g., mm and degrees)
    distance = (subject_size / 2) / math.tan(field_of_view / 2)
    return distance

def get_camera_translation(distance, is_z_up):
    return Gf.Vec3d(0, -distance, 0) if is_z_up else Gf.Vec3d(0, 0, distance)

def apply_camera_transforms(camera_stage, camera_prim, camera_translation, is_z_up):
    xformRoot = UsdGeom.Xformable(camera_prim.GetPrim())
    translateOp = None
    # Go through each operation in the xformable schema
    for op in xformRoot.GetOrderedXformOps():
        # If the operation is a translate operation, we've found our operation
        if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
            translateOp = op
            break

    # If no translate operation exists, create one
    if translateOp is None:
        translateOp = xformRoot.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble)

    if (is_z_up):
        xformRoot.AddRotateXOp().Set(90)

    translateOp.Set(camera_translation)
    camera_stage.Save()

def sublayer_subject(camera_stage, input_file):
    camera_stage.GetRootLayer().subLayerPaths = [input_file]
    camera_stage.GetRootLayer().Save()

def take_snapshot(image_name):
    renderer = get_renderer()
    cmd = ['usdrecord', '--camera', 'MainCamera', '--imageWidth', str(args.width), '--renderer', renderer, DEFAULT_THUMBNAIL_FILENAME, image_name]
    run_os_specific_usdrecord(cmd)
    os.remove(DEFAULT_THUMBNAIL_FILENAME)
    return image_name

def get_renderer():
    if os.name == 'nt':
        print("windows default renderer GL being used...")
        return "GL"
    else:
        if sys.platform == 'darwin':
            print("macOS default renderer Metal being used...")
            return 'Metal'
        else:
            print("linux default renderer GL being used...")
            return 'GL'

def run_os_specific_usdrecord(cmd):
    if os.name == 'nt':
        subprocess.run(cmd, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        if sys.platform == 'darwin':
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def create_image_filename(input_path, extension):
    return Path(input_path).with_suffix("." + extension)

def link_image_to_subject(subject_stage, image_name):
    subject_root_prim = subject_stage.GetDefaultPrim()
    mediaAPI = UsdMedia.AssetPreviewsAPI.Apply(subject_root_prim)
    thumbnails = UsdMedia.AssetPreviewsAPI.Thumbnails(defaultImage = Sdf.AssetPath(image_name))
    mediaAPI.SetDefaultThumbnails(thumbnails)
    subject_stage.GetRootLayer().Save()
    
def create_usdz_wrapper_stage(usdz_file):
    file_name = usdz_file.split('.')[0]
    existing_stage = Usd.Stage.Open(usd_file)
    new_stage = Usd.Stage.CreateNew(file_name + THUMBNAIL_LAYER_SUFFIX)
    
    UsdUtils.CopyLayerMetadata(existing_stage.GetRootLayer(), new_stage.GetRootLayer())

    new_stage.GetRootLayer().subLayerPaths = [usdz_file]
    new_stage.GetRootLayer().Save()
    return new_stage

def zip_results(usd_file, image_name, is_usdz):
    file_list = [usd_file, image_name]
    usdPath = Path(usd_file)

    if is_usdz:
        file_list.append(usdPath.with_suffix(THUMBNAIL_LAYER_SUFFIX))
        
    usdz_file = usdPath.with_suffix('_Thumbnail.usdz')
    cmd = ["usdzip", "-r", usdz_file] + file_list
    subprocess.run(cmd)

if __name__ == "__main__":

    args = parse_args()

    usd_file = args.usd_file
    is_usdz = ".usdz" in usd_file
        
    image_name = generate_thumbnail(usd_file, args.verbose, args.output_extension)
    subject_stage = create_usdz_wrapper_stage(usd_file) if is_usdz else Usd.Stage.Open(usd_file)

    if args.apply_thumbnail:
        if args.verbose:
            print("Step 3: Linking thumbnail to subject...")
        link_image_to_subject(subject_stage, image_name)

    if args.create_usdz_result:
        if args.verbose:
            print("Step 4: Creating usdz result...")
        
        zip_results(usd_file, image_name, is_usdz)