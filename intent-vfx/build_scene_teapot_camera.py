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
    # build scene file for camera
    #
    scene_camera_filepath = './teapotScene_camera.usd'
    
    # new stage for scene camera
    #
    frameBegin = 0.0
    frameEnd = 480.0
    stage = stage_begin(scene_camera_filepath, frameBegin, frameEnd)

    # create main camera (mono)
    #
    root_path = Sdf.Path.absoluteRootPath
    cameras_xform = UsdGeom.Xform.Define(stage, root_path.AppendChild("Cameras"))
    main_camera_xform = UsdGeom.Xform.Define(stage, cameras_xform.GetPath().AppendChild("mainCamera"))
    mono_camera = UsdGeom.Camera.Define(stage, main_camera_xform.GetPath().AppendChild("mono"))
    mono_camera.CreateFocalLengthAttr().Set(32.0)
    mono_camera.CreateClippingRangeAttr().Set((0.1,100000.0))
    
    # turntable movement spiraling to the center
    #

    ccenter = Gf.Vec3d(0,0,0)
    distance = 25.0
    elevation = 10.0

    translateOp = main_camera_xform.AddTranslateOp( opSuffix="zoomedIn" )
    rotateYOp = main_camera_xform.AddRotateYOp( opSuffix="zoomedIn" )
    rotateXOp = main_camera_xform.AddRotateXOp( opSuffix="zoomedIn" )

    angle = 90.0
    for frame in range(int(frameEnd)):
        new_distance = 2.0 + distance - frame*distance/frameEnd
        new_elevation = 5.0 + elevation - frame*elevation/frameEnd
        new_angle = frame*angle/frameEnd
        y_pos = math.sin(Gf.DegreesToRadians( new_elevation ))*new_distance
        y_pos_cos = math.cos(Gf.DegreesToRadians( new_elevation ))
        x_pos = (math.sin(Gf.DegreesToRadians( new_angle ))*new_distance)*y_pos_cos
        z_pos = (math.cos(Gf.DegreesToRadians( new_angle ))*new_distance)*y_pos_cos
        translateOp.Set( ccenter + Gf.Vec3d(x_pos, y_pos, z_pos), frame )        
        rotateYOp.Set( new_angle, frame )
        rotateXOp.Set( -new_elevation, frame )

    # set default prim and close the stage
    #
    stage.SetDefaultPrim(cameras_xform.GetPrim())
    stage_end(stage)


if __name__ == '__main__':
    main()