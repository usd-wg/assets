# Simple Transform

## Screenshot

![screenshot](screenshots/simple_transform_usdrecord_22.08.png)
_usdrecord 22.08_

## Description

This file shows an example of a mesh with a simple, ../_common stack of transform operations.

```usda
uniform token[] xformOpOrder = [
    "xformOp:translate",
    "xformOp:rotateXYZ",
    "xformOp:scale"
]
```

Schema specification: <https://github.com/PixarAnimationStudios/USD/blob/release/pxr/usd/usdGeom/schema.usda>
