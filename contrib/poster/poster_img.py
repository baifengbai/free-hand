from core.base.poster.base import BasePoster_Img
import os

"""使用方法：
调用Poster_Imgs_Thumbnails/Poster_Imgs_Contentimgs类创建对象，
对象.postauto(task_type)即可
注意： imgDirPath所在目录的图片必须为处理完成可以直接上传的目录
"""
class Poster_Imgs_Base(BasePoster_Img):
    '''Post 图片的基类'''
    def __init__(self, uri, imgDirPath):
        '''
        :param imgDirPath  处理完的图片目录路径dir   注意这里的路径最后加\\的
        '''
        BasePoster_Img.__init__(self, uri=uri, imgs_dir_path=imgDirPath)
        self.imgDirPath = imgDirPath
        if(not self.imgDirPath==''):
            self.imgNameList = self.get_imgPathList()
        else:
            self.imgNameList = None

            # 获取目录下所有文件的路径列表
    def get_imgPathList(self):
        imgNameList = os.listdir(self.imgDirPath)  # 获取目录下的所有文件名
        imgPathList = []
        for imgName in imgNameList:
            item = self.imgDirPath + '\\' + imgName
            imgPathList.append(item)
        return imgNameList



class Poster_Imgs_Thumbnails(Poster_Imgs_Base):
    """上传内容图"""
    def __init__(self, imgDirPath, uri='http://121.40.187.51:8088/api/contentimgs_api'):
        Poster_Imgs_Base.__init__(self, uri=uri, imgDirPath=imgDirPath)


class Poster_Imgs_Contentimgs(Poster_Imgs_Base):
    """上传缩略图"""
    def __init__(self, imgDirPath, uri='http://121.40.187.51:8088/api/thumbnail_api'):
        Poster_Imgs_Base.__init__(self, uri=uri, imgDirPath=imgDirPath)

