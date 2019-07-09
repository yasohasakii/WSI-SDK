# WSI-SDK
WSI(Whole slide image)-SDK on Linux 顾名思义,先挖个坑以后再填。

## Content
* [Introduction](#introduction)
* [Install on Linux](#Install_on_Linux)
* [Preprocess](#Preprocess)


## Introduction（2019/7/4）
&#160; &#160; &#160; &#160;先做一个简单的科普。
WSI常作为医疗病理切片图像的保存载体，通常大小在几百MB到十几GB不等。WSI保存的是一个不同尺度下的图像序列，可以理解为用不同放大倍数的显微镜扫描了同时刻下的同一目标，更加直观的可根据下图所示的金字塔结构来理解。  
<div align=center><img width = '600' height ='400' src ="https://github.com/caibojun/WSI-SDK/blob/master/image/svs_pyramid.png"/></div>

&#160; &#160; &#160; &#160;由于设备厂商不同，WSI存在多种格式，常见的SVS和TIF为 [Aperio](http://www.aperio.com/documents/api/Aperio_Digital_Slides_and_Third-party_data_interchange.pdf)的格式，另外本项目还涉及一种KFB格式是由[江丰生物](http://www.kfbio.cn/)的扫描设备生成的私有格式。本项目处理的主要就是svs和kfb格式的数据。  
&#160; &#160; &#160; &#160;在进行读取的过程中，主要用到的是Openslide库，我把Openslide的python库都封装在一起，为了较为规范的读取数据，wsi图像被分为header和image两个部分。header中包含wsi的层次结构、尺度以及标签等信息，image为最大分辨率图像，也就是level0图像。一般level0的图像会非常大，尺度常在10000\*10000像素以上，超过65000像素的图像，就无法用OpenCV导出为jpg格式了，同理[Pillow](https://github.com/python-pillow/Pillow/blob/master/docs/reference/limits.rst)也是没有办法处理的，而png与tiff格式则没有这一限制。  
&#160; &#160; &#160; &#160;为了直观的查看图像，可以通过特定的查看器如[Image Scope](https://www.leicabiosystems.com/digital-pathology/manage/aperio-imagescope/), kfb格式可以通过KViewer打开。 

## Install on Linux（2019/7/2）
Please see the `requirements.txt`

## Preprocess (2019/7/9)
### Read SVS/TIFF File
