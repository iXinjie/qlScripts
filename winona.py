import requests
import notify



phone = ""
pwd = ""


print(f"用户【{phone}】开始签到\n")

def Login(phone,pwd):

    urlLogin = "https://api.qiumeiapp.com/gwm/10001/gwmUserLogin"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
        "Referer": "https://m.winona.cn/",  #必要参数
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    data = {
        "loginMode" : "1",
        "loginName" : phone,
        "password" : pwd,
        "verificationCode" : ""
    }

    response = requests.post(url=urlLogin,headers=headers,data=data).json()
    # print(response)
    if response["code"] == 200:
        return response["data"]["appUserToken"]
    else:
        return response



def zgSignIn(token):
    signInUrl = "https://api.qiumeiapp.com/zg-activity/zg-daily/zgSigninNew"
    headers = {
        "xweb_xhr": "1",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/9079",
        "Content-Type" : "application/x-www-form-urlencoded",
        "Accept" : "*/*"
    }

    data = {"appUserToken" : token}

    response = requests.post(url=signInUrl,headers=headers,data=data).json()
    if response["code"] == 200:
        return True
    else:
        return response


# 获取Token
try:
    token = Login(phone,pwd)
    if len(token) == 40:
        # 开始签到
        content = ""
        zgRes = zgSignIn(token)
        if zgRes is True:
            # print("专柜小程序端签到成功\n")
            content += "专柜小程序端签到成功\n"
        else:
            # print(f"专柜小程序签到:\n{zgRes}\n")
            content += f"专柜小程序签到:\n\n{zgRes}\n"
        print(content)
        notify.send("薇诺娜签到",content)
    else:
        print("Token获取失败，签到未完成")
        notify.send("薇诺娜签到","Token获取失败，签到未完成")
except:
    
    print("获取Token失败，签到未完成")
    notify.send("薇诺娜签到","Token获取失败，签到未完成")
