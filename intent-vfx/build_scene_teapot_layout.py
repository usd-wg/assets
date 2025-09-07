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
    # main details for current asset
    #
    asset_name = "teapot"
    root_path = Sdf.Path.absoluteRootPath
    root_scene_path = root_path.AppendChild("Scene")

    # build scene file
    #
    asset_filename = "../assets/{}/{}.usd".format(asset_name,asset_name)
    scene_filename = './{}Scene_layout.usd'.format(asset_name)
    # create stage for geometry
    stage = stage_begin(scene_filename)
    # build root
    root = UsdGeom.Scope.Define(stage, root_scene_path)
    # create classes prim
    classes = stage.CreateClassPrim(root_path.AppendChild("_class_"))
    # create simpleAsset class
    simpleAsset_class = stage.CreateClassPrim(classes.GetPath().AppendChild(asset_name))

    # create elements in rings-shaped layout
    ring_radius = 0.7
    ring_radius_inc = 0.4
    ring_angle = 0.0
    angle_step = 0.6
    num_of_assets = 1000
    ring = 0
    make_instancer = False
    instancer = None
    for ei in range(num_of_assets):
        hierarchy_point = "ring{:0>3}".format(ring)
        hierarchy_path = root.GetPath().AppendChild(hierarchy_point)
        if not stage.GetPrimAtPath(hierarchy_path):
            UsdGeom.Scope.Define(stage, hierarchy_path)
        uscale = 0.7+random.random()*0.6
        pos = (math.cos(ring_angle)*ring_radius, 0.0, math.sin(ring_angle)*ring_radius)
        scale = (uscale,uscale,uscale)
        rot = random.random()*360.0
        if make_instancer:
            element_name = "instancer_{}{:0>3}".format(asset_name, ring)
            element_path = hierarchy_path.AppendChild(element_name)
            if not stage.GetPrimAtPath(element_path):
                instancer = UsdGeom.PointInstancer.Define(stage, element_path)
                prototype = UsdGeom.Xform.Define( stage, instancer.GetPath().AppendChild('Prototypes').AppendChild(asset_name) )
                instancer.GetPrototypesRel().AddTarget( prototype.GetPath() )
                prototype.GetPrim().SetInstanceable(True)
                prototype.GetPrim().GetInherits().AddInherit( simpleAsset_class.GetPath() )
                prototype.GetPrim().GetReferences().AddReference( asset_filename )
            positions = list(instancer.GetPositionsAttr().Get()) if instancer.GetPositionsAttr().Get() else []
            rotations = list(instancer.GetOrientationsAttr().Get()) if instancer.GetOrientationsAttr().Get() else []
            scales = list(instancer.GetScalesAttr().Get()) if instancer.GetScalesAttr().Get() else []
            protos = list(instancer.GetProtoIndicesAttr().Get()) if instancer.GetProtoIndicesAttr().Get() else []
            positions.append(pos)
            rotations.append(rotate2orientation((0,rot,0)))
            scales.append(scale)
            protos.append(0)
            instancer.GetPositionsAttr().Set(positions)
            instancer.GetOrientationsAttr().Set(rotations)
            instancer.GetScalesAttr().Set(scales)
            instancer.GetProtoIndicesAttr().Set(protos)
        else:
            element_name = "{}{:0>3}".format(asset_name, ei)
            element_path = hierarchy_path.AppendChild(element_name)
            element = UsdGeom.Xform.Define(stage,element_path)
            element.GetPrim().SetInstanceable(True)
            element.GetPrim().GetInherits().AddInherit( simpleAsset_class.GetPath() )
            element.GetPrim().GetReferences().AddReference( asset_filename )
            element.AddTranslateOp().Set(pos)
            element.AddRotateYOp().Set(rot)
            element.AddScaleOp().Set(scale)
        jitter_step = (random.random()*0.5)*angle_step
        ring_angle += angle_step*uscale-jitter_step
        if ring_angle > 2.0*math.pi:
            ring += 1
            ring_angle -= 2.0*math.pi
            ring_radius += ring_radius_inc
            angle_step *= 0.98
            make_instancer = True if random.random()>0.5 else False
        
    # set default prim and close the stage
    stage.SetDefaultPrim(root.GetPrim())
    stage_end(stage)


if __name__ == '__main__':
    main()