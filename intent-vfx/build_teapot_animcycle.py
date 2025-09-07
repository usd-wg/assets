import os
import sys
import math
import random
from pxr import Sdf, Usd, UsdGeom, Gf, UsdShade
import numpy

def stage_begin(i_filename, i_start=1.0, i_end=1.0):
    layer = Sdf.Layer.CreateNew( i_filename, args={'format':'usda'} )
    o_stage = Usd.Stage.Open( layer )
    o_stage.SetStartTimeCode(i_start)
    o_stage.SetEndTimeCode(i_end)
    o_stage.SetMetadata("metersPerUnit", 1.0 )
    o_stage.SetMetadata("upAxis", "Y")
    return o_stage

def stage_end(i_stage):
    i_stage.GetRootLayer().Save()

def main():
    # build scene file for overrides
    #
    original_scene = './teapot.usd'
    scene_with_overrides = './teapot_animCycle.usd'
    
    startTime = 0.0
    endTime = 48.0
    cycles = 10

    # new stage for scene with overrides
    #
    stage = stage_begin(scene_with_overrides, startTime, endTime)

    root_path = Sdf.Path.absoluteRootPath
    root_scene_path = root_path.AppendChild("teapot")
    root_over = stage.OverridePrim(root_scene_path)

    # add original scene as sublayer
    #
    stage.GetRootLayer().subLayerPaths.append( original_scene )
    
    over_prim = stage.OverridePrim("/teapot/geo/default/Body")
    over_points_attr = over_prim.GetAttribute("points")

    for f in range(int(endTime)*cycles):
        frame = f % int(endTime)
        c = math.cos(Gf.DegreesToRadians( 90.0 + (frame/endTime)*720.0 ))
        s = math.sin(Gf.DegreesToRadians( (frame/endTime)*360.0 )) * 2.0
        over_points = over_points_attr.Get()
        for i in range(len(over_points)):
            p = over_points[i]
            x_offset = s * p[1] * p[1]
            y_offset = c * p[1] * p[1]
            over_points[i] = Gf.Vec3f(p[0]+x_offset, p[1]+y_offset, p[2])
        over_points_attr.Set(over_points, f)

    # remove sublayers
    stage.GetRootLayer().subLayerPaths = []

    # close the stage
    stage.SetDefaultPrim(root_over)
    stage_end(stage)


if __name__ == '__main__':
    main()