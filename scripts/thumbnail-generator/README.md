# USD Thumbnail Generator

## Purpose
Given a USD file, take a picture and assign it as it's thumbnail.

## Usage

`python generate_thumbnail.py <usd_file>`

positional arguments:
  - `usd_file` : The USD file you want to add a thumbnail to. If USDZ is input, a new USD file will be created to wrap the existing one called `<subject_usd_file>_Thumbnail.usd`

optional arguments:
  - `-h`, `--help` : Show help
  - `--create-usdz-result` :  Returns the resulting files as a new USDZ file called `<subject_usd_file>_Thumbnail.usdz`
  - `--output-extension` :    The file extension of the output image you want (exr, png..). If using exr, make sure your usd install includes OpenEXR
  - `--verbose` :             Prints out the steps as they happen
  - `--dome-light` :          The path to the dome light HDR image to use, if any

  Note: You must have usd installed and available in your path. [Install Steps Here](https://github.com/PixarAnimationStudios/OpenUSD#getting-and-building-the-code)

## How it works
Given a USD file to use as the subject of the thumbnail do the following

1. Generate a camera such that the subject is in view
2. Sublayer the subject in the camera
3. Run `usdrecord` to take a snapshot and store it in `/renders/<input>.png`
    - macOS
        - `usdrecord --camera ZCamera --imageWidth 2048 --renderer Metal camera.usda <input>.png` 
    - windows
        - `usdrecord --camera ZCamera --imageWidth 2048 --renderer GL camera.usda <input>.#.png` 
        - note: this will run with `shell=True` for the subprocess call
    - linux
        - `usdrecord --camera ZCamera --imageWidth 2048 --renderer Metal camera.usda <input>.png`
    - ZCamera & camera.usda are generated in step 2
4. If the file is not a USDZ file, assign that image as the usd's thumbnail image
5. If the file is a USDZ file, create a new `<subject_usd_file>_Thumbnail.usda`, assign the image as the thumbnail, and sublayer `<subject_usd_file>.usdz`
6. If `--create-usdz-result` is passed in, combine all of the files into a USDZ, in the case of a USD file it would be the input file and the image. In the case of a USDZ file it would be the new USDA, the image, and the input USDZ


## Thumbnail Usage

Thumbnails are being used in these apps:

- [Needle Tools - Asset Explorer](https://asset-explorer.needle.tools)
  - In the Information and Downloads section of any asset, the USDZ image is using Thumbnails