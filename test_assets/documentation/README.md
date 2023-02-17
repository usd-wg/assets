# Test Asset Docs


## Convert from gltf 2.0 -> usdz

### Goal

Generate a library of good test assets in usdz like there are in gltf. Given the repo [here](https://github.com/KhronosGroup/glTF-Sample-Models) generate equivalent usdz files for each asset, with a focus on animations

### Process
1. Pulled down the [gltf-Sample-Models](https://github.com/KhronosGroup/glTF-Sample-Models) repository
2. Downloaded [Reality Converter](https://developer.apple.com/news/?id=01132020a)
3. For Each asset, drag and drop the asset folder into Reality Converter
4. If the asset loads properly, export it back out of Reality Converter to generate .usdz
5. Commit .usdz file
6. Pull branch on PC to run [USDView](https://graphics.pixar.com/usd/release/toolset.html#usdview) from [Omniverse Launcher](https://www.nvidia.com/en-us/omniverse/download/)
7. Using [ScreenToGif](https://www.screentogif.com) record the animation in USDView
8. Save new screenshot and update this doc.


### Animated Assets

| Name                                  | usdz Screenshot                                           |  glTF Screenshot                                  | gltf2.0 Link                                                                              |   Status               | 
|-----------------------                |-----------                                                | ---------                                         |-------------------------------                                                            |---------         |
| [Animated Cube](../AnimatedCube/)                             | ![](../AnimatedCube/screenshot/USDView_AnimatedCube.gif)  | ![](../AnimatedCube/screenshot/screenshot.gif) | [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedCube)   |  Passed                |
| [Animated Morph Cube](../AnimatedMorphCube/)                  |n/a|![](../AnimatedMorphCube/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedMorphCube)|  Failed to view in usdview      | 
| [Animated Morph Sphere](../AnimatedMorphSphere/)              |n/a|![](../AnimatedMorphSphere/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedMorphSphere)|  Failed to view in usdview     | 
| [Animated Triangle](../AnimatedTriangle/)                     |![](../AnimatedTriangle/screenshot/USDView_AnimatedTriangle.gif) |![](../AnimatedTriangle/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedTriangle)|  Passed      | 
| [BoxAnimated](../BoxAnimated/)                                |n/a|![](../BoxAnimated/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BoxAnimated)|  Not Started      | 
| [BrainStem](../BrainStem/)                                    |n/a|![](../BrainStem/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BrainStem)|  Not Started      | 
| [Cesium Man](../CesiumMan/)                                   |n/a|![](../CesiumMan/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/CesiumMan)|  Not Started      | 
| [Interpolation Test](../InterpolationTest/)                   |n/a|![](../InterpolationTest/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/InterpolationTest)|  Not Started      | 
| [Iridescent Dish with Olives](../IridescentDishWithOlives/)   |n/a|![](../IridescentDishWithOlives/screenshot/glassCover_animation.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/IridescentDishWithOlives)|  Not Started      | 
| [Morph Stress Test](../MorphStressTest/)                      |n/a|![](../MorphStressTest/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/MorphStressTest)|  Not Started      |
| [Rigged Figure](../RiggedFigure/)                             |n/a|![](../RiggedFigure/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedFigure)|  Not Started      |  
| [Rigged Simple](../RiggedSimple/)                             |n/a|![](../RiggedSimple/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedSimple)|  Not Started      |  
| Simple Skin                                                   |n/a|![](../SimpleSkin/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/SimpleSkin)|  Failed to Convert      |  