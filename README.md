# USD Assets Working Group

This repository contains examples of USD assets provided under the umbrella of the [ASWF USD WG](https://wiki.aswf.io/display/WGUSD).
Our objective is to foster information exchange within the USD community regarding USD asset import/export, asset structure, testing, and schema design. The overarching goal of this group is to bolster the U of USD.

The GitHub repository is only half the story: much of the value this working group provides is in the monthly sync where folks present schema, discuss asset/pipeline problems, and share plans for this repository -- please consider joining!

## Web Catalog

You can browse and preview the assets in this repository live in the online [Web Catalog](https://usd-assets.needle.tools/), which renders the USD assets using USD-WASM.

## What's in this Repo?

The repository is roughly structure into three buckets: documentation, test assets, and full assets.

**Documentation:** A collection of markdown docs and educational assets designed for education and common practices for asset design.

**Test Assets:** Test assets are intended to be used as unit tests and include docs and screenshots.
Correct and intentionally malformed assets are included in this collection.
Schema-specific assets are designed to aid developers in correctly handling various USD schema. It's often unclear exactly how a specific
schema should be imported or exported based on the schema docs alone and the unit tests provided by the schema typically don't include
written descriptions of intent or reference images to show how a given asset should appear.

**Full Assets:** The full_assets folder contains examples of assets that you might find in the wild, in terms of their structure, but are still limited in terms of file size. The largest "full asset" at the time of this writing is 30mb.

![image](https://github.com/usd-wg/assets/assets/1510114/e4d19125-371c-4940-9894-17af119822bc)
(Full asset example: [StandardShaderBall](full_assets/StandardShaderBall/))

## Contributing
If you'd like to get involved to contribute, discuss schema, or just generally talk about USD assets, please reach out on slack or join our monthly sync:

 * Slack: [#wg-usd-assets](https://academysoftwarefdn.slack.com/archives/C02TZPYMP8S) on [academysoftwarefdn.slack.com](https://join.slack.com/t/academysoftwarefdn/shared_invite/zt-24cnganaf-~1UQpPJIdeoQohWk0k5X5g)
 * [Meeting Notes](https://drive.google.com/drive/u/0/folders/1jIosOIcpnLDLdcjv78NN8g7TWJR3KaIZ)
 * [Wiki Page](https://wiki.aswf.io/display/WGUSD/USD+Assets)
 * [Calendar](https://lists.aswf.io/g/wg-usd/calendar)
 * Zoom: note that after the switch to LXF, you must now register for the event and will be given a personalized zoom link (also note that this link is personalized and cannot be shared).

### Submitting a New Asset

Before submitting, take a look at an existing asset. A well formed example should include a read me doc with license, a screenshot and comments
on how the asset is intended to be used and common issues to avoid.

A minimal schema test asset should include one representative asset per USD schema, with qualitative & quantitative
descriptions, along with screenshots of what the asset should look like when correctly imported and exported. In addition, the
readme page should offer high-level guidance on round-trip concerns or common issues specific to the schema.

## Why ASWF USD Assets and ASWF DPEL Assets?

The Digital Production Example Library (DPEL) is for production assets of all data formats, where the USD Assets group is purely for USD assets,
which are explicitly small and/or educational (very much NOT production assets).

# Even Moar USD Assets

The USD Assets repository is limited to small assets designed for testing, validation, and learning; the external links we've collected below
are larger assets more representative of something in a real production, which can be useful for scale testing or learning how a large pipeline
is designed.

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

If you have suggestions for this list, please open a GitHub issue and share a link!
 
### Notable Asset Stores with USD Content

 * [CG Trader](https://www.cgtrader.com/3d-models/ext/usd)
 * [SketchFab](https://sketchfab.com/) - all models available as USDZ
 * [Turbo Squid](https://www.turbosquid.com/Search/3D-Models/usd)

### Tutorial Assets, Blogs & Videos

 * [Awesome OpenUSD](https://github.com/matiascodesal/awesome-openusd) a collection of tutorials and educational links by Matias Codesal
 * [The Book of USD](https://remedy-entertainment.github.io/USDBook/) by Remedy Entertainment
 * [USD Hello World](https://github.com/carlynorama/USDHelloWorld) also see the related [Blog Post](https://github.com/carlynorama/USDHelloWorld#toc) by carlynorama
 * [UsdSkel Tutorial](https://www.youtube.com/playlist?list=PL5P7shki7MOWkMgMpRkPl-nNVJEKRU8fQ) by Matias Codesal

# Licenses

Each asset has a license declared in the readme, typically CC0 or something highly permissive. Everything else is provided under the [repository license](LICENSE).
