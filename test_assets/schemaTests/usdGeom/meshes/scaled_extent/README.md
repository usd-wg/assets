# Scaled Extent

## Screenshot

![screenshot](screenshots/scaled_extent_usdrecord_22.08.png)
_usdrecord 22.08_

## Description

These two meshes have scaled extents. The original extent was:

```usda
float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
```

Extent too small:

```usda
float3[] extent = [(-0.1, -0.1, -0.1), (0.1, 0.1, 0.1)]
```

Extent too big:

```usda
float3[] extent = [(-1, -1, -1), (1, 1, 1)]
```

Schema specification: <https://github.com/PixarAnimationStudios/USD/blob/release/pxr/usd/usdGeom/schema.usda>
