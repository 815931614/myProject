from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets
import re
import time

class ThirdPartyLogin(QThread):
    loginRes = pyqtSignal(dict,QtWidgets.QPushButton)
    def __init__(self,function,username,password,btn):
        super(QThread, self).__init__()
        self.btn = btn
        self.function = function
        self.username = username
        self.password = password
    def run(self):
        res = self.function(self.username,self.password)
        self.loginRes.emit(res,self.btn)

class ProxiesTest(QThread):
    testRes = pyqtSignal(dict,QtWidgets.QPushButton)
    def __init__(self,function, btn):
        self.function = function
        self.btn = btn
        super(QThread, self).__init__()

    def run(self):

        self.testRes.emit(self.function(),self.btn)




class ReadIdCard(QThread):
    _idCardRead = pyqtSignal(dict)
    _setProgressBarNum = pyqtSignal(int)
    def __init__(self, rlist):

        self.rlist = rlist
        super(QThread, self).__init__()

    def run(self):
        errorLine = 0
        flag = False
        listcar = []
        shangci = 0
        for rts in range(len(self.rlist)):
            l = None
            onLine = self.is_name_card(self.rlist[rts])
            if rts == len(self.rlist) - 1:
                flag = True
            if onLine['code'] != 0:
                errorLine += 1
                l = [self.rlist[rts], "", "失败", rts]
            else:
                name = onLine['name']
                idCard = onLine['id_card']
                l = [self.rlist[rts], name + "/" + idCard, "成功", rts]
            listcar.append(l)
            if len(listcar) == rts + 1:
                flag = True
            if len(listcar) % 500 == 0:
                self._setProgressBarNum.emit(int(len(listcar) / (len(self.rlist) / 100)))
                time.sleep(.01)
            elif len(listcar) == rts + 1:
                self._setProgressBarNum.emit(100)
        self._idCardRead.emit({
            'rlist' : listcar,
            'errorLine' : errorLine

        })

        # self._idCardRead.emit(flag)
    def is_name_card(self, text):
        data = {"name": None, "id_card": None, "msg": "", 'code': 0}
        pattern_name = r'[付|自|赵|钱|孙|李|周|吴|郑|王|冯|陈|褚|卫|蒋|沈|韩|杨|朱|秦|尤|许|何|吕|施|张|孔|曹|严|华|金|魏|陶|姜|戚|谢|邹|喻|柏|水|窦|章|云|苏|潘|葛|奚|范|彭|郎|鲁|韦|昌|马|苗|凤|花|方|俞|任|袁|柳|酆|鲍|史|唐|费|廉|岑|薛|雷|贺|倪|汤|滕|殷|罗|毕|郝|邬|安|常|乐|于|时|傅|皮|卞|齐|康|伍|余|元|卜|顾|孟|平|黄|和|穆|萧|尹|姚|邵|湛|汪|祁|毛|禹|狄|米|贝|明|臧|计|伏|成|戴|谈|宋|茅|庞|熊|纪|舒|屈|项|祝|董|梁|杜|阮|蓝|闵|席|季|麻|强|贾|路|娄|危|江|童|颜|郭|梅|盛|林|刁|锺|徐|邱|骆|高|夏|蔡|田|樊|胡|凌|霍|虞|万|支|柯|昝|管|卢|莫|经|房|裘|缪|干|解|应|宗|丁|宣|贲|邓|郁|单|杭|洪|包|诸|左|石|崔|吉|钮|龚|程|嵇|邢|滑|裴|陆|荣|翁|荀|羊|於|惠|甄|麴|家|封|芮|羿|储|靳|汲|邴|糜|松|井|段|富|巫|乌|焦|巴|弓|牧|隗|山|谷|车|侯|宓|蓬|全|郗|班|仰|秋|仲|伊|宫|宁|仇|栾|暴|甘|钭|历|戎|祖|武|符|刘|景|詹|束|龙|叶|幸|司|韶|郜|黎|溥|印|宿|白|怀|蒲|邰|从|鄂|索|咸|籍|卓|蔺|屠|蒙|池|乔|阳|郁|胥|能|苍|双|闻|莘|党|翟|谭|贡|劳|逄|姬|申|扶|堵|冉|宰|郦|雍|却|桑|桂|濮|牛|寿|通|边|扈|燕|冀|浦|尚|农|温|别|庄|晏|柴|瞿|充|慕|连|茹|习|宦|艾|鱼|容|向|古|易|慎|戈|廖|庾|终|暨|居|衡|步|都|耿|满|弘|匡|国|文|寇|广|禄|阙|东|欧|沃|利|蔚|越|夔|隆|师|巩|厍|聂|晁|勾|敖|融|冷|訾|辛|阚|那|简|饶|空|曾|毋|沙|乜|养|鞠|须|丰|巢|关|蒯|相|荆|红|游|竺|权|司马|上官|欧阳|夏侯|诸葛|闻人|东方|赫连|皇甫|尉迟|公羊|澹台|公冶宗政|濮阳|淳于|单于|太叔|申屠|公孙|仲孙|轩辕|令狐|钟离|宇文|长孙|慕容|司徒|司空|召|有|舜|岳|黄辰|寸|贰|皇|侨|彤|竭|端|赫|实|甫|集|象|翠|狂|辟|典|良|函|芒|苦|其|京|中|夕|乌孙|完颜|富察|费莫|蹇|称|诺|来|多|繁|戊|朴|回|毓|鉏|税|荤|靖|绪|愈|硕|牢|买|但|巧|枚|撒|泰|秘|亥|绍|以|壬|森|斋|释|奕|姒|朋|求|羽|用|占|真|穰|翦|闾|漆|贵|代|贯|旁|崇|栋|告|休|褒|谏|锐|皋|闳|在|歧|禾|示|是|委|钊|频|嬴|呼|大|威|昂|律|冒|保|系|抄|定|化|莱|校|么|抗|祢|綦|悟|宏|功|庚|务|敏|捷|拱|兆|丑|丙|畅|苟|随|类|卯|俟|友|答|乙|允|甲|留|尾|佼|玄|乘|裔|延|植|环|矫|赛|昔|侍|度|旷|遇|偶|前|由|咎|塞|敛|受|泷|袭|衅|叔|圣|御|夫|仆|镇|藩|邸|府|掌|首|员|焉|戏|可|智|尔|凭|悉|进|笃|厚|仁|业|肇|资|合|仍|九|衷|哀|刑|俎|仵|圭|夷|徭|蛮|汗|孛|乾|帖|罕|洛|淦|洋|邶|郸|郯|邗|邛|剑|虢|隋|蒿|茆|菅|苌|树|桐|锁|钟|机|盘|铎|斛|玉|线|针|箕|庹|绳|磨|蒉|瓮|弭|刀|疏|牵|浑|恽|势|世|仝|同|蚁|止|戢|睢|冼|种|涂|肖|己|泣|潜|卷|脱|谬|蹉|赧|浮|顿|说|次|错|念|夙|斯|完|丹|表|聊|源|姓|吾|寻|展|出|不|户|闭|才|无|书|学|愚|本|性|雪|霜|烟|寒|少|字|桥|板|斐|独|千|诗|嘉|扬|善|揭|祈|析|赤|紫|青|柔|刚|奇|拜|佛|陀|弥|阿|素|长|僧|隐|仙|隽|宇|祭|酒|淡|塔|琦|闪|始|星|南|天|接|波|碧|速|禚|腾|潮|镜|似|澄|潭|謇|纵|渠|奈|风|春|濯|沐|茂|英|兰|檀|藤|枝|检|生|折|登|驹|骑|貊|虎|肥|鹿|雀|野|禽|飞|节|宜|鲜|粟|栗|豆|帛|官|布|衣|藏|宝|钞|银|门|盈|庆|喜|及|普|建|营|巨|望|希|道|载|声|漫|犁|力|贸|勤|革|改|兴|亓|睦|修|信|闽|北|守|坚|勇|汉|练|尉|士|旅|五|令|将|旗|军|行|奉|敬|恭|仪|母|堂|丘|义|礼|慈|孝|理|伦|卿|问|永|辉|位|让|尧|依|犹|介|承|市|所|苑|杞|剧|第|零|谌|招|续|达|忻|六|鄞|战|迟|候|宛|励|粘|萨|邝|覃|辜|初|楼|城|区|局|台|原|考|妫|纳|泉|老|清|德|卑|过|麦|曲|竹|百|福|言|第五|佟|爱|年|笪|谯|哈|墨|连|南宫|赏|伯|佴|佘|牟|商|西门|东门|左丘|梁丘|琴|后|况|亢|缑|帅|微生|羊舌|海|归|呼延|南门|东郭|百里|钦|鄢|汝|法|闫|楚|晋|谷梁|宰父|夹谷|拓跋|壤驷|乐正|漆雕|公西|巫马|端木|颛孙|子车|督|仉|司寇|亓官|三小|鲜于|锺离|盖|逯|库|郏|逢|阴|薄|厉|稽|闾丘|公良|段干|开|光|操|瑞|眭|泥|运|摩|伟|铁|迮][\u4e00-\u9fa5]{1,3}'
        find_name = re.findall(pattern_name, text)
        if find_name:
            data['name'] = find_name[0]
        regularExpression = "\\d{17}[\\d|x|X]|\\d{15}"
        match2 = re.findall(regularExpression, text)
        if match2:
            regularExpression2 = r"^([1-6][1-9]|50)\d{4}(18|19|20)\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
            regularExpression3 = r"^([1-6][1-9]|50)\d{4}\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}$"
            if re.match(regularExpression2, match2[0]) or re.match(regularExpression3, match2[0]):
                data['id_card'] = match2[0]
        if not data['name'] or not data['id_card']:
            data['code'] = 1
        return data
