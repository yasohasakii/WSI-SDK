import io

from PIL import Image
from openslide import AbstractSlide, _OpenSlideMap

from kfbslide import utils


class kfbRef:
    img_count = 0


class TSlide(AbstractSlide):
    def __init__(self, filename):
        AbstractSlide.__init__(self)
        self.__filename = filename
        self._osr = utils.kfbslide_open(filename)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__filename)

    @classmethod
    def detect_format(cls, filename):
        return utils.detect_vendor(filename)

    def close(self):
        utils.kfbslide_close(self._osr)

    @property
    def level_count(self):
        return utils.kfbslide_get_level_count(self._osr)

    @property
    def level_dimensions(self):
        return tuple(utils.kfbslide_get_level_dimensions(self._osr, i)
                     for i in range(self.level_count))

    @property
    def level_downsamples(self):
        return tuple(utils.kfbslide_get_level_downsample(self._osr, i)
                     for i in range(self.level_count))

    @property
    def properties(self):
        return _KfbPropertyMap(self._osr)

    @property
    def associated_images(self):
        return _AssociatedImageMap(self._osr)

    def get_best_level_for_downsample(self, downsample):
        return utils.kfbslide_get_best_level_for_downsample(self._osr, downsample)

    # def read_region(self, location, level, size):
    #     import pdb
    #     #pdb.set_trace()
    #     x = int(location[0])
    #     y = int(location[1])
    #     img_index = kfbRef.img_count
    #     kfbRef.img_count += 1
    #     # print("img_index : ", img_index, "Level : ", level, "Location : ", x , y)
    #     return utils.kfbslide_read_region(self._osr, level, x, y)

    def read_region(self, location, level, size):
        # import pdb

        x = int(location[0])
        y = int(location[1])
        width = int(size[0])
        height = int(size[1])
        img_index = kfbRef.img_count
        kfbRef.img_count += 1

        return Image.open(io.BytesIO(utils.kfbslide_read_roi_region(self._osr, level, x, y, width, height)))

    def get_thumbnail(self, size):
        """Return a PIL.Image containing an RGB thumbnail of the image.

        size:     the maximum size of the thumbnail."""

        thumb = self.associated_images[b'thumbnail']
        return thumb


class _KfbPropertyMap(_OpenSlideMap):
    def _keys(self):
        return utils.kfbslide_property_names(self._osr)

    def __getitem__(self, key):
        v = utils.kfbslide_property_value(self._osr, key)
        if v is None:
            raise KeyError()
        return v


class _AssociatedImageMap(_OpenSlideMap):
    def _keys(self):
        return utils.kfbslide_get_associated_image_names(self._osr)

    def __getitem__(self, key):
        if key not in self._keys():
            raise KeyError()
        return utils.kfbslide_read_associated_image(self._osr, key)


def open_kfbslide(filename):
    try:
        return TSlide(filename)
    except Exception:
        return None

import numpy as np
class kfb:
    def __init(self,path):
        self.slide = TSlide(path)
        self.patch_size = 4000
        
    def header(self):
        header = {}
        for key, val in self.slide.associated_images.items():
            print(key, " --> ", val.size)
            header[key] = np.array(val)
        return header

    def read(self,level = 0):
        [x, y] = self.slide.level_dimensions[level]
        print("Resolution --> {}, {}".format(x,y))
        image = np.zeros([y,x,3],np.uint8)
        x_range = list(range(0,x,patch_size))
        y_range = list(range(0,y,patch_size))
        for i in x_range:
            for j in y_range:
                x_size = y_size = patch_size
                if i == max(x_range):
                    x_size = x-i
                if j == max(y_range):
                    y_size = y-j
                patch =  np.array(self.slide.read_region((i ,j) ,level ,(x_size ,y_size)))
                if patch.shape[2] == 4:
                    r, g, b, a = cv2.split(patch)
                    patch = cv2.merge([r, g, b])
                image[j:j+y_size,i:i+x_size,:] = patch 
        return image


if __name__ == '__main__':
    _, image = kfbread('./2018-08-29 17_11_05.kfb')
    import cv2
    cv2.imwrite('./2018-08-29 17_11_05.jpg',image)
