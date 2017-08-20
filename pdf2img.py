import os
from PyPDF2 import PdfFileReader
from wand.image import Image

WIDTH = 2048
QUALITY = 400

def pdf2img(file_path, images_path):
    width = WIDTH
    pdf = PdfFileReader(file_path)
    pages_number = pdf.getNumPages()
    for index in range(pages_number):
        image_file = ''.join([file_path, '[{}]'.format(index)])
        # width: the width of target image;  resolution: different quality or image (input intager)
        with Image(filename=image_file, width=width, resolution=QUALITY) as img:
            target = '{}/{}.jpg'.format(images_path, str(index))
            if not os.path.isdir(os.path.dirname(target)):
                os.mkdir(os.path.dirname(target))
            img.save(filename=target)



if __name__ == '__main__':
    pdf = 'test.pdf'
    path = '/home/ubuntu/image.jpg'   
    pdf2img(pdf, path)