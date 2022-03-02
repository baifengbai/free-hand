import requests

"""
    下载相关的基类和方法
"""

# 下载类
class BaseDownloader:
    # 已有图片链接下载图片的方法
    @staticmethod
    def download_img(urlpath, imgname, dstDirPath):
        '''
        图片下载
        :param urlpath: 可下载的图片资源链接
        :param imgname: 保存图片为指定名字
        :param dstDirPath: 图片保存目录位置，注意：最后要有\\
        :return:
        '''
        r = requests.get(urlpath)
        img = r.content  # 响应的二进制文件
        with open(dstDirPath + str(imgname) + '.png', 'wb') as f:  # 二进制写入
            f.write(img)

    # 下载视频
    @staticmethod
    def downVideo(urlpath, name, dstDirPath, *headers_):
        print("正在下载： ", urlpath)
        if(headers_!=[]):
            r = requests.get(urlpath, verify=False, headers=headers_, timeout=30)
        else:
            r = requests.get(urlpath, verify=False, timeout=30)
        video = r.content  # 响应的二进制文件
        with open(dstDirPath + str(name) + '.mp4', 'wb') as f:  # 二进制写入
            f.write(video)
        r.close()  # 关闭很重要，确保不要过多的连接

