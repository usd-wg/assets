#!/usr/bin/env python3

from pxr import Usd, UsdGeom, UsdLux, Gf
from collections import namedtuple
from camera.cameraGenerator import create_camera_for_card

BoundingBox = namedtuple('BoundingBox', ['width', 'height'])
RENDER_PURPOSE_MAP = {
    "default": UsdGeom.Tokens.default_,
    "render": UsdGeom.Tokens.render,
    "proxy": UsdGeom.Tokens.proxy,
    "guide": UsdGeom.Tokens.guide
}

def setup_cameras(subject_stage, usd_file, cards, dome_light, render_purposes):
    camera_stage = create_camera_stage()
    create_cameras(camera_stage, subject_stage, cards, render_purposes)
    sublayer_subject(camera_stage, usd_file)

    if dome_light:
        add_domelight(camera_stage, dome_light)
    
    camera_stage.Save()

def create_camera_stage():
    stage = Usd.Stage.CreateNew('cameras.usda')
    stage.SetMetadata('metersPerUnit', 0.01)

    return stage

def create_cameras(camera_stage, subject_stage, cards, render_purposes):
    render_purpose_tokens = convert_render_purposes_to_tokens(render_purposes)
    stage_bounding_box = get_bounding_box(subject_stage, render_purpose_tokens)
    min_bound = stage_bounding_box.GetMin()
    max_bound = stage_bounding_box.GetMax()
    subject_center = (min_bound + max_bound) / 2.0

    for card in cards:
        card_width = (max_bound[card.horizontalIndex] - min_bound[card.horizontalIndex]) * 10
        card_height = (max_bound[card.verticalIndex] - min_bound[card.verticalIndex]) * 10
        card_bounding_box = BoundingBox(card_width, card_height)
        
        faceTranslationValue = max_bound[card.translationIndex] if card.sign > 0 else min_bound[card.translationIndex]
        center_of_card_face = Gf.Vec3d(subject_center[0], subject_center[1], subject_center[2])
        center_of_card_face[card.translationIndex] = faceTranslationValue

        camera_view_axis_distance = card_height = (max_bound[card.translationIndex] - min_bound[card.translationIndex])

        create_camera_for_card(card, camera_stage, center_of_card_face, card_bounding_box, camera_view_axis_distance)

def convert_render_purposes_to_tokens(render_purposes):
    return [RENDER_PURPOSE_MAP[key] for key in render_purposes.split(',')]

def get_bounding_box(subject_stage, render_purpose_tokens):
    bboxCache = UsdGeom.BBoxCache(Usd.TimeCode(0.0), render_purpose_tokens)
    root = subject_stage.GetPseudoRoot()
    return bboxCache.ComputeWorldBound(root).GetBox()


def sublayer_subject(camera_stage, input_file):
    camera_stage.GetRootLayer().subLayerPaths = [input_file]

def add_domelight(camera_stage, dome_light):
    UsdLux.DomeLight.Define(camera_stage, '/CardGenerator/DomeLight')
    domeLight = UsdLux.DomeLight(camera_stage.GetPrimAtPath('/CardGenerator/DomeLight'))
    domeLight.CreateTextureFileAttr().Set(dome_light)
    domeLight.CreateTextureFormatAttr().Set("latlong")