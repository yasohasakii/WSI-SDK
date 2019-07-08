# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from scipy import misc
import skimage.morphology

def OutsSeg(path):
    def resize(src_image,h,w):
        H, W =src_image.shape[:2]
        if src_image.ndim==3:
            dst_image = np.zeros([h,w,3],np.uint8)
        else:
            dst_image = np.zeros([h,w],np.uint8)
        dst_image[:h/2,:w/2] = misc.imresize(src_image[:H/2,:W/2],(h/2,w/2),'nearest')
        dst_image[h/2:,:w/2] = misc.imresize(src_image[H/2:,:W/2],(h-h/2,w/2),'nearest')
        dst_image[:h/2,w/2:] = misc.imresize(src_image[:H/2,W/2:],(h/2,w-w/2),'nearest')
        dst_image[h/2:,w/2:] = misc.imresize(src_image[H/2:,W/2:],(h-h/2,w-w/2),'nearest')
        return dst_image

    savefolder = os.path.join(os.path.dirname(path),'segment')
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    image = cv2.imread(path)
    # image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    gray = 255 - cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    h = int(image.shape[0]/10)
    w = int(image.shape[1]/10)
    thumbnail = resize(gray,h,w)
    print('thumbnail size {}'.format(thumbnail.shape))

    _, outs = cv2.threshold(thumbnail, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    temp = np.zeros((h+2, w+2), np.uint8)
    im_floodfill = outs.copy()
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, temp, (0,0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    mask = outs | im_floodfill_inv
    mask = cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
    mask[mask==255]=1 #binary
    # if image is too large, below code would break terminal
    mask, contours, hierarch = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 50000:
            cv2.drawContours(mask,[contours[i]],0,0,-1)
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    for label in range(1,np.max(labels)+1):
        mask = labels.copy()
        mask[labels!=label] = 0
        mask[mask!=0]=255
        
        x_min = 10*stats[label][1]
        x_max = 10*stats[label][3] + x_min
        y_min = 10*stats[label][0]
        y_max = 10*stats[label][2] + y_min

        mask = resize(mask,image.shape[0],image.shape[1])
        mask_b = mask*image[:,:,0]
        mask_b = mask_b[x_min:x_max,y_min:y_max]
        mask_g = (mask*image[:,:,1])
        mask_g = mask_g[x_min:x_max,y_min:y_max]
        mask_r = (mask*image[:,:,2])
        mask_r = mask_r[x_min:x_max,y_min:y_max]
        patch = cv2.merge([mask_b,mask_r,mask_g])

        
        savepath = os.path.join(savefolder,path.split('/')[-1].split('.')[0]+'_{}.{}'.format(label,path.split('.')[-1]))
        print("save into {}".format(savepath))
        cv2.imwrite(savepath,patch)
    return

def Segfolder(folder):
    files = os.listdir(folder)
    for file in files:
        if os.path.isfile(os.path.join(folder,file)):
            if file.endswith('.jpg') or file.endswith('.png'):
                print("Segmenting {}".format(file))
                OutsSeg(os.path.join(folder,file)) 
            else:
                continue           
        else:
            Segfolder(os.path.join(folder,file))
            break
            
    return

if __name__ == "__main__":
    Segfolder('/home/liubo/zy_bio')