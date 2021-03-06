# -*- coding: utf-8 -*-
import os
import cv2
import json
import openslide
import numpy as np

class WSI(object):
    def __init__(self,svs_path):
        self.path = svs_path
        self.wsi = openslide.OpenSlide(self.path)
        self.header = {}
        self.image = None
        self.header['producer'] = self.wsi.detect_format(self.path)
        self.header['level_count'] = self.wsi.level_count
        self.header['level_downsamples'] = self.wsi.level_downsamples
        for key, content in self.wsi.associated_images.items():
            self.header[key] = np.array(content)
        self.header['level_downsamples'] = self.wsi.level_downsamples

    def save_header(self,folder = None):
        savepath = self.path.replace(self.path.endswith,'.json')
        if folder is None:
            folder = os.path.dirname(self.path)
        else:
            if not os.path.isdir(folder):
                os.mkdir(folder)
                savepath = os.path.join(folder,savepath.split('/')[-1])
        with open(savepath,'wb') as header:
            json.dump(self.header,header)
            
    def read(self, level = 0, patch_size = 4000):
        """
        param level: int type which layer extract from image pyramid, default is '0' 
        param patch_size: int type that small patch's size for extract image piles by piles
        return: 'numpy.ndarray' type, the image extracted out
        """
        [x,y] =self.wsi.level_dimensions[level]
        print("Image size of level {}: {} {}".format(level, x, y))
        image = np.zeros([y,x,3],np.uint8)
        x_range = list(range(0,x,patch_size))
        y_range = list(range(0,y,patch_size))
        for i in x_range:
            for j in y_range:
                if (i != max(x_range)) and (j != max(y_range)):
                    x_size = y_size = patch_size
                elif i == max(x_range):
                    x_size = x-i
                else:
                    y_size = y-j
                try:
                    patch = np.array(self.wsi.read_region((i ,j) ,level ,[x_size ,y_size]))
                except Exception as e:
                    print('Patch location {} /n'.format((i,j)),e)
                if patch.shape[2]==4:
                    patch = patch[:,:,:3]
                image[j:j+y_size,i:i+x_size] = patch
        return image
    
    def get_thumbnail(self,ratio=36):
        """
        param ratio: int type means original image's size divide thumbnail image's size
        return: thumbnail image
        """
        [x,y] =self.wsi.level_dimensions[0]
        thumbnail = self.wsi.get_thumbnail((x/ratio,y/ratio))
        return thumbnail
        
    def close(self):
        """
        Close wsi object for release memory
        """
        self.wsi.close()
        
# if __name__=="__main__":
#     readimg("TCGA.svs")
