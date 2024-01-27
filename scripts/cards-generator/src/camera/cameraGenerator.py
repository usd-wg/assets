#!/usr/bin/env python3

from pxr import UsdGeom, Gf
from camera.utils.distanceCalculator import get_distance_to_frame_subject
from camera.globals import APERTURE, FOCAL_LENGTH, FOCUS_DISTANCE

def create_camera_for_card(card, camera_stage, center_of_card_face, bounding_box, camera_view_axis_distance):
    camera_prim = create_camera_with_defaults(camera_stage, card.name)

    distance = get_distance_to_frame_subject(bounding_box, APERTURE, FOCAL_LENGTH)

    nearClip = distance / 10.0
    farClip = (( distance + camera_view_axis_distance ) / 10.0) * 2
    clippingPlanes = Gf.Vec2f(nearClip, farClip)
    camera_prim.GetClippingRangeAttr().Set(clippingPlanes)

    position_camera(camera_prim, card, center_of_card_face, distance)

    calculate_apertures(camera_prim, bounding_box, distance, card)

    rotate_camera(card, camera_prim)

def create_camera_with_defaults(camera_stage, name):
    camera_prim = UsdGeom.Camera.Define(camera_stage, '/CardGenerator/' + name)
    camera_prim.CreateFocalLengthAttr(FOCAL_LENGTH)
    camera_prim.CreateFocusDistanceAttr(FOCUS_DISTANCE)
    camera_prim.CreateFStopAttr(0)
    camera_prim.CreateHorizontalApertureOffsetAttr(0)
    camera_prim.CreateProjectionAttr("perspective")
    camera_prim.CreateVerticalApertureOffsetAttr(0)

    return camera_prim

def position_camera(camera_prim, card, center_of_card_face, distance):
    camera_translation = create_camera_translation(card, center_of_card_face, distance)
    apply_camera_translation(camera_prim, camera_translation)

def create_camera_translation(card, center_of_card_face, distance):
    return center_of_card_face + create_translate_vector(distance * card.sign, card.translationIndex)

def calculate_apertures(camera_prim, bounding_box, distance, card):
    flip_aperatures = False
    for rotation in card.rotations:
        if rotation.amount != 180:
            flip_aperatures = True
            break
    
    actual_horizontal_aperture = FOCAL_LENGTH * bounding_box.width / distance
    actual_vertical_aperture = FOCAL_LENGTH * bounding_box.height / distance

    if flip_aperatures:
        camera_prim.CreateHorizontalApertureAttr(actual_vertical_aperture)
        camera_prim.CreateVerticalApertureAttr(actual_horizontal_aperture)
    else:
        camera_prim.CreateHorizontalApertureAttr(actual_horizontal_aperture)
        camera_prim.CreateVerticalApertureAttr(actual_vertical_aperture)

def rotate_camera(card, camera_prim):
    for rotation in card.rotations:
        apply_camera_rotation(camera_prim, rotation.index, rotation.amount)

def create_translate_vector(distance, translationIndex):
    vector = Gf.Vec3d(0, 0, 0)
    vector[translationIndex] = distance / 10.0 # convert units from mm to cm
    return vector

def apply_camera_translation(camera_prim, camera_translation):
    xformRoot = UsdGeom.Xformable(camera_prim.GetPrim())
    translateOp = xformRoot.AddTranslateOp(UsdGeom.XformOp.PrecisionDouble)
    translateOp.Set(camera_translation)

def apply_camera_rotation(camera_prim, rotationDirection, rotationAmount):
    xformRoot = UsdGeom.Xformable(camera_prim.GetPrim())
    if rotationDirection == 0:
        rotateOp = xformRoot.AddRotateXOp()
        rotateOp.Set(rotationAmount)
    elif rotationDirection == 1:
        rotateOp = xformRoot.AddRotateYOp()
        rotateOp.Set(rotationAmount)
    else:
        rotateOp = xformRoot.AddRotateZOp()
        rotateOp.Set(rotationAmount)