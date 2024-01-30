# USD Cards Generator

## Purpose
Given a USD file, take pictures of each of it's axes and assign them as the cards' images

## Usage

`python generate_cards.py --usd-file <usd_file>`

optional arguments:
  - `usd-file` : The USD file you want to generate card images from
  - `-h`, `--help` : Show help
  - `--create-usdz-result` :  Returns the resulting files as a new USDZ file called `<subject_usd_file>_Cards.usdz`
  - `--output-extension` :    The file extension of the output image you want (exr, png..). If using exr, make sure your usd install includes OpenEXR
  - `--verbose` :             Prints out the steps as they happen
  - `--dome-light` :          The path to the dome light HDR image to use, if any
  - `--apply-cards` :         Saves the images as the cards for the given USD file. If USDZ is input, a new USD file will be created to wrap the existing one called `<subject_usd_file>_Cards.usd`
  - `--render-purposes` :     A comma separated list of render purposes to include in the thumbnail. Valid values are: default, render, proxy, guide
  - `--image-width`:          The width of the image to generate. Default is 2048
  - `--directory` :           A directory to generate thumbnails for all .usd, .usda, .usdc, and .usdz files. When a directory is supplied, usd-file is ignored
  - `--recursive` : Will recursively search all directories underneath a given directory, requires a directory to be set

  Note: You must have usd installed and available in your path. [Install Steps Here](https://github.com/PixarAnimationStudios/OpenUSD#getting-and-building-the-code)

## How it works when using --apply-cards
Given a USD file to use as the subject of the cards do the following

1. Apply DrawMode defaults (cards attribute, box geometry)
2. Create, position, and orient cameras for each axis (XPos, XNeg, YPos, YNeg, ZPos, ZNeg)
3. Sublayer the subject in the camera
4. Run `usdrecord` to take a snapshot and store it in `/renders/<axis>.0.png`
    - macOS
        - `usdrecord --frames 0:0 --camera ZCamera --imageWidth 2048 --renderer Metal camera.usda <axis>.#.png` 
    - windows
        - `usdrecord --frames 0:0 --camera ZCamera --imageWidth 2048 --renderer GL camera.usda <axis>.#.png` 
        - note: this will run with `shell=True` for the subprocess call
    - linux
        - `usdrecord --frames 0:0 --camera ZCamera --imageWidth 2048 --renderer Metal camera.usda <axis>.#.png`
    - ZCamera & camera.usda are generated in step 2
4. If the file is not a USDZ file, assign each image as the usd's axis card image
5. If the file is a USDZ file, create a new `<subject_usd_file>_Cards.usda`, assign each image as the usd's axis card image, and sublayer `<subject_usd_file>.usdz`
6. If `--create-usdz-result` is passed in, combine all of the files into a USDZ, in the case of a USD file it would be the input file and each axis image. In the case of a USDZ file it would be the new USDA, the axis images, and the input USDZ
