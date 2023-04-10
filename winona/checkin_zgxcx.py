import requests
from ql_api import get_envs

xcxUserToken = get_envs("zgToken")[0]
# 薇诺娜  专柜  小程序签到
def xcx_signin():
    zg_url = "https://api.qiumeiapp.com/zgxcx/10001/addZgSignIn"
    zg_headers = {
        "Host": "api.qiumeiapp.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wx250394ab3f680bfa/330/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }
    zg_data = {
        "zgUserToken": xcxUserToken["value"]
    }
    zg_res = requests.post(url=zg_url, headers=zg_headers, data=zg_data).json()
    zg_msg = zg_res['msg']
    if zg_msg == "成功":
        result = "签到" + zg_msg
        pass_push = "⭕签到成功"
        return result , pass_push
    else:
        result = "签到失败，返回结果：\n" + str(zg_res)
        fail_push = "❌签到失败，具体请查看日志信息"
        return result , fail_push

if __name__ == "__main__":
    a = xcx_signin()
    print(a)