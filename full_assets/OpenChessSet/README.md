
# The Open Chess Set

![The Open Chess Set, rendered in Arnold for Maya](teaser.png)

A complete USD chess set, with materials encoded in the MaterialX standard. Autodesk's [Standard Surface](https://autodesk.github.io/standard-surface/) is used throughout the project, covering shading scenarios including transmission and subsurface scattering.


## Origin

The asset was authored by Moeen and Mujtaba Sayed for the Houdini Tutorial [Karma | A Beautiful Game](https://www.sidefx.com/tutorials/karma-a-beautiful-game/).

It was then contributed to the [MaterialX project](https://github.com/AcademySoftwareFoundation/MaterialX) by SideFX, with a [conversion](https://github.com/AcademySoftwareFoundation/MaterialX/pull/982) to glTF being done by Chris Rydalch and Mark Elendt together with additional refinements by Jonathan Stone. In a later contribution, Ed Mackey baked displacement into the normal maps (MaterialX[#1098](https://github.com/AcademySoftwareFoundation/MaterialX/pull/1098)).

A compatibility-focused USD version was created by Pablo Delgado for the ASWF Open Source Days 2022 MaterialX & OSL panel ([slides](https://materialx.org/assets/ASWF_OSD2022_MaterialX_OSL_Final.pdf)). This version was then reworked for use as an openly available USD reference asset.


## Known Problems

- The MaterialX `colorspace` attribute is poorly supported in Hydra render delegates (10/2022). This may lead to incorrect brightening of the base color.
- z-fighting can be observed in Pixar's Storm Hydra render delegate (v22.08)


## Future Improvements

UsdPreviewSurfaces and displacement maps can be added.


## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) by the Academy Software Foundation.
