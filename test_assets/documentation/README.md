# Test Asset Docs


## Convert from glTF 2.0 -> usdz

### Goal

Given the repo [here](https://github.com/KhronosGroup/glTF-Sample-Models) generate equivalent usdz files for each asset, with a focus on animations

### Process
1. Pulled down the [glTF-Sample-Models](https://github.com/KhronosGroup/glTF-Sample-Models) repository
2. Downloaded [Reality Converter](https://developer.apple.com/news/?id=01132020a)
3. For Each asset, drag and drop the asset folder into Reality Converter
4. If the asset loads properly, export it back out of Reality Converter to generate .usdz
5. Commit .usdz file
6. Pull branch on PC to run [USDView](https://graphics.pixar.com/usd/release/toolset.html#usdview) from [Omniverse Launcher](https://www.nvidia.com/en-us/omniverse/download/)
7. Using [ScreenToGif](https://www.screentogif.com) record the animation in USDView
8. Save new screenshot and update this doc.

**Note: For all failed projects, `usdchecker` will be run to debug further**


### Animated Assets

| Name                                  | usdz Screenshot                                           |  glTF Screenshot                                  | glTF 2.0 Link                                                                               |   Animation Runs?               | 
|-----------------------                |-----------                                                | ---------                                         |-------------------------------                                                            |---------         |
| [Animated Cube](../AnimatedCube/)                             | ![](../AnimatedCube/screenshot/USDView_AnimatedCube.gif)  | ![](../AnimatedCube/screenshot/screenshot.gif) | [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedCube)   |  Yes                |
| [Animated Morph Cube](../AnimatedMorphCube/)                  |n/a|![](../AnimatedMorphCube/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedMorphCube)|  No, no asset seen      | 
| [Animated Morph Sphere](../AnimatedMorphSphere/)              |n/a|![](../AnimatedMorphSphere/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedMorphSphere)|  No, no asset seen     | 
| [Animated Triangle](../AnimatedTriangle/)                     |![](../AnimatedTriangle/screenshot/USDView_AnimatedTriangle.gif) |![](../AnimatedTriangle/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/AnimatedTriangle)|  Yes      | 
| [BoxAnimated](../BoxAnimated/)                                |![](../BoxAnimated/screenshot/USDView_BoxAnimated.gif)|![](../BoxAnimated/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BoxAnimated)|  Yes      | 
| [BrainStem](../BrainStem/)                                    |![](../BrainStem/screenshot/USDView_BrainStem.gif)|![](../BrainStem/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/BrainStem)|  Yes     | 
| [Cesium Man](../CesiumMan/)                                   |![](../CesiumMan/screenshot/USDView_CesiumMan.gif)|![](../CesiumMan/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/CesiumMan)|  Yes      | 
| [Interpolation Test](../InterpolationTest/)                   |![](../InterpolationTest/screenshot/USDView_InterpolationTest.gif)|![](../InterpolationTest/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/InterpolationTest)|  Yes     | 
| [Iridescent Dish with Olives](../IridescentDishWithOlives/)   |![](../IridescentDishWithOlives/screenshot/USDView_IridescentDishWithOlives.gif)|![](../IridescentDishWithOlives/screenshot/glassCover_animation.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/IridescentDishWithOlives)|  Yes, but possible material issue   | 
| [Morph Stress Test](../MorphStressTest/)                      |n/a|![](../MorphStressTest/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/MorphStressTest)|  No, no asset seen      |
| [Rigged Figure](../RiggedFigure/)                             |![](../RiggedFigure/screenshot/USDView_RiggedFigure.gif)|![](../RiggedFigure/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedFigure)|  Yes      |  
| [Rigged Simple](../RiggedSimple/)                             |![](../RiggedSimple/screenshot/USDView_RiggedSimple.gif)|![](../RiggedSimple/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/RiggedSimple)|  Yes      |  
| Simple Skin                                                   |n/a|![](../SimpleSkin/screenshot/screenshot.gif)| [glTF 2.0 Link ](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/SimpleSkin)|  Failed to Convert      |  
