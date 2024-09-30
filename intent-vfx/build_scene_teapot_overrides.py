import os
import sys
import math
import random
from pxr import Sdf, Usd, UsdGeom, Gf, Vt
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

def rotate2orientation( rotate ):
    rotx = Gf.Rotation(Gf.Vec3d(1,0,0),rotate[0])
    roty = Gf.Rotation(Gf.Vec3d(0,1,0),rotate[1])
    rotz = Gf.Rotation(Gf.Vec3d(0,0,1),rotate[2])
    composedRotate = rotx * roty * rotz
    orientation = Gf.Quath(composedRotate.GetQuaternion().GetReal(),*composedRotate.GetQuaternion().GetImaginary())
    return orientation

def main():
    # build scene file for overrides
    #
    original_scene = './teapotScene.usd'
    scene_with_overrides = './teapotSceneWithOverrides.usd'
    
    # new stage for scene with overrides
    #
    stage = stage_begin(scene_with_overrides)

    # add original scene as sublayer
    #
    stage.GetRootLayer().subLayerPaths.append( original_scene )
    
    root_path = Sdf.Path.absoluteRootPath
    root_scene_path = root_path.AppendChild("Scene")
    root_over = stage.OverridePrim(root_scene_path)
    
    red_teapot_class = stage.CreateClassPrim("/_red_teapot")
    red_teapot_over = stage.OverridePrim("/_red_teapot/mtl/default_material/default_shader_mtlx")
    red_teapot_over.CreateAttribute("inputs:base_color", Sdf.ValueTypeNames.Color3f).Set((1.0,0.0,0.0))

    green_teapot_class = stage.CreateClassPrim("/_green_teapot")
    green_teapot_over = stage.OverridePrim("/_green_teapot/mtl/default_material/default_shader_mtlx")
    green_teapot_over.CreateAttribute("inputs:base_color", Sdf.ValueTypeNames.Color3f).Set((0.0,1.0,0.0))

    blue_teapot_class = stage.CreateClassPrim("/_blue_teapot")
    blue_teapot_over = stage.OverridePrim("/_blue_teapot/mtl/default_material/default_shader_mtlx")
    blue_teapot_over.CreateAttribute("inputs:base_color", Sdf.ValueTypeNames.Color3f).Set((0.0,0.0,1.0))

    overrides = [
        None,
        red_teapot_class,
        green_teapot_class,
        blue_teapot_class
    ]

    random.seed(123)
    
    for p in stage.Traverse():
        if p.IsInstanceable():
            override = overrides[int(random.random()*4)]
            if override:
                p.GetInherits().AddInherit(override.GetPath())

    # set default prim and close the stage
    stage.SetDefaultPrim(root_over)
    stage_end(stage)


if __name__ == '__main__':
    main()