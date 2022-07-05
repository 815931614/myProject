from DaiLi import DaiLi
from urllib.parse import urlencode
import requests
class YiDaiLi(DaiLi):
    def __init__(self):
        super().__init__()

    def getIp(self):

        # {'status': 'success', 'left_time': 0, 'number': 8719, 'domain': '', 'data': [{'IP': '58.241.179.164:48452', 'ISP': None, 'IpAddress': None}]}
        # { "info":"数量用完了，请及时续费或充值", "status":"206" }
        '''
        206ip数量用完
        203需要添加白名单
        406提取间隔太快
        215单次提取数量超过上限
        '''
        try:
            res = requests.get(self.url, timeout=5).json()

            if "info" in res.keys():
                return {
                    "code":1,
                    "msg": res['info']
                }
            if res['status'] == 'success':
                return {
                    "code": 0,
                    "IP": res['data'][0]['IP'],
                    "number" : res['number'],
                    "msg": "ok"
                }
        except Exception as e:
            return {
                "code": 999,
                "msg": "代理链接请求错误。"
            }


    def isUrl(self,url):
        '''
        验证URL链接格式
        :param url:
        :return:
        '''
        self.url = url

        uparse = self.getUrlParse()

        if  uparse['message'] != "ok" or uparse['host'] != 'api1.ydaili.cn' or ("secret" not in uparse['params'].keys() and "key" not in uparse['params'].keys()) or "format" not in uparse['params'].keys() or "number" not in uparse['params'].keys():
            return False

        uparse['params']['format'] = 'json'
        uparse['params']['number'] = 1
        self.url = uparse['scheme'] + "://" + uparse['host'] + uparse['path'] + "?" + urlencode(uparse['params'])
        return True

if __name__ == '__main__':
    ydl =  YiDaiLi()
    ydl.url = "http://api1.ydaili.cn/tools/BMeasureApi.ashx?action=BEAPI&secret=C889D62C154089F9E4EC47408FA4F3D93021822792CD6452FDF2773B9B6803034C36EEB463A4FFF9&number=1&orderId=SH20220511002533319&format=json"

    print(ydl.isUrl(ydl.url))