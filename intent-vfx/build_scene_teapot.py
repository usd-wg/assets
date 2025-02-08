import os
import sys
import math
import random
from pxr import Sdf, Usd, UsdGeom, Gf, UsdShade
import numpy

def stage_begin(i_filename):
    layer = Sdf.Layer.CreateNew( i_filename, args={'format':'usda'} )
    o_stage = Usd.Stage.Open( layer )
    o_stage.SetStartTimeCode(1.0)
    o_stage.SetEndTimeCode(1.0)
    o_stage.SetMetadata("metersPerUnit", 1.0 )
    o_stage.SetMetadata("upAxis", "Y")
    return o_stage

def stage_end(i_stage):
    i_stage.GetRootLayer().Save()

def main():
    # build scene file with all sublayers
    #
    scene = './teapotScene.usd'
    stage = stage_begin(scene)

    # sublayers in proper order
    sublayers = [
        './teapotScene_animCycle.usd',
        './teapotScene_layoutOverrides.usd',
        './teapotScene_camera.usd',
        './teapotScene_layout.usd',
    ]
    for layer in sublayers:
        stage.GetRootLayer().subLayerPaths.append( layer )

    root_path = Sdf.Path.absoluteRootPath
    root_scene_path = root_path.AppendChild("Scene")
    root_over = stage.OverridePrim(root_scene_path)
    stage.SetDefaultPrim(root_over)

    # close the stage
    stage_end(stage)


if __name__ == '__main__':
    main()