# -*- coding: utf-8 -*-
import os
import openslide
import numpy as np
import scipy.misc

def readimg(path,downsampling = 0, patch_size = 2000):
    """

    :param path:
    :param downsampling:
    :param patch_size:
    :return:
    """
    img = openslide.open_slide(path)
    print("Image level dimensions:{}".format(img.level_dimensions))
    [x,y] =img.level_dimensions[downsampling]
    print("Image size: {} {}".format(x,y))
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
            downsampled_image = np.array(img.read_region((i ,j) ,downsampling ,[x_size ,y_size]))
            savepath = path.split('.')[0]+'_{}_{}.tiff'.format(i,j)
            scipy.misc.imsave(savepath,downsampled_image)


if __name__=="__main__":
    readimg("TCGA.svs")