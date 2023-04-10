import time
import requests
from get_webToken import get_web_token
from ql_api import get_envs

tokens = get_envs("webToken")[0]
pass_push = "⭕签到成功"
fail_push = "❌签到失败，具体请查看日志信息"
already_push = "⭕今天已经签到了"
frequent_push = "❌请勿频繁签到！"

# 签到配置
url = "https://api.qiumeiapp.com/gw-activity/gw-daily/userSignin"
headers = {
    "Host": "api.qiumeiapp.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-us,en",
    "Cookies": 'acw_tc=707c9fd616687869500016522e17ed89bc6768e58c713428996aa096091a20; JSESSIONID=46EC3261A49A0D608741135A6303C72D'
}
data = {
    "appUserToken": tokens["value"],
    "sysCode": "xcx"
}
# 执行签到
def gfxcx_sign(request_url,request_headers,request_data):
    res = requests.post(url=request_url, headers=request_headers, data=request_data).json()
    msg = res['msg']
    code = res['code']
    return msg,code,res

def gfxcx_signin():
    res = gfxcx_sign(url,headers,data)
    msg = res[0]
    code = res[1]
    if code == 200:
        return msg, pass_push
    elif code == 714:
        return msg, already_push
    # 600代表token失效，需重新登录获取新的token
    elif code == 600:
        print("gfxcx尝试重新获取Token")
        new_token = get_web_token()
        print("获取到用户token：" + new_token)
        print("正在重试签到")
        new_data = {
            "appUserToken": new_token,
            "sysCode": "xcx"
        }
        # 重新签到
        time.sleep(1)
        res1 = gfxcx_sign(url,headers,new_data)
        msg1 = res1[0]
        code1 = res1[1]
        if code1 == 200:
            print("官方小程序签到成功")
            return msg1, pass_push, new_token
        elif code1 == 600:
            print("官方小程序重试签到失败")
            return res1, fail_push, new_token
        elif code1 == 714:
            return msg1, already_push, new_token
        elif code1 == 703:
            print(frequent_push)
            print("等待30秒")
            time.sleep(30)
            res2 = gfxcx_sign(url,headers,new_data)
            msg2 = res2[0]
            code2 = res2[1]
            if code2 == 200:
                return msg2, pass_push, new_token
            elif code2 == 714:
                return msg2, already_push, new_token
            elif code2 == 703 :
                print("频繁签到，请稍后再试")
                return msg2, frequent_push, new_token
            elif code2 == 600 :
                print("失败，Token无效")
            else:
                print("官方小程序重新签到失败，未知")
                return res2, fail_push, new_token

        else:
            print("官方小程序重新签到失败，未知错误")
            return res1, fail_push, new_token

    elif code == 703:
        print(frequent_push)
        print("等待30秒")
        time.sleep(30)
        res3 = gfxcx_sign(url,headers,data)
        msg3 = res3[0]
        code3 = res3[1]
        if code3 == 200:
            return msg3, pass_push
        elif code3 == 714:
            return msg3, already_push
        elif code3 == 703:
            print("频繁签到，请稍后再试")
            return msg3, frequent_push
        else:
            return res3, fail_push

    else:
        return res, fail_push
