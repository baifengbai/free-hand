'''
    此处处理上传缩略图--今日头条
'''
from basement__ import ContralerDatabase, Download
from customFunction__.imgref import classifier, processing
from customFunction__.imgref import maskcheck
from customFunction__.Poster import poster_img
from customFunction__.imgref import processing

from customFunction__.Poster import poster_img

# config = {
#     'template_dirpath': 'E:\\Projects\\auto_datahandler\\resource\\mask_templates\\toutiao_templates\\',
#     'thumbnail_dirpath': 'E:\\imgs\\toutiao_thumbnail_0to4999\\',
#     'thumbnail_dirpath_reconized': 'E:\\imgs\\toutiao_thumbnail_0to4999_reconized\\',
#     'thumbnail_dirpath_hasmask': 'E:\\imgs\\toutiao_thumbnail_0to4999_hasmask\\',
#     'thumbnail_dirpath_donthasmask': 'E:\\imgs\\toutiao_thumbnail_0to4999_donthasmask\\',
#     'thumbnail_dirpath_maskreconizeres': 'E:\\imgs\\toutiao_thumbnail_0to4999_maskreconizeres',# 水印识别结果
#     'thumbnail_dirpath_tobeposted': 'E:\\imgs\\toutiao_thumbnail_0to4999_tobeposted\\', # 待上传的图
#
#     'contentimg_dirpath': 'E:\\imgs\\toutiao_contentimg_5000toend\\',
#     'contentimg_dirpath_reconized': 'E:\\imgs\\toutiao_contentimg_5000toend_reconized\\',
#     'contentimg_dirpath_hasmask': 'E:\\imgs\\toutiao_contentimg_dirpath_hasmask\\',
#     'contentimg_dirpath_donthasmask': 'E:\\imgs\\toutiao_contentimg_dirpath_donthasmask\\',
#     'contentimg_dirpath_maskreconizeres': 'E:\\imgs\\toutiao_contentimg_5000toend_maskreconizeres'
# }

config = {
    'template_dirpath': 'E:\\Projects\\auto_datahandler\\resource\\mask_templates\\toutiao_templates\\',
    'thumbnail_dirpath': 'E:\\toutiao\\origin\\',
    'thumbnail_dirpath_reconized': 'E:\\toutiao\\reconized\\',
    'thumbnail_dirpath_hasmask': 'E:\\toutiao\\hasmask\\',
    'thumbnail_dirpath_donthasmask': 'E:\\toutiao\\donthasmask\\',
    'thumbnail_dirpath_maskreconizeres': 'E:\\toutiao\\maskreconizeres',# 水印识别结果
    'thumbnail_dirpath_tobeposted': 'E:\\toutiao\\tobeposted\\', # 待上传的图
}

class Tools:
    contraler_db = ContralerDatabase.Contraler_Database('imgsdatabase')
    downloader = Download.Downloader()
    imgclassifier_thumbnail = classifier.ImgsClassifier(crawledDirPath=config['thumbnail_dirpath'], savedDirPath=config['thumbnail_dirpath_reconized'])
    # imgclassifier_contentimg = classifier.ImgsClassifier(crawledDirPath=config['contentimg_dirpath'], savedDirPath=config['contentimg_dirpath_reconized'])
    maskchecker = maskcheck.Base_Maskcheck()


tableName = 'tb_contentimg_toutiao'
toutiao_imgurl_list = Tools.contraler_db.getAllDataFromDB('select `origin_pic_path` from `{}`;'.format(tableName))
print(tableName, ' 数据总数目： ', len(toutiao_imgurl_list))




print('------------------ 处理今日头条图片（前5k张）传至缩略图 -------------------------')
thumbnail_toutiao_0to4999_list = toutiao_imgurl_list[0:5000]
print("缩略图_头条_数目： ", len(thumbnail_toutiao_0to4999_list))
print('读取 例子 ', toutiao_imgurl_list[0])
# print("1 下载图片到目录")
# for i, url in enumerate(thumbnail_toutiao_0to4999_list):
#     try:
#         Tools.downloader.download_img(url[0], i, config['thumbnail_dirpath'])
#     except Exception as e:
#         print(i, ' ', url)
# 图片下载已经完成，人工筛选 可上传的占比约一半
# print('2 图片识别-命名')
# Tools.imgclassifier_thumbnail.run()

# print('3 水印识别及处理')
# Tools.maskchecker.identifyMask_imgs_dir(imgs_dirpath=config['thumbnail_dirpath_reconized'], templates_dirpath=config['template_dirpath'], dirpath_hasmask=config['thumbnail_dirpath_hasmask'], dirpath_donthasmask=config['thumbnail_dirpath_donthasmask'])

# print('4 将图片整成缩略图')
# processer0 = processing.Imgs2ThumbnailByDir(thumbnailOriDirPath=config['thumbnail_dirpath_donthasmask'],thumbnailDstDirPath=config['thumbnail_dirpath_tobeposted'])
# processer0.cutOff2ThumbnailByDir()

# print('5 上传无水印的缩略图')
# poster = poster_img.Poster_Imgs(imgDirPath=config['thumbnail_dirpath_tobeposted'])
# poster.updateImgsThumbnail()

print('------------------ 处理今日头条图片（5k张之后的）传至内容图 -------------------------')
# contentimg_toutiao_5000toend_list = toutiao_imgurl_list[5000:]
# print("内容图_头条_数目： ", len(contentimg_toutiao_5000toend_list))
# print("1 下载图片到目录")
# for i, url in enumerate(contentimg_toutiao_5000toend_list):
#     try:
#         Tools.downloader.download_img(url[0], i, config['contentimg_dirpath'])
#     except Exception as e:
#         print(i, ' ', url)
# 图片下载已经完成，人工筛选 可上传的占比约一半
# print('2 图片识别-命名')
# Tools.imgclassifier_contentimg.run()

# print('3 水印识别及处理')
# Tools.maskchecker.identifyMask_imgs_dir(imgs_dirpath=config['contentimg_dirpath_reconized'], templates_dirpath=config['template_dirpath'], dirpath_hasmask=config['contentimg_dirpath_hasmask'], dirpath_donthasmask=config['contentimg_dirpath_donthasmask'])

# step1
# print('4 resize内容图 图片 默认为宽度小1000')
# imgSetSizer = processing.ImgsSetSize(imgsOriDirPath=config['contentimg_dirpath_hasmask'])
# imgSetSizer.resize_byDir()

# print('5 上传无水印的内容图')
# poster = poster_img.Poster_Imgs(imgDirPath=config['contentimg_dirpath_hasmask'])
# poster.updateImgs()

# step2
# print('4 resize内容图 图片 默认为宽度小1000')
# imgSetSizer = processing.ImgsSetSize(imgsOriDirPath=config['contentimg_dirpath_donthasmask'])
# imgSetSizer.resize_byDir()

# print('5 上传无水印的内容图')
# poster = poster_img.Poster_Imgs(imgDirPath=config['contentimg_dirpath_donthasmask'])
# poster.updateImgs()
