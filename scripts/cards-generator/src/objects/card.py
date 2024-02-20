from objects.rotation import Rotation

class Card:
    def __init__(self, name, horizontalIndex, verticalIndex, sign, rotations, translationIndex, parentPath, usdFileName, imageWidth):
        self.name = name
        self.horizontalIndex = horizontalIndex
        self.verticalIndex = verticalIndex
        self.sign = sign
        self.rotations = rotations
        self.translationIndex = translationIndex
        self.parentPath = parentPath
        self.usdFileName = usdFileName
        self.imageWidth = imageWidth

    def update_image_width(self, new_width):
        self.imageWidth = new_width