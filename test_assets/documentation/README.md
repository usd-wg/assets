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
| [BoxAnimated](../BoxAnimated/)                                |![](../BoxAnimated/screenshot/USDView_BoxAnimated.gif)|![](../BoxAnimated/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BoxAnimated)|  Passed      | 
| [BrainStem](../BrainStem/)                                    |![](../BrainStem/screenshot/USDView_BrainStem.gif)|![](../BrainStem/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BrainStem)|  Passed     | 
| [Cesium Man](../CesiumMan/)                                   |![](../CesiumMan/screenshot/USDView_CesiumMan.gif)|![](../CesiumMan/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/CesiumMan)|  Passed      | 
| [Interpolation Test](../InterpolationTest/)                   |![](../InterpolationTest/screenshot/USDView_InterpolationTest.gif)|![](../InterpolationTest/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/InterpolationTest)|  Passed     | 
| [Iridescent Dish with Olives](../IridescentDishWithOlives/)   |![](../IridescentDishWithOlives/screenshot/USDView_IridescentDishWithOlives.gif)|![](../IridescentDishWithOlives/screenshot/glassCover_animation.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/IridescentDishWithOlives)|  Animation works but materials not seen, maybe not using usdview properly      | 
| [Morph Stress Test](../MorphStressTest/)                      |n/a|![](../MorphStressTest/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/MorphStressTest)|  Not Started      |
| [Rigged Figure](../RiggedFigure/)                             |n/a|![](../RiggedFigure/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedFigure)|  Not Started      |  
| [Rigged Simple](../RiggedSimple/)                             |n/a|![](../RiggedSimple/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedSimple)|  Not Started      |  
| Simple Skin                                                   |n/a|![](../SimpleSkin/screenshot/screenshot.gif)| [Link](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/SimpleSkin)|  Failed to Convert      |  