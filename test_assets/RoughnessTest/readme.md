# Roughness Material Constant vs Texture Test

## Screenshot

![screenshot](screenshots/usdview-20.08.png)  

## Description

This file contains six meshes, the left three specify roughness values of 0.0, 0.33, and 0.66 specified via a texture.
The right three meshes similarly specify roughness, however the value is authored as a constant on the UsdPreviewSurface material.

Specification: https://graphics.pixar.com/usd/release/spec_usdpreviewsurface.html#roughness-vs-glossiness

The meshes are aligned intentionally to make it easy to compare lighting between the textured and constant versions. The intended
use for debugging is to catch a light highlight directly on the split between meshes to enable easy visual inspection of the 
lighting response (see below).

![screenshot](screenshots/usdview-split000-20.08.png)  
![screenshot](screenshots/usdview-split033-20.08.png)  
![screenshot](screenshots/usdview-split066-20.08.png)  

The roughness values are packed into a single texture, with the red channel set to 0.00, the green channel set to 0.33, and the
blue channel is set to 0.66.

Note: that in the screenshots above, usdview is rendering the mesh as semi-transparent, which is incorrect.

Created on contract by [Nika Somkhishvili](https://www.fiverr.com/nikasomkhishvil).

## License Information

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)  
To the extent possible under law, Unity has waived all copyright and related or neighboring rights to this asset.  


