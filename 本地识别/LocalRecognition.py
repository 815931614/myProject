# -*- coding: UTF-8 -*-
import ddddocr
import cv2
from Image_Dispose import Image_Dispose
import time
import pytesseract
import base64
class LocalRecognition:
    """
       本地识别
    """


    def __init__(self):

        self.image_Dispose = Image_Dispose()

    def sliding_block(self,target,background):
        """
        滑块识别
        :param img:
        :return:
        """

        pass

    def figure_letter(self,img):
        """
        数字加字母识别
        :param img:
        :return:
        """

        pass




    def hanzi(self, BigImg):
        """
        中文汉字识别
        :param img:
        :return:
        """
        ocr = ddddocr.DdddOcr(old=False)  # 文字识别


        key = ocr.classification(BigImg)



        return key





    def figure_letter_location(self,img):
        """
        数字加字母识别(含位置)
        :param img:
        :return:
        """

        pass




    def hanzi_location(self, BigImg, keyStr=None, keyImg = None):
        """
        中文汉字识别(含位置)
        :param img:
        :return:
        """
        #
        # BigImg = self.image_Dispose.imgBinarizationProcessing(BigImg)  # 图片二值化处理
        # with open('2.jpg','wb') as f:
        #     f.write(BigImg)

        det = ddddocr.DdddOcr(det=True)  # 文字定位

        ocr = ddddocr.DdddOcr(old=False)  # 文字识别

        poses = det.detection(BigImg)
        # print(poses)



        # 记录无法识别的文字坐标
        errorKey = []

        words = ""

        result = {
            'words_result': []
        }

        for box in range(len(poses)):

            x1, y1, x2, y2 = poses[box]
            centerX = x1 + int((x2 - x1) / 2)
            centerY = y1 + int((y2 - y1) / 2)


            # 对单个文字进行裁剪
            key = ocr.classification(
                self.image_Dispose.reClip(BigImg, (x1, y1 - 7, x2 + 7, y2 + 7), str(int(time.time() * 1000))))
            if not key:
                errorKey.append({
                    'word': key,
                    'position': (centerX, centerY)
                })
            else:
                words += key
                result['words_result'].append({
                    'word': key,
                    'position': (centerX, centerY)
                })



        # 未传入key直接返回识别结果
        if not keyStr and not keyImg:
            result['errorCount'] = len(errorKey)
            result['msg'] = "ok"
            return result

        # key的格式为img，则进行识别转为字符串
        if keyImg:
            keyStr = self.hanzi(keyImg)

        result['msg'] = f"识别失败keys:{keyStr},words:{words};"
        result['keys'] = keyStr
        result['words'] = words
        # errorWordNotInKeys = []
        #
        # # 校验识别的结果是否在keys中
        # for k in keyStr:
        #     if k not in words:
        #         errorWordNotInKeys.append(k)



        # # 如果缺少的字符大于1，或者缺少1个字符但没有识别到该字符的坐标或错误的坐标大于一，则识别失败
        # if len(errorWordNotInKeys) > 1 or (len(errorWordNotInKeys) == 1 and len(errorKey) != 1):
        #     return result
        #
        #
        # # 验证keys的长度，是否与识别结果的长度一直
        # kw_length = len(keyStr) - len(words)
        #
        #
        # # 如果长度差超过2，则识别失败
        # if   -1  >= kw_length >= 1 and len(errorWordNotInKeys) != 0:
        #     return result
        #
        #
        #
        #
        # # 如果识别缺少的字符等于1，并且keys与words的长度差等于正1，则进行补齐。
        # if kw_length  == 1 and len(errorWordNotInKeys) == 1:
        #     for k in keyStr:
        #         if k not in words:
        #             errorKey[0]['word'] = k
        #             result['words_result'].append(errorKey[0])

        resultlist = []
        for k in keyStr:
            for r in result['words_result']:
                if k == r['word']:
                    resultlist.append(r)

        result['msg'] = "ok"
        result['words_result'] = resultlist
        if len(resultlist) != len(keyStr):
            result['msg'] = "识别失败"





        # print(str(result))
        return result
        # cv2.imwrite("152836.jpg", im)

        # res = self.ocr.classification(img)

        # return res


    
    
if __name__ == '__main__':
    ocr = LocalRecognition()

    # with open('./keys.jpg','rb') as r:
    #    keysImg = r.read()

    from io import BytesIO
    import requests
    import base64
    import re
    s = 0
    for i in range(1,101):

        res = requests.post("https://www.avapunk.com/api/captcha/get",headers={
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '103',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'www.avapunk.com',
            'Origin': 'https://www.avapunk.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.avapunk.com/home',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',

        },json={"captchaType":"clickWord","clientUid":"point-6f75ccd9-5a1b-4fce-b5f7-40dad658887e","ts":1656242061659}).json()





        # with open('./dfd.jpg','rb') as r:
        #    bigimg = r.read()



        bigimg = base64.b64decode(res['repData']['originalImageBase64'])
        keyStr = "".join(res['repData']['wordList'])
        numl = '①②③④⑤⑥⑦⑧⑨⑩'
        plist = ocr.hanzi_location(bigimg,keyStr=keyStr)

        if plist['msg'] == 'ok':
            s += 1
            print(s)
        print(plist)
        from PIL import ImageFont, ImageDraw, Image

        img1 = Image.open(BytesIO(bigimg))
        draw = ImageDraw.Draw(img1)
        fnt = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc',size= 40)
        for p in range(len(plist['words_result'])):
            draw.text((plist['words_result'][p]['position'][0]-20,plist['words_result'][p]['position'][1]-25), numl[p], fill='black', font=fnt)

        img1.save(f"./images/{i}-{keyStr}.jpg")
