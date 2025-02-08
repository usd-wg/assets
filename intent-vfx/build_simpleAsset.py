import os
import sys
import math
import random
from pxr import Sdf, Usd, UsdGeom, UsdShade

random.seed(123)

def stage_begin(i_filename):
    layer = Sdf.Layer.CreateNew( i_filename, args={'format':'usda'} )
    o_stage = Usd.Stage.Open( layer )
    o_stage.SetStartTimeCode(1.0)
    o_stage.SetEndTimeCode(1.0)
    o_stage.SetMetadata("metersPerUnit", 0.01 )
    o_stage.SetMetadata("upAxis", "Y")
    return o_stage

def stage_end(i_stage):
    i_stage.GetRootLayer().Save()

def build_asset_root(i_stage, i_asset_root_path, 
                     i_asset_name="", 
                     i_asset_identifier="", 
                     i_asset_version=""):
    o_asset_root = UsdGeom.Xform.Define(i_stage, i_asset_root_path)
    modelAPI = Usd.ModelAPI(o_asset_root)
    modelAPI.SetKind("component")
    if i_asset_name != "":
        modelAPI.SetAssetName(i_asset_name)
    if i_asset_identifier != "":
        modelAPI.SetAssetIdentifier(i_asset_identifier)
    if i_asset_version != "":
        modelAPI.SetAssetVersion(i_asset_version)
    return o_asset_root

def add_readprimvar_shader(i_stage,i_material,i_varname,i_type):
    prim_path = i_material.GetPath().AppendChild("generic_primvar_reader_{}".format(i_varname))
    prim = UsdShade.Shader.Define( i_stage, prim_path )
    prim.CreateIdAttr("UsdPrimvarReader_{}".format(type))
    prim.CreateInput( "varname", Sdf.ValueTypeNames.Token ).Set( i_varname )
    result_output = None
    if i_type == "float2":
        prim.CreateInput( "fallback", Sdf.ValueTypeNames.Float2 ).Set( (0.0,0.0) )
        result_output = prim.CreateOutput( "result", Sdf.ValueTypeNames.Float2 )
    return result_output

def add_readtexture_shader(i_stage,i_material,i_texname,i_type,i_texture_filename):
    prim_path = i_material.GetPath().AppendChild("generic_texture_{}".format(i_texname))
    prim = UsdShade.Shader.Define( i_stage, prim_path )
    prim.CreateIdAttr("UsdUVTexture")
    prim.CreateInput( "file", Sdf.ValueTypeNames.Asset ).Set( i_texture_filename )
    readprimvar_st_output = add_readprimvar_shader(i_stage,i_material,"st","float2")
    prim.CreateInput( "st",Sdf.ValueTypeNames.Float2 ).ConnectToSource( readprimvar_st_output )
    result_output = None
    if i_type == "color":
        result_output = prim.CreateOutput( "rgb", Sdf.ValueTypeNames.Color3f )
    elif i_type == "float":
        result_output = prim.CreateOutput( "r", Sdf.ValueTypeNames.Float )
    return result_output

def build_preview_shader(i_stage, i_material, i_name):
    o_shader = UsdShade.Shader.Define( i_stage, i_material.GetPath().AppendChild(i_name) )
    o_shader.CreateIdAttr("UsdPreviewSurface")
    diff_random_color = (random.random(),random.random(),random.random())
    channels = [
        ("diffuseColor","color",Sdf.ValueTypeNames.Color3f, diff_random_color,"" ),
        ("specularColor","color",Sdf.ValueTypeNames.Color3f,(1.0,1.0,1.0),""),
        ("roughness","float",Sdf.ValueTypeNames.Float,0.2,""),
        ("clearcoatRoughness","float",Sdf.ValueTypeNames.Float,0.1,"")
    ]

    for channel in channels:
        ch_name = channel[0]
        ch_type = channel[1]
        ch_sdftype = channel[2]
        ch_default = channel[3]
        ch_texture = channel[4]
        ch_input = o_shader.CreateInput(ch_name, ch_sdftype)
        ch_input.Set(ch_default)
        if ch_texture != "":
            ch_texture_output = add_readtexture_shader(i_stage,i_material,ch_name,ch_type,ch_texture)
            ch_input.ConnectToSource( ch_texture_output )

    surfaceOutput = o_shader.CreateOutput("surface",Sdf.ValueTypeNames.Token)
    materialSurfaceOutput = i_material.CreateSurfaceOutput()
    materialSurfaceOutput.ConnectToSource( surfaceOutput )
    return o_shader

def add_mtlx_image(i_stage,i_material,i_texname,i_sdftype,i_texture_filename):
    # https://github.com/AcademySoftwareFoundation/MaterialX/blob/v1.38.10/libraries/stdlib/stdlib_defs.mtlx
    prim_path = i_material.GetPath().AppendChild("mtlx_texture_{}".format(i_texname))
    prim = UsdShade.Shader.Define( i_stage, prim_path )
    prim.CreateIdAttr("ND_image_{}".format( str(i_sdftype).replace("3f","3") ) )
    prim.CreateInput( "file", Sdf.ValueTypeNames.Asset ).Set( i_texture_filename )
    result_output = prim.CreateOutput( "out", i_sdftype )
    return result_output

def build_mtlx_standard_surface(i_stage, i_material, i_name):
    # https://github.com/AcademySoftwareFoundation/MaterialX/blob/v1.38.10/libraries/bxdf/standard_surface.mtlx
    o_shader = UsdShade.Shader.Define( i_stage, i_material.GetPath().AppendChild(i_name) )
    o_shader.CreateIdAttr("ND_standard_surface_surfaceshader")
    diff_random_color = (random.random(),random.random(),random.random())
    channels = [
        ("base",Sdf.ValueTypeNames.Float, 1.0, ""),
        ("base_color",Sdf.ValueTypeNames.Color3f, (0.8,0.8,0.8), ""),
        ("diffuse_roughness",Sdf.ValueTypeNames.Float, 0, ""),

        ("specular",Sdf.ValueTypeNames.Float, 1, ""),
        ("specular_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("specular_roughness",Sdf.ValueTypeNames.Float, 0.2, ""),
        ("specular_IOR",Sdf.ValueTypeNames.Float, 1.5, ""),
        ("specular_anisotropy",Sdf.ValueTypeNames.Float, 0, ""),
        ("specular_rotation",Sdf.ValueTypeNames.Float, 0, ""),

        ("metalness",Sdf.ValueTypeNames.Float, 0, ""),

        ("transmission",Sdf.ValueTypeNames.Float, 0, ""),
        ("transmission_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("transmission_depth",Sdf.ValueTypeNames.Float, 0, ""),
        ("transmission_scatter",Sdf.ValueTypeNames.Color3f, (0,0,0), ""),
        ("transmission_scatter_anisotropy",Sdf.ValueTypeNames.Float, 0, ""),
        ("transmission_dispersion",Sdf.ValueTypeNames.Float, 0, ""),
        ("transmission_extra_roughness",Sdf.ValueTypeNames.Float, 0, ""),

        ("subsurface",Sdf.ValueTypeNames.Float, 0, ""),
        ("subsurface_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("subsurface_radius",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("subsurface_scale",Sdf.ValueTypeNames.Float, 1, ""),
        ("subsurface_anisotropy",Sdf.ValueTypeNames.Float, 0, ""),

        ("sheen",Sdf.ValueTypeNames.Float, 0, ""),
        ("sheen_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("sheen_roughness",Sdf.ValueTypeNames.Float, 0.3, ""),

        ("coat",Sdf.ValueTypeNames.Float, 0, ""),
        ("coat_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),
        ("coat_roughness",Sdf.ValueTypeNames.Float, 0.1, ""),
        ("coat_anisotropy",Sdf.ValueTypeNames.Float, 0, ""),
        ("coat_rotation",Sdf.ValueTypeNames.Float, 0, ""),
        ("coat_IOR",Sdf.ValueTypeNames.Float, 1.5, ""),
        ("coat_affect_color",Sdf.ValueTypeNames.Float, 0, ""),
        ("coat_affect_roughness",Sdf.ValueTypeNames.Float, 0, ""),

        ("thin_film_thickness",Sdf.ValueTypeNames.Float, 0, ""),
        ("thin_film_IOR",Sdf.ValueTypeNames.Float, 1.5, ""),

        ("emission",Sdf.ValueTypeNames.Float, 0, ""),
        ("emission_color",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),

        ("opacity",Sdf.ValueTypeNames.Color3f, (1,1,1), ""),

        ("thin_walled",Sdf.ValueTypeNames.Bool, False, ""),
    ]
    for channel in channels:
        ch_name = channel[0]
        ch_sdftype = channel[1]
        ch_default = channel[2]
        ch_texture = channel[3]
        ch_input = o_shader.CreateInput(ch_name, ch_sdftype)
        ch_input.Set(ch_default)
        if ch_texture != "":
            ch_texture_output = add_mtlx_image(i_stage,i_material,ch_name,ch_sdftype,ch_texture)
            ch_input.ConnectToSource( ch_texture_output )

    surfaceOutput = o_shader.CreateOutput("surface",Sdf.ValueTypeNames.Token)
    materialSurfaceOutput = i_material.CreateSurfaceOutput(renderContext="mtlx")
    materialSurfaceOutput.ConnectToSource( surfaceOutput )
    return o_shader

def build_material(i_stage, i_mtl_scope, i_name):
    return UsdShade.Material.Define(
        i_stage,i_mtl_scope.GetPath().AppendChild(i_name))


def main():
    # main details for current asset
    #
    asset_name = "simpleAsset"
    root_path = Sdf.Path.absoluteRootPath
    root_asset_path = root_path.AppendChild(asset_name)

    # build lower-level usd file with actual geometry
    #
    geo_filename = './geo.usd'
    # create stage for geometry
    stage = stage_begin(geo_filename)
    # build root
    root = build_asset_root(stage, root_asset_path)
    # at geometry level we apply the GeomModelAPI schema
    UsdGeom.ModelAPI.Apply(root.GetPrim())
    # the geo prim to hold proxy and render prims
    geo_scope = UsdGeom.Scope.Define(stage, root.GetPath().AppendChild("geo"))
    # proxy prim will contain low-res geometry for proxy-purpose
    proxy = UsdGeom.Scope.Define(stage, geo_scope.GetPath().AppendChild("proxy"))
    proxy.GetPrim().GetAttribute("purpose").Set("proxy")
    cube = UsdGeom.Cube.Define(stage, proxy.GetPath().AppendChild("{}Shape".format(asset_name)))
    # get proxy-shapes for later binding
    proxy_shapes = [cube.GetPath()]
    # render prim will contain high-res geometry for render-prupose
    render = UsdGeom.Scope.Define(stage, geo_scope.GetPath().AppendChild("render"))
    render.GetPrim().GetAttribute("purpose").Set("render")
    sphere = UsdGeom.Sphere.Define(stage, render.GetPath().AppendChild("{}Shape".format(asset_name)))
    # get render-shapes for later binding
    render_shapes = [sphere.GetPath()]
    # set default prim and close stage
    stage.SetDefaultPrim(root.GetPrim())
    stage_end(stage)

    # build material layer
    #
    mtl_filename = './mtl.usd'
    # create stage for material layer
    stage = stage_begin(mtl_filename)
    # build root prim
    root = build_asset_root(stage, root_asset_path)
    # add geometry reference to root prim
    root.GetPrim().GetReferences().AddReference(geo_filename)
    # create mtl scope to hold all materials for proxy and render purposes
    mtl_scope = UsdGeom.Scope.Define(stage, root.GetPath().AppendChild("mtl"))
    # create material and shader for purposes and bind to shapes
    proxy_material = build_material(stage,mtl_scope,"proxy_material")
    proxy_shader_mtlx = build_mtlx_standard_surface(stage,proxy_material,"proxy_shader_mtlx")
    proxy_shader = build_preview_shader(stage,proxy_material,"proxy_shader")
    for p in proxy_shapes:
        p_over = stage.OverridePrim(p)
        UsdShade.MaterialBindingAPI.Apply(p_over)
        UsdShade.MaterialBindingAPI(p_over).Bind(proxy_material)
    render_material = build_material(stage,mtl_scope,"render_material")
    render_shader_mtlx = build_mtlx_standard_surface(stage,render_material,"render_shader_mtlx")
    render_shader = build_preview_shader(stage,render_material,"render_shader")
    for p in render_shapes:
        p_over = stage.OverridePrim(p)
        UsdShade.MaterialBindingAPI.Apply(p_over)
        UsdShade.MaterialBindingAPI(p_over).Bind(render_material)
    # set default prima and close stage
    stage.SetDefaultPrim(root.GetPrim())
    stage_end(stage)

    # build top-level payload with geometry and material
    #
    payload_filename = './payload.usd'
    # create stage for payload
    stage = stage_begin(payload_filename)
    # add material layer to sublayers
    stage.GetRootLayer().subLayerPaths = [mtl_filename]
    # create root prim
    root = build_asset_root(stage, root_asset_path)
    # set default prim and close the stage
    stage.SetDefaultPrim(root.GetPrim())
    stage_end(stage)

    # build main asset file
    #
    asset_filename = './{}.usd'.format(asset_name)
    # create stage for main asset file
    stage = stage_begin(asset_filename)
    # build root prim with metadata for current asset
    root = build_asset_root(stage, root_asset_path, 
                            i_asset_name=asset_name, 
                            i_asset_identifier=payload_filename, 
                            i_asset_version="1.0")
    # add payload to root layer to material and geometry are payloaded
    root.GetPrim().GetPayloads().AddPayload(payload_filename)
    # set default prim and close the stage
    stage.SetDefaultPrim(root.GetPrim())
    stage_end(stage)


if __name__ == '__main__':
    main()