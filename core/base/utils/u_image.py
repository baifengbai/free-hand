import base64
import io
import os.path

from PIL import Image, ImageFile

"""针对图片的处理"""
class Compress_Picture:
    def __init__(self):
        # 图片格式
        self.file = '.JPG'

    def compress_img_method1(self, img_path, img_save_path, multiple=2):
        """
        压缩图像大小 压缩后的质量比method2好
        :param img_path 原图路径
        :param img_save_path 保存路径
        :param multiple 压缩比例 默认1/2 即2
        """
        s_img = Image.open(img_path)
        w, h = s_img.size
        d_img = s_img.resize((int(w/multiple), int(h/multiple)), Image.ANTIALIAS) # 设置压缩此存和大小
        d_img.save(img_save_path)

    def get_size(self, img_path):
        """获取文件大小 KB"""
        size = os.path.getsize(img_path)
        return size/1024

    def compress_img_method2(self, img_path, out_path, mb=50, step=5, quality=100):
        """
        不改变图像尺寸压缩图像大小 通过Image.open.save函数调整图像质量，达到降低存储大小目的。
        特别注意： 本方法只适用于保存为JPG/JPEG格式的图片的情况
        :param img_path 图像地址
        :param out_path 输出地址
        :param mb 压缩目标 KB
        :param step 每次调整的压缩比率
        :param quality 初始压缩比率
            保存图像的质量，值的范围从1（最差）到95（最佳）。 默认值为75，使用中应尽量避免高于95的值; 100会禁用部分JPEG压缩算法，并导致大文件图像质量几乎没有任何增益。
        """
        o_size = self.get_size(img_path)
        if(o_size<mb):
            return 'img大小小于设定的mb，无需压缩大小'
        while(o_size>mb):
            s_img = Image.open(img_path)
            s_img = s_img.convert('RGB')
            s_img.save(out_path, quality=quality)
            if(quality-step<0):
                break
            quality = quality - step
            o_size = self.get_size(out_path)

    def compress_img_method3(self, img_path, output_path,mb=600, quality=85, k=0.9):
        """
        不改变图片尺寸压缩到指定大小
        :param img_path
        :param mb 压缩目标 KB
        :param quality 初始压缩比率
        :return: 压缩文件地址
        """
        img_size = self.get_size(img_path)
        if(img_size<=mb):
            return 'img大小小于设定的mb，无需压缩大小'
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        output_size = img_size
        while(output_size>mb):
            img = Image.open(img_path)
            x, y = img.size
            output_img = img.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
            try:
                output_img.save(output_path,quality=quality)
            except Exception as e:
                print(e)
                break
            output_size = os.path.getsize(output_path)
        return output_path

    def compress_img_bs4(self, b64, mb=190, k=0.9):
        """不改变尺寸压缩base64图片"""
        f = base64.b64decode(b64)
        with io.BytesIO(f) as im:
            o_size = len(im.getvalue())
            if(o_size<=mb):
                return b64
            im_out = im
            while(o_size>mb):
                img = Image.open(im_out)
                x,y = img.size
                out = img.resize((int(x*k), int(y*k)), Image.ANTIALIAS)
                im_out.close()
                im_out = io.BytesIO()
                out.save(im_out, 'jpeg')
                o_size = len(im_out.getvalue())
            b64 = base64.b64encode(im_out.getvalue())
            im_out.close()
        return str(b64, encoding='utf-8')

    def compress_imgs_fromdir(self, dir_origin, dir_dst):
        """
        将目录下所有的图片压缩放在目标目录下
        """
        img_name_lis = os.listdir(dir_origin)
        for img_name in img_name_lis:
            img_path = dir_origin + '\\' + img_name
            img_dst_path = dir_dst + '\\' + img_name
            self.compress_img_method1(img_path=img_path, img_save_path=img_dst_path)


