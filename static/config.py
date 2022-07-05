class Config:
    def __init__(self):
        # 项目名称
        self.projectName = ""

        # 是否需要接码
        self.isJieMa = True


        # 是否需要打码
        self.isDaMa = True


        # 1：必须使用代理 ，2：无需代理 ， 3：可有可无
        self.isDaiLi = 1


        # 是否需要料子
        self.isCard = False


        # 默认邀请码
        self.invitation_input = "123"


        # 默认注册数量
        self.runSuccessNum_input = 2



        # 默认线程数量
        self.threadNum_input = 1