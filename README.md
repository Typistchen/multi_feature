# Multi_feature Detect
## 1、项目说明：
该项目包括了PyQt5图形界面，面部检测，面部识别，手势检测，手势识别五个功能
其中
1、面部检测采用Opencv方案，利用opencv自带的API进行面部检测
2、面部识别采用谷歌的FaceNet方案，搭建了相关的网络
3、手势检测采用了Yolo_v5方案，自行收集了数据集，进行了训练
4、手势识别采用Resnet18方案，自行搭建了网络，并进行了训练
## 2、文件说明：
### 2.1、文件结构：
-----pyqt5
|----face_detect
|----face_recognitze
|----hand_detect
|----hand_recognize
|----PYQT5.py
### 2.2、文件使用说明：
1、运行该系统PYQT5即可进行运行

note：需要进行修改的：
①face_detect：两个图片的地址，与opencv的权重地址
②face_recognize：两个图片的地址
③hand_detect：权重与图片的地址
④hand_recognize：权重和两个图片的地址

2、运行界面说明

运行PYQT5后，点击打开摄像-->拍照-->检测 ，后续即可显示下方的检测结果
详见example.jpg
### 2.3、数据集说明
1、手势检测数据集采用coco-hand、tv-hand以及部分自行拍摄的照片
2、手势识别的数据集采用学长给的数据集，也可以自行处理

