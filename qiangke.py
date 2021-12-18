import time
import requests
import os



class Qiangke:
    def __init__(self, ):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    # 验证码
    def verfiyCode(self):
        url = "http://www.fjpit.com/studentportal.php/Public/verify/"

        res = self.session.get(url, verify=False)

        img = res.content

        with open('验证码.png', 'wb') as f:
            f.write(img)

        self.code = input("请打开软件所在目录查看“验证码.png”并输入：")

        os.remove('验证码.png')

        return 1

    # 登录
    def login(self, userName, passWord):
        url = 'http://www.fjpit.com/studentportal.php/Index/checkLogin'

        data = {
            "logintype": "xsxh",
            'xsxh': userName,
            'dlmm': passWord,
            'yzm': self.code
        }
        res = self.session.post(url, data=data, verify=False).json()
        if res['code'] == 3:
            print('验证码识别错误！')
            return 0
        elif res['code'] == 0:
            return 1
        else:
            print(res)
            print('❌ 登录异常, 出现未知错误！')
            time.sleep(3)
            exit()

    # 获取选修课列表
    def courseInfo(self):
        courselist = []
        url = 'http://www.fjpit.com/studentportal.php/Wsxk/yjxklb/xn/2021-2022/xq/2'
        res = self.session.post(url, verify=False).json()['rows']
        for i, list in enumerate(res):
            id = list['id']
            courselist.append(id)
            name = list['kcmc']
            tech = list['zdjsxm']
            leixin = list["kcflmc"]
            rang = list["kkxqmc"]
            print(f"{i + 1}.{name} {tech} {leixin} {rang}")
        return courselist

    # 发送请求数据
    def processingData(self, ID):
        url = 'http://www.fjpit.com/studentportal.php/Wsxk/yjxkbc'
        data = {
            'xkxxid': ID,  # 166492
            'xktjid': 0
        }
        reponse = self.session.post(url, data=data).json()
        if reponse["Code"] == 0:
            print(reponse["errorMsg"])
        elif reponse["Code"] == 1:
            print('恭喜你成功抢到课了！')
        else:
            time.sleep(1)
            os.system(
                r'start "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://h.fmbit.top')
            print("欢迎来到官网！")


if __name__ == "__main__":

    xxk = Qiangke()
    print('开始登录...⏳')

    while True:
        # 登录
        user = "XXX"
        password = "XXX"
        if xxk.verfiyCode() and xxk.login(user, password):
            print('登录成功 ✅')
            xkid = xxk.courseInfo()
            while True:
                courseid = int(input("请输入课程序号(0退出）："))
                if courseid > len(xkid):
                    print("所选课程不在范围内，请重新输入！")
                    continue
                courseId = xkid[courseid - 1]
                xxk.processingData(courseId)
                if courseid == 0:
                    break
            break
        else:
            print('⚠️  2秒后将重新登录, 请等待...')
            time.sleep(2)
