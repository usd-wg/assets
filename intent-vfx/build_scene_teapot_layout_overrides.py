import os
import sys
import math
import random
from pxr import Sdf, Usd, UsdGeom, Gf, UsdShade
import numpy

def add_readcolorprimvar_shader(i_stage,i_material,i_varname):
    prim_path = i_material.GetPath().AppendChild("generic_primvar_reader_{}".format(i_varname))
    prim = UsdShade.Shader.Define( i_stage, prim_path )
    prim.CreateIdAttr("ND_UsdPrimvarReader_vector3")
    prim.CreateInput( "varname", Sdf.ValueTypeNames.Token ).Set( i_varname )
    result_output = None
    prim.CreateInput( "fallback", Sdf.ValueTypeNames.Color3f ).Set( (0.18,0.18,0.18) )
    result_output = prim.CreateOutput( "out", Sdf.ValueTypeNames.Color3f )
    return result_output


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
    original_scene = './teapotScene_layout.usd'
    scene_with_overrides = './teapotScene_layoutOverrides.usd'
    
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

    rgb_teapot_class = stage.CreateClassPrim("/_rgb_teapot")
    rgb_teapot_material_over = stage.OverridePrim("/_rgb_teapot/mtl/default_material")
    rgb_teapot_shader_over = stage.OverridePrim("/_rgb_teapot/mtl/default_material/default_shader_mtlx")
    readprimvar_custom_color_output = add_readcolorprimvar_shader(stage,rgb_teapot_material_over,"custom_color")
    UsdShade.Shader(rgb_teapot_shader_over).CreateInput( "base_color",Sdf.ValueTypeNames.Color3f ).ConnectToSource( readprimvar_custom_color_output )

    # NOTE: Following 3 overs are for debugging purposes only. 
    #       When looking at the implicit-prototypes in USD you
    #       can't really see where they are coming from.
    #       Which this over, you can see which implicit-proto 
    #       has which over, so you can tell what those protos are.
    #       It's a trick that adds more prims to your stage, 
    #       but good for debugging directly in outliners.
    red_teapot_id = stage.OverridePrim("/_red_teapot/i_am_red_teapot")
    green_teapot_id = stage.OverridePrim("/_green_teapot/i_am_green_teapot")
    blue_teapot_id = stage.OverridePrim("/_blue_teapot/i_am_blue_teapot")
    rgb_teapot_id = stage.OverridePrim("/_rgb_teapot/i_am_rgb_teapot")

    overrides = [
        None,
        red_teapot_class,
        green_teapot_class,
        blue_teapot_class
    ]

    random.seed(123)
    
    for p in stage.Traverse():

        if p.IsInstanceable() and not (p.GetParent() and p.GetParent().GetName() == "Prototypes"):
            override = overrides[int(random.random()*4)]
            if override:
                p.GetInherits().AddInherit(override.GetPath())

        elif p.GetTypeName() == "PointInstancer":
            pi = UsdGeom.PointInstancer(p)
            # two options:
            # 1. new prototypes with material-overrides and overriding protoids
            # 2. per-instance primvars to drive same material
            #    this option require that per-instance primvars are used in the shaders then
            option = random.random()
            if option < 0.5:
                protoIds = pi.GetProtoIndicesAttr().Get()
                for i in range(len(protoIds)):
                    protoIds[i] = int(random.random()*4)
                # NOTE: we know where the prototypes are
                red_prototype = UsdGeom.Xform.Define( stage, p.GetPath().AppendChild("Prototypes").AppendChild("red_teapot") )
                red_prototype.GetPrim().SetInstanceable(True)
                red_prototype.GetPrim().GetInherits().AddInherit( "/_class_/teapot" )
                red_prototype.GetPrim().GetReferences().AddReference( "../assets/teapot/teapot.usd" )                
                green_prototype = UsdGeom.Xform.Define( stage, p.GetPath().AppendChild("Prototypes").AppendChild("green_teapot") )
                green_prototype.GetPrim().SetInstanceable(True)
                green_prototype.GetPrim().GetInherits().AddInherit( "/_class_/teapot" )
                green_prototype.GetPrim().GetReferences().AddReference( "../assets/teapot/teapot.usd" )                
                blue_prototype = UsdGeom.Xform.Define( stage, p.GetPath().AppendChild("Prototypes").AppendChild("blue_teapot") )
                blue_prototype.GetPrim().SetInstanceable(True)
                blue_prototype.GetPrim().GetInherits().AddInherit( "/_class_/teapot" )
                blue_prototype.GetPrim().GetReferences().AddReference( "../assets/teapot/teapot.usd" )                
                pi.GetPrototypesRel().AddTarget( red_prototype.GetPath() )
                pi.GetPrototypesRel().AddTarget( green_prototype.GetPath() )
                pi.GetPrototypesRel().AddTarget( blue_prototype.GetPath() )
                # order of inherits here is important, but only because we are using
                # inheriting from the original prototype, which means, mostly driven by
                # how we are building this scene.
                red_prototype.GetPrim().GetInherits().AddInherit( overrides[1].GetPath() )
                green_prototype.GetPrim().GetInherits().AddInherit( overrides[2].GetPath() )
                blue_prototype.GetPrim().GetInherits().AddInherit( overrides[3].GetPath() )
                pi.GetProtoIndicesAttr().Set(protoIds)
            else:
                # add per-instance primvars for shaders
                instance_count = pi.GetInstanceCount()
                per_instance_colors = numpy.full( (instance_count,3), 0.0 )
                for i in range(instance_count):
                    per_instance_colors[i][0] = random.random()
                    per_instance_colors[i][1] = random.random()
                    per_instance_colors[i][2] = random.random()
                color_attr = p.CreateAttribute("primvars:custom_color", Sdf.ValueTypeNames.Color3fArray )
                color_attr.Set( per_instance_colors )
                UsdGeom.Primvar( color_attr ).SetInterpolation( "vertex" )
                # NOTE: we know where the prototypes are
                orig_prototype = stage.GetPrimAtPath(p.GetPath().AppendChild("Prototypes").AppendChild("teapot"))
                orig_prototype.GetInherits().AddInherit(rgb_teapot_class.GetPath())

    # remove sublayers
    stage.GetRootLayer().subLayerPaths = []

    # set default prim and close the stage
    stage.SetDefaultPrim(root_over)
    stage_end(stage)


if __name__ == '__main__':
    main()