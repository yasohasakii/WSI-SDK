# WSI-SDK
WSI(Whole slide image)-SDK 顾名思义,先挖个坑以后再填。

## Install on Linux（2019/7/2）
Please see the `requirements.txt`

## Introduction（2019/7/4）
先做一个简单的科普。
WSI常作为医疗病理切片图像的保存载体，通常大小在几百MB到十几GB不等。WSI保存的是一个不同尺度下的图像序列，可以理解为用不同放大倍数的显微镜扫描了同时刻下的同一目标，可以理解成Fig 1所示的金字塔结构。

<div align=center><img width = '600' height ='400' src ="https://github.com/caibojun/WSI-SDK/blob/master/svs_pyramid.png"/></div>
<center >**Fig 1.Pyramid sampling**</center >

由于设备厂商不同，WSI存在多种格式，常见的SVS和TIF为[Aperio](http://www.aperio.com/documents/api/Aperio_Digital_Slides_and_Third-party_data_interchange.pdf)的格式，另外本项目还涉及一种KFB格式是由[江丰生物](http://www.kfbio.cn/)的设备封装的私有格式。
