# Inverse Extent

## Screenshot

![screenshot](screenshots/inverse_extent_usdrecord_22.08.png)
_usdrecord 22.08_

This screenshot is empty as expected.

## Description

This mesh has its extent values in the wrong order:

```usda
float3[] extent = [(1,1,1), (0,0,0)]
```

The correct order is:

```usda
float3[] extent = [(0,0,0), (1,1,1)]
```

Schema specification: <https://github.com/PixarAnimationStudios/USD/blob/release/pxr/usd/usdGeom/schema.usda>
