from pdf2image import convert_from_path, convert_from_bytes
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

"""处理pdf文件"""
class PDF_Handler:
    @staticmethod
    def pdf2images(pdf_path, output_path):
        """
        提取pdf文件中的图片
        """
        images = convert_from_path(pdf_path, dpi=200)
        for image in images:
            if(not os.path.exists(output_path)):
                os.mkdir(output_path)
            image.save(output_path + f'\img_{images.index(image)}.png', 'PNG')

    @staticmethod
    def split_pdf(pdf_path:str, start_page:int, end_page:int, output_path:str):
        """
        将pdf文件拆分成不同的小文件
        :pdf_path 待处理的pdf文件路径
        :start_page 从第几页开始
        :end_page 从第几页结束
        :output_path 输出路径
        """
        pdf_name = pdf_path.split('\\')[-1].split('.')[0]
        out_dir = "\\".join(output_path.split('\\')[:-1]) +'\\'
        ori_pdf = PdfFileReader(open(pdf_path, 'rb'))
        output_file = PdfFileWriter()
        for i in range(start_page, end_page):
            output_file.addPage(ori_pdf.getPage(i))
        with open(output_path, 'wb') as f:
            output_file.write(f)
        return '拆分完成'

    @staticmethod
    def split_pdf_method2(pdf_path, num_file, num_page, output_dir_path):
        """
        将pdf分割为固定页数的多个文件
        :param pdf_path 源pdf路径
        :param num_file 分成几份文件
        :param output_dir_path 没份文件页数多少
        :param output_dir_path 输出目录
        """
        fname = os.path.splitext(os.path.basename(pdf_path))[0] # 文件名不含后缀
        for i in range(num_file):
            with open(pdf_path, 'rb') as open_pdf:
                pdf_reader = PdfFileReader(open_pdf)
                pdf_writer = PdfFileWriter()
                if((i+1)*num_page<= pdf_reader.numPages):
                    for page in range(i*num_page, (i+1)*num_page):
                        pdf_writer.addPage(pdf_reader.getPage(page))
                    output_filename = output_dir_path + r'\{}_{}.pdf'.format(fname, i+1)
                else:
                    for page in range(i*num_page, pdf_reader.getPage(page)):
                        pdf_writer.addPage(pdf_reader.getPage(page))
                    output_filename = output_dir_path + r'\{}_{}.pdf'.format(fname, i+1)
                with open(output_filename, 'wb') as output:
                    pdf_writer.write(output)
                    print('生成文件{}'.format(output_filename))

    @staticmethod
    def pdf_merge(merge_list, output_pdf):
        """
        pdf合并
        :param merge_list 需要合并的pdf列表
        :param output_pdf 合并之后的pdf名
        """
        output = PdfFileWriter()
        for ml in merge_list:
            pdf_input = PdfFileReader(open(ml, 'rb'))
            page_count = pdf_input.getNumPages()
            for i in range(page_count):
                output.addPage(pdf_input.getPage(i))
        output.write(open(output_pdf, 'wb'))