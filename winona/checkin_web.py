import time
import requests
from get_webToken import get_web_token
from ql_api import get_envs,put_envs

tokens = get_envs("webToken")[0]
token = tokens["value"]
pass_push = "⭕签到成功"
fail_push = "❌签到失败，具体请查看日志信息"

# mobile_web_signin_config 请求参数
web_url = "https://api.qiumeiapp.com/gwm/10001/addGwmSignIn"
web_headers = {
    "Host": "api.qiumeiapp.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 Edg/106.0.1370.42",
    "Referer": "https://m.winona.cn/",
    "Accept-Encoding": "gzip, deflate, br"
}
web_data = {
    "appUserToken": token,
    "type": "2"
}

def mobile_web_signin(signin_url, signin_headers, signin_data):
    web_res = requests.post(url=signin_url, headers=signin_headers, data=signin_data).json()
    web_msg = web_res["msg"]
    web_code = web_res["code"]
    return web_msg,web_code,web_res

def mobile_web_signin_action():
    res = mobile_web_signin(web_url, web_headers, web_data)
    msg = res[0]
    code = res[1]
    if msg == "成功":
        return msg , pass_push
    elif code == 702:
        res1 = mobile_web_signin(web_url, web_headers, web_data)
        msg1 = res1[0]
        code1 = res1[1]
        if msg1 == "成功":
            return msg1, pass_push
        else:
            return res1, fail_push
    elif code == 703:
        for i in range(0,3):
            # 操作频繁，间隔10s重试3次
            time.sleep(10)
            res2 = mobile_web_signin(web_url, web_headers, web_data)
            msg2 = res2[0]
            code2 = res2[1]
            if msg2 == "成功":
                return msg2, pass_push
            else:
                pass
        return res2, fail_push
    # 600代表token失效，需重新登录获取新的token
    elif code == 600:
        # 获取新token
        print("web尝试重新获取Token")
        new_token = get_web_token()
        tokens["web"] = new_token
        print("获取到用户token：" + new_token)
        print("正在重试签到")
        signin_new_data = {
            "appUserToken": new_token,
            "type": "2"
        }
        # 重新签到
        res2 = mobile_web_signin(web_url, web_headers, signin_new_data)
        msg2 = res2[0]
        code2 = res2[1]
        if msg2 == "成功":
            print("移动网页端签到成功")
            return msg2, pass_push
        else:
            return res2, fail_push
    else:
        return res, fail_push
