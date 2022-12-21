import os, glob, pathlib


class ProjectFolder(object):
    def __init__(self, project='Inn', worksapce='Qsync/Project', sourceimages='sourceimages', scenes='scenes'):
        self.home = pathlib.Path.home()
        self.texture_folder = self.home / worksapce / project / sourceimages
        self.scenes_folder = self.home / worksapce / project / scenes

        self.imgList = self.buildImgList()

    def get_texture_folder(self):
        """
        Get 'sourceimages' folder
        :return: (str) 'sourceimages' folder
        """
        return str(self.texture_folder)

    def get_images(self):
        """
        Get list of all textures in 'sourceimages' folder
        :return: (list) images
        """
        return self.imgList

    def buildImgList(self, search_extension='png'):
        """
        Return a list with all images in a folder: image.png
        :param path: (str) path
        :return: (list) imgList
        """
        imgList = []
        os.chdir(self.get_texture_folder())
        for file in glob.glob('*.' + search_extension):
            imgList.append(file)

        return imgList

def getTextureFromNode(file):
    """
    Return texture file with info
    :param file: (str) file path
    :return: (pathlib.Path) baseColor_texture_path
    """
    baseColor_texture_path = pathlib.Path(file)

    return baseColor_texture_path

def getTextureBaseName(texture_stem):
    """
    Return Texture without '_BaseColor'
    :param texture_stem: texture file
    :return: (str) Texture base name
    """
    texture = str(texture_stem)
    if texture.count('BaseColor'):
        #texture = texture.split(' - ')[0]
        return '_'.join(texture.split('_')[:-1])

    return texture


if __name__ == "__main__":
    #print(getTextureBaseName(getTextureFromNode('//daz_import\.\Maps\BackBar_PNTR_Mat1_BaseColor.png')[2]))
    print(getTextureBaseName(getTextureFromNode('//daz_import/./Maps/Debris_PNTR-Tile_BaseColor.png').stem))
