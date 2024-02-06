#!/usr/bin/env python3

import subprocess
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

CARDS_FOLDER_NAME = "cards"

def take_snapshots(cards, output_extension):
    images = []
    renderer = get_renderer()

    def task(card):
        cardName = card.usdFileName + "_" + card.name
        image_name = create_image_filename(cardName, output_extension, card.parentPath)
        cmd = ['usdrecord','--camera', card.name, '--imageWidth', str(card.imageWidth), '--renderer', renderer, 'cameras.usda', image_name]
        run_os_specific_command(cmd)
        return image_name
    
    with ThreadPoolExecutor() as executor:
        images = list(executor.map(task, cards))
    
    os.remove("cameras.usda")
    return images

def create_image_filename(card_name, extension, parent_path):
    if CARDS_FOLDER_NAME:
        cards_folder_dir = Path().joinpath(parent_path, CARDS_FOLDER_NAME)
    else:
        cards_folder_dir = parent_path
    cards_folder_dir.mkdir(parents=True, exist_ok=True)
    return str(Path().joinpath(cards_folder_dir, card_name).with_suffix("." + extension)).replace("\\", "/")

def get_renderer():
    if os.name == 'nt':
        print("windows default renderer GL being used...")
        return "GL"
    else:
        if sys.platform == 'darwin':
            print("macOS default renderer Metal being used...")
            return 'Metal'
        else:
            print("linux default renderer GL being used...")
            return 'GL'

def run_os_specific_command(cmd):
    if os.name == 'nt':
        subprocess.run(cmd, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        if sys.platform == 'darwin':
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
