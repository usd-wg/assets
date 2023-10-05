# USD Assets Working Group

This repository contains examples of USD assets provided under the umbrella of the [ASWF USD WG](https://wiki.aswf.io/display/WGUSD).
Our objective is to foster information exchange within the USD community regarding USD asset import/export, asset structure, testing, and schema design. The overarching goal of this group is to bolster the U of USD.

The GitHub repository is only half the story: much of the value this working group provides happens in the montly sync where folks present schema, discuss asset/pipeline problems, and share plans for this repository -- please consider joining!

## Contributing
If you'd like to get involved to contribute, discuss schema, or just generally talk about USD assets, please reach out on slack or join our monthly sync:

 * [Calendar](https://lists.aswf.io/g/wg-usd/calendar)
 * [Wiki Page](https://wiki.aswf.io/display/WGUSD/USD+Assets)
 * Slack: [#wg-usd-assets](https://academysoftwarefdn.slack.com/archives/C02TZPYMP8S) on [academysoftwarefdn.slack.com](https://join.slack.com/t/academysoftwarefdn/shared_invite/zt-24cnganaf-~1UQpPJIdeoQohWk0k5X5g)
 * [Meeting Notes](https://drive.google.com/drive/u/0/folders/1jIosOIcpnLDLdcjv78NN8g7TWJR3KaIZ)
 * Zoom: note that after the switch to LXF, you must now register for the event and will be given a personalized zoom link (also note that this link is personalized and cannot be shared).

## Schema-Specific Assets

Schema-specific assets are designed to to aid developers in correctly implementing the handling of various USD schema. The
motivation behind this is that it's often unclear exactly how a specific schema should be imported or exported based on the
schema alone and the unit tests provided by the schema typically don't include written descriptions of intent or reference images
to show how a given asset should appear.

A minimal starting point for schema test assets would be one representative asset per schema, with qualitative & quantitative
descriptions, along with screenshots of what the asset should look like when correctly imported and exported. In addition, the test
asset should offer high-level guidance on round-trip concerns or common issues specific to the schema.

## Even Moar USD Assets

This repository is focused on small assets designed for testing, validation, and learning; the external links we've collected below
are larger assets and/or live on external repositories. If you have anything to add to this list, please open a GitHub issue and share
a link.

 * [Animal Logic A-Lab](https://animallogic.com/alab)
 * [Apple Sample Assets](https://developer.apple.com/augmented-reality/quick-look/)
 * [Blender Sample Assets](https://download.blender.org/institute/sybren/usd/)
 * [Disney's Moana Island](https://www.disneyanimation.com/data-sets/?drawer=/resources/moana-island-scene/)
 * [DPEL (Digital Production Example Library)](https://dpel.aswf.io/)
 * [DPEL External Asset Links Wiki Page](https://wiki.aswf.io/display/ARW/Links+to+Open+Assets)
 * [Intel's 4004 Moore Lane](https://dpel.aswf.io/4004-moore-lane/)
 * [J-Cube Assets](https://j-cube.jp/solutions/multiverse/assets/)
 * [NVIDIA Sample Assets](https://developer.nvidia.com/usd#sample)
 * [PhysicallyBased.info MaterialX Shaders](https://physicallybased.info/)
 * [Pixar Sample Assets](https://graphics.pixar.com/usd/downloads.html)
 * [Polyhaven](https://github.com/minami110/polyhaven)
 * [Side FX - Bar Scene](https://www.sidefx.com/contentlibrary/bar-scene/)
 * [Side FX - Content Library](https://www.sidefx.com/contentlibrary/)
 
### Notable Asset Stores with USD Content

 * [CG Trader](https://www.cgtrader.com/3d-models/ext/usd)
 * [SketchFab](https://sketchfab.com/) - all models available as USDZ
 * [Turbo Squid](https://www.turbosquid.com/Search/3D-Models/usd)

### Tutorial Assets, Blogs & Videos

 * [Awesome OpenUSD](https://github.com/matiascodesal/awesome-openusd) a collection of tutorials and educational links by Matias Codesal
 * [The Book of USD](https://remedy-entertainment.github.io/USDBook/) by Remedy Entertainment
 * [USD Hello World](https://github.com/carlynorama/USDHelloWorld) also see the related [Blog Post](https://github.com/carlynorama/USDHelloWorld#toc) by carlynorama
 * [UsdSkell Tutorial](https://www.youtube.com/playlist?list=PL5P7shki7MOWkMgMpRkPl-nNVJEKRU8fQ) by Matias Codesal
