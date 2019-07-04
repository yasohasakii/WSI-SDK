import kfbread
import os
import cv2

def read_folder(dirname):
    kfb_files = os.listdir(dirname)
    for kfb in kfb_files:
        if os.path.isdir(kfb):
            read_folder(kfb)
            if kfb.endswith('kfb'):
                kfb_path = os.path.join(dirname,kfb)
                savepath = kfb_path.split('.kfb')[0] + '.jpg'
                print("Reading {}".format(kfb))
                header, image = kfbread.kfbread(kfb_path)
                for key in header.keys():
                    endwith = '_'+key+'.jpg'
                    cv2.imwrite(savepath.replace('.jpg',endwith),header[key])
                cv2.imwrite(savepath,image)


# if __name__ == "__main__":
#     read_folder("/home/liubo/zy_bio/CD")