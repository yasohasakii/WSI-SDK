# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from scipy import misc

def ROI_extract(image):
    def resize(src_image,h,w):
        H, W =src_image.shape[:2]
        if src_image.ndim==3:
            dst_image = np.zeros([h,w,3],np.uint8)
        else:
            dst_image = np.zeros([h,w],np.uint8)
        if max(H/2,W/2,h/2,w/2)>20000:
            dst_image[:h/2,:w/2] = resize(src_image[:H/2,:W/2],(h/2,w/2))
            dst_image[h/2:,:w/2] = resize(src_image[H/2:,:W/2],(h-h/2,w/2))
            dst_image[:h/2,w/2:] = resize(src_image[:H/2,W/2:],(h/2,w-w/2))
            dst_image[h/2:,w/2:] = resize(src_image[H/2:,W/2:],(h-h/2,w-w/2))
        else:
            dst_image[:h/2,:w/2] = misc.imresize(src_image[:H/2,:W/2],(h/2,w/2),'nearest')
            dst_image[h/2:,:w/2] = misc.imresize(src_image[H/2:,:W/2],(h-h/2,w/2),'nearest')
            dst_image[:h/2,w/2:] = misc.imresize(src_image[:H/2,W/2:],(h/2,w-w/2),'nearest')
            dst_image[h/2:,w/2:] = misc.imresize(src_image[H/2:,W/2:],(h-h/2,w-w/2),'nearest')
        return dst_image

    gray = 255 - cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
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
    mask[mask != 0] = 1
    dilation = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    # if image is too large, below code would break terminal
    mask, contours, hierarch = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 2700:
            cv2.drawContours(mask,[contours[i]],0,0,-1)
        else:
            cv2.fillPoly(mask,[contours[i]],255)
    
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    roi_list = []
    for label in range(1,np.max(labels)+1):
        mask = labels.copy()
        mask[mask!=label] = 0

        x_min = 10*stats[label][1]
        x_max = 10*stats[label][3] + x_min
        y_min = 10*stats[label][0]
        y_max = 10*stats[label][2] + y_min

        mask = resize(mask,image.shape[0],image.shape[1])
        mask_rgb = cv2.merge([mask,mask,mask])
        mask_rgb[mask_rgb!=0]=1
        mask_rgb = mask_rgb*image
        patch = mask_rgb[x_min:x_max,y_min:y_max,:]
        roi_list.append(patch)
    return roi_list

def ROI_folder(src_folder,dst_folder):
	if not os.path.isdir(dst_folder):
		os.mkdir(dst_folder)
    files = os.listdir(src_folder)
    for file in files:
        filepath = os.path.join(src_folder,file)
        if os.path.isfile(filepath):
            if file.endswith('.jpg') or file.endswith('.png'):	
                print("Segmenting {}".format(filepath))
                image = cv2.imread(filepath)
                roi_list = ROI_extract(image)
                for index,patch in enumerate(roi_list): 
                    patch_path = os.path.join(dst_folder,filepath.split('/')[-1].split('.')[0]+'_{}.{}'.format(index,filepath.split('.')[-1]))
                    print("save into {}".format(patchpath))
                    cv2.imwrite(patch_path,patch)
            else:
                continue           
        else:
        	# folder, recursion
            ROI_folder(os.path.join(src_folder,file),dst_folder)            
    return

# if __name__ == "__main__":
#     ROI_folder('/home/liubo/zy_bio')
