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
    # new stage for scene with overrides
    #
    stage = stage_begin('./teapotScene_animCycle.usd')

    root_path = Sdf.Path.absoluteRootPath
    root_scene_path = root_path.AppendChild("Scene")
    root_over = stage.OverridePrim(root_scene_path)

    # add original scene as sublayer with layoutOverrides too
    #
    stage.GetRootLayer().subLayerPaths.append( './teapotScene_layoutOverrides.usd' )
    stage.GetRootLayer().subLayerPaths.append( './teapotScene_layout.usd' )
    
    # fixed number of offsets will be randomly
    # distributed on the layout elements and instances
    # teapot animation is a cycle of 48 frames (baked for 480 frames)
    # we are going to create 24 variations with 2-frames offset from
    # each other
    #
    anim_offsets = 24
    overrides = []
    for i in range(anim_offsets):
        frame_offset = i*2
        overrides.append( stage.CreateClassPrim("/_teapot_animCycle_offset_{}".format(frame_offset)) )
        stage.OverridePrim(overrides[-1].GetPath().AppendChild("i_am_anim_offset_{}".format(frame_offset)))
        overrides[-1].GetReferences().AddReference(
            assetPath = "../assets/teapot/teapot_animCycle.usd",
            primPath = '/teapot',
            layerOffset = Sdf.LayerOffset(offset=frame_offset))

    random.seed(123)
    
    for p in stage.Traverse():

        if p.IsInstanceable() and not (p.GetParent() and p.GetParent().GetName() == "Prototypes"):
            override = overrides[int(random.random()*len(overrides))]
            p.GetInherits().AddInherit(override.GetPath())

        elif p.GetTypeName() == "PointInstancer":
            # CBB: this should add new protos inheriting from
            #      existing ones so that all protos get an
            #      animated variant to be used in proto-ids
            pi = UsdGeom.PointInstancer(p)
            protos = pi.GetPrototypesRel().GetTargets()
            for proto in protos:
                override = overrides[int(random.random()*len(overrides))]
                proto_prim = stage.GetPrimAtPath(proto)
                proto_prim.GetInherits().AddInherit(override.GetPath())


    # remove sublayers
    stage.GetRootLayer().subLayerPaths = []

    # set default prim and close the stage
    stage.SetDefaultPrim(root_over)
    stage_end(stage)


if __name__ == '__main__':
    main()