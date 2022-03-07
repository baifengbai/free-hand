import cv2, os
import numpy as np
from utils.common import Controler_Img
from utils.common import ControlerDir

'''
    水印识别的类
    识别图片中是否含有指定的模板
'''

class Base_Maskcheck(Controler_Img):
    @staticmethod
    def method1_cv_reconize(img_gray, template):
        """模板匹配方法1"""
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)   # Perform match operations.
        return res

    @staticmethod
    def method2_cv_reconize(img_gray, template):
        """模板匹配方法2"""
        pass

    @staticmethod
    def identifyMask_single_img(img_target_path, imgs_template_path, threshold=0.38):
        '''
        单张图片水印识别
        :param img_target_path: 目标图片绝对路径
        :param img_template_path: 模板图片目录绝对路径 需以\\结尾
        :param threshold: Specify a threshold 0.35本来挺好的
        '''
        # 获取模板目录路径下所有模板绝对
        imgs_templateNameList = os.listdir(imgs_template_path)
        imgs_template_path_list = []
        for templateName in imgs_templateNameList:
            imgs_template_path_list.append(imgs_template_path + templateName)

        # 读取目标图片
        img_target_rgb = cv2.imdecode(np.fromfile(img_target_path, dtype=np.uint8), -1)  # Read the main image

        try:
            img_target_gray = cv2.cvtColor(img_target_rgb, cv2.COLOR_BGR2GRAY)  # Convert it to grayscale
        except Exception as e:
            print('图片转换为灰度失败，请查看原图是否是灰度图片，本功能不应用于灰度图片')
            return {
                "hasWaterMask" : False
            }

        for img_template_path in imgs_template_path_list:
            img_template = cv2.imread(img_template_path, 0)  # Read the template
            w, h = img_template.shape[::-1]  # Store width and heigth of template in w and h

            res = Base_Maskcheck.method1_cv_reconize(img_target_gray, img_template)
            loc = np.where(res >= threshold)  # Store the coordinates of matched area in a numpy array
            x = loc[0]
            y = loc[1]

            # Draw a rectangle around the matched region.
            if (len(x) and len(y)):
                for pt in zip(*loc[::-1]):
                    # pt[0]表示水印位置所在的像素高度
                    cv2.rectangle(img_target_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
                    # Show the final image with the matched area.
                    cv2.imwrite("E:\imgs\\toutiao_thumbnail_0to4999_maskreconizeres\\test_001.png", img_target_rgb)
                    waterMaskLocY = pt[1]
                print("发现水印: ", img_target_path, "水印位置： x= ", x, " y= ", y, "对应模板：", img_template_path)
                return {
                    "hasWaterMask" : True,
                    "waterMaskLocY": waterMaskLocY      # 水印位置的y坐标
                }
            else:
                # print('该图片匹配此模板：', img_template_path)
                continue
        print("匹配不到符合当前模板目录下图片模板的水印")
        return {
            "hasWaterMask" : False
       }

    @staticmethod
    def identifyMask_imgs_dir(imgs_dirpath, templates_dirpath, dirpath_hasmask, dirpath_donthasmask):
        '''
            对指定目录下的所有图片进行水印识别处理
        :param imgs_dirpath: 目录绝对路径 最后必须加上\\
        :param templates_dirpath: 模板图片目录的绝对路径 最后必须加上\\
        :param dirpath_hasmask  存放含有水印的图片的目录路径  最后必须加上\\
        :param dirpath_donthasmask  存放无水印的图片的目录路径   最后必须加上\\
        '''
        imgName_list = os.listdir(imgs_dirpath)
        print('待处理图片总数量： ', len(imgName_list))
        hasmask_imgName_list = []
        donthasmask_imgName_list = []
        for imgName in imgName_list:
            imgpath = imgs_dirpath + imgName
            res = Base_Maskcheck.identifyMask_single_img(imgpath, templates_dirpath)
            if(res['hasWaterMask']):
                # 匹配到模板
                hasmask_imgName_list.append(imgName)
                img_hasmask_dst = dirpath_hasmask + imgName
                # 复制到对应目录下
                ControlerDir.Controler_Dir.copyFile(src=imgpath, dst=img_hasmask_dst)
                # 根据水印位置的裁切 对新目录下的水印图片裁切
                waterMaskY = res["waterMaskLocY"]
                imgHeight = Controler_Img.get_imgHeight(imgpath)
                cutBottomHeight = imgHeight - waterMaskY
                Controler_Img.cutting_single_img(img_path=img_hasmask_dst, cutBottomHeight=cutBottomHeight)
            else:
                # 匹配不到模板
                donthasmask_imgName_list.append(imgName)
                img_donthasmask_dst = dirpath_donthasmask + imgName
                # 复制到对应目录下
                ControlerDir.Controler_Dir.copyFile(src=imgpath, dst=img_donthasmask_dst)


