# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image
import io
import base64
import re
class Image_Dispose:
    def __init__(self):
        pass

    def imgBackgroundPadding(self, img):
        """
        填充图片的透明背景
        :param img:
        :return:
        """

        # StringIO(base64.b64decode(base64_string_here))
        im = Image.open(io.BytesIO(img))
        # im = im.resize((40, 40),Image.ANTIALIAS)
        x, y = im.size
        try:
            # 使用白色来填充背景 from：www.outofmemory.cn
            # (alpha band as paste mask).
            p = Image.new('RGBA', im.size, (240, 240, 240))
            p.paste(im, (0, 0, x, y), im)
        except:
            return img
        buffer = io.BytesIO()
        p.save(buffer, format='PNG')
        imageBuffer = buffer.getvalue()
        stringFile = base64.b64encode(imageBuffer).decode("utf-8")
        base64Data = re.sub('^data:image/.+;base64,', '', stringFile)
        byteData = base64.b64decode(base64Data)
        return byteData


    def reClip(self,img,p,f):

        big_image = Image.open(io.BytesIO(img))
        # 将要裁剪的图片块距原图左边界距左边距离，上边界距上边距离，右边界距左边距离，下边界距上边的距离。

        region = big_image.crop(p)  ## 0,0表示要裁剪的位置的左上角坐标，50,50表示右下角。
        # region.save(f + '.PNG')  ## 将裁剪下来的图片保存到 举例.png
        # return region
        buffer = io.BytesIO()
        region.save(buffer, format='PNG')
        imageBuffer = buffer.getvalue()
        stringFile = base64.b64encode(imageBuffer).decode("utf-8")
        base64Data = re.sub('^data:image/.+;base64,', '', stringFile)
        byteData = base64.b64decode(base64Data)
        return byteData

    def imgBinarizationProcessing(self, img):
        """
        图片二值化处理
        :param img:
        :return:
        """
        img = Image.open(io.BytesIO(img))
        Img = img.convert('L')
        # 自定义灰度界限，大于这个值为白色，小于这个值为黑色
        threshold = 250
        table = []
        for i in range(256):
            if i < threshold:
                table.append(1)
            else:
                table.append(0)
        # 图片二值化
        photo = Img.point(table, '1')
        buffer = io.BytesIO()
        photo.save(buffer, format='PNG')
        imageBuffer = buffer.getvalue()
        stringFile = base64.b64encode(imageBuffer).decode("utf-8")
        base64Data = re.sub('^data:image/.+;base64,', '', stringFile)
        byteData = base64.b64decode(base64Data)
        return byteData
if __name__ == '__main__':
    Image_Dispose()