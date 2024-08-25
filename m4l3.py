import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout,
                             QVBoxLayout)

from PyQt5.QtCore import Qt

from PIL import Image, ImageEnhance, ImageFilter

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Doanh-Image Editor')
############################################
button_folder = QPushButton('Folder')
button_left = QPushButton('Left')
button_right = QPushButton('Right')
button_mirror = QPushButton('Mirror')
button_sharpness = QPushButton('Sharpness')
button_bw = QPushButton('B/W')
button_blur = QPushButton("Blur")
###############################################
label_image = QLabel('Image')
list_widget_files = QListWidget()
##############################################
layout_Hbutton = QHBoxLayout()
layout_Hbutton.addWidget(button_left)
layout_Hbutton.addWidget(button_right)
layout_Hbutton.addWidget(button_mirror)
layout_Hbutton.addWidget(button_sharpness)
layout_Hbutton.addWidget(button_bw)
layout_Hbutton.addWidget(button_blur)
#############################################
layout_v_fol_list = QVBoxLayout()
layout_v_fol_list.addWidget(button_folder)
layout_v_fol_list.addWidget(list_widget_files)
###################################################
layout_v_img_button = QVBoxLayout()
layout_v_img_button.addWidget(label_image,95)
layout_v_img_button.addLayout(layout_Hbutton)
#################################################
layout_main = QHBoxLayout()
layout_main.addLayout(layout_v_fol_list,20)
layout_main.addLayout(layout_v_img_button,80)
##################################################
win.setLayout(layout_main)
win.show()
##################################
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.file_name = None
        self.save_dir = "Modified/"
    def loadImage(self,dir,file_name):
        self.dir = dir
        self.file_name = file_name
        img_path = os.path.join(dir,file_name)
        self.image = Image.open(img_path)
    def showImage(self,path):
        label_image.hide()
        pixel_image = QPixmap(path)
        w = label_image.width()
        h = label_image.height()
        pixel_image = pixel_image.scaled(w,h, Qt.KeepAspectRatio)
        label_image.setPixmap(pixel_image)
        label_image.show()
        
    def saveImage(self):
        path = os.path.join(work_dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path,self.file_name)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(work_dir,self.save_dir,self.file_name)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)

    def do_sharpness(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)


#########################################################################
def showSelectedImage():
    if list_widget_files.currentRow() >= 0:
        file_name = list_widget_files.currentItem().text()
        work_image.loadImage(work_dir,file_name)
        image_path = os.path.join(work_image.dir,work_image.file_name)
        work_image.showImage(image_path)
##########################################################################
def selectedWorkDir():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
##################################################
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
##################################################
def showFileNamesList():
    extension = ['.jpg','.jpeg','.png','.gif']
    selectedWorkDir()
    list_widget_files.clear()
    files = filter(os.listdir(work_dir),extension)
    for file in files:
        list_widget_files.addItem(file)
##################################################
work_dir = ""
work_image = ImageProcessor()
list_widget_files.currentRowChanged.connect(showSelectedImage)
##################################################################
button_folder.clicked.connect(showFileNamesList)
button_bw.clicked.connect(work_image.do_bw)
button_left.clicked.connect(work_image.do_left)
button_right.clicked.connect(work_image.do_right)
button_mirror.clicked.connect(work_image.do_mirror)
button_sharpness.clicked.connect(work_image.do_sharpness)
button_blur.clicked.connect(work_image.do_blur)
















##################################################
app.exec()
