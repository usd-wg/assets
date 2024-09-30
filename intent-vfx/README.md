# intent-vfx

The intent of this structure is to be an initial guide to one of the many possible ways in which assets and scenes can be described in OpenUSD, trying to answer to some of the VFX-pipeline workflow requirements.

The full description of where this structure is starting from can be found in the `docs` of this repo.

## VFX workflow requirements

### Contributions from various departments

The very first requirement is to be able to describe the content with layered content, usually contributed by various departments in a non-destructive manner.

### Granularity

Content should be granular enough to allow for per-shape shading and/or geometric opinions.

### Scriptable

Creation and/or edits should be scriptable using OpenUSD API (Sdf, Usd, etc).

Scripts for example use-cases are more than welcome.

### Instancing

Explicit and implicit instancing (PointInstancers and native-instancing via instanceable metadata) should be used to provide example of how to apply edits (for materials or geometry or anything else) via composition-arcs and retain instanceability.

### Large scene scalability

Together with instancing, also providing various representations and/or LODs for various purposes will help handling large scenes, and allow for scalable structures in the future ( e.g. alternative representations of larger layouts could be provided as variants for specific purposes ).

### Type and Kind hierarchy

Simple but useful type and kind hierarchy to allow for better interrogability and usability.

### Files and folders structure

A simple structure, with ability to re-use and share assets or contributions across assets (textures, materials) could be a plus.

Quite often this is very specific to pipelines and it might be the very first thing you want to change if starting from these guidelines.

## Not accounted for

Versions are usually very specific to pipeline, so we are not handling those here.

Assets and scenes are always on latest, history is only provided as git-history by the repo.

## Assets generation

There are two scripts to generate a `simpleAsset` and a `teapot` asset, and they are almost identical scripts.

The `simpleAsset` has 2 purposes, with a `cube` for the `proxy` purpose, and a `sphere` for the `render` purpose.

The `teapot` asset has only a `default` purpose.

To run the script

```
cd assets/teapot
python ../../build_teapot.py
```

or

```
cd assets/simpleAsst
python ../../build_simpleAsset.py
```

## Layout generation

There are 2 scripts to generate a layout per asset, in a concentric-ring distribution, having each ring to randomly use PointInstancers or native-instancing for its instances.

Even if there are mixed PointInstancers and individual elements, the layouts are made so that only one implicit prototype is actually created, shared across all elements and PointInstancers prototypes.

To run the script to build the layouts:

```
cd scenes
python ../build_scene_teapot.py
```

or

```
cd scenes
python ../build_scene_simpleAsset.py
```

A third script is provided to generate a new-layer for the `teapotScene`, with overrides to materials and geometry, with a controlled implicit prototypes creation, where each set of "overrides" is provided as an abstract prim inherited on elements and PointInstancers where edits are applied.

To run the script to build the overrides:

```
cd scenes
python ../build_scene_teapot_overrides.py
```
