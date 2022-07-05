import requests
from urllib.parse import urlparse, parse_qsl
class DaiLi:
    def __init__(self):
        self.url = None
        self.number = None

    def getProxies(self):
        ipdict  =  self.getIp()

        if ipdict["msg"] == "ok":
            self.number = ipdict['number']
            ipdict['proxies'] = {
                "http": "http://" + ipdict['IP'],
                "https": "https://" + ipdict['IP']
            }
        """
          {
                'IP': '117.95.199.163:35515', 
                'number': 8718, 
                'msg': 'ok',
                'proxies': {
                    'http': 'http://117.95.199.163:35515', 
                    'https': 'https://117.95.199.163:35515'
                }
            }
        """
        return ipdict

    def getIp(self):
        pass



    def getUrlParse(self):
        '''
        解析URL
        :return:
        '''
        try:
            uparse = urlparse(self.url)
            return {
                'scheme' : uparse.scheme,
                'message': "ok",
                'host': uparse.netloc,
                'path': uparse.path,
                'params': dict(parse_qsl(uparse.query))
            }
        except Exception:
            return {
                'message': None,
            }



    def getLocalHostIp(self,proxies):
        '''
        验证ip是否可用
        :param proxies:
        :return:
        '''
        try:
            res = requests.get('http://httpbin.org/get', timeout=5, proxies=proxies)
            origin = res.json()['origin']
            return {
                "IP" : origin,
                "msg" : "ok"
            }
        except Exception as e:
            return {
                "msg": None
            }
