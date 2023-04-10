import requests
from os import environ
from ql_api import get_envs,put_envs

# 重新登录获取token，官方小程序、移动网页端通用
def get_web_token():
    webAccount = get_envs("webAccount")[0]
    login_url = "https://api.qiumeiapp.com/gwm/10001/gwmUserLogin"
    login_headers = {
        "Host": "api.qiumeiapp.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 Edg/106.0.1370.52",
        "Origin": "https://m.winona.cn",
        "Referer": "https://m.winona.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    login_data = {
        "loginMode": "1",
        "loginName": webAccount["value"].split(",")[0],
        "password": webAccount["value"].split(",")[1],
        "verificationCode": ""
    }

    login_res = requests.post(url=login_url, headers=login_headers, data=login_data).json()
    try:
        apptoken = login_res["data"]["appUserToken"]
        put_envs(webAccount["id"],webAccount["name"],apptoken)
    except:
        apptoken = login_res
    return apptoken
