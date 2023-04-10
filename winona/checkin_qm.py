import requests
from get_qmToken import get_qmToken
from ql_api import get_envs

tokens = get_envs("qmToken")[0]
qmToken = tokens["value"]
pass_push = "⭕签到成功"
fail_push = "❌签到失败，具体请查看日志信息"
already_push = "⭕今天已经签到了"
luckdraw_none_push = "⛔今日没有抽奖资格！"

# 逑美签到配置
url = "https://api.qiumeiapp.com/qm-activity/qdcj/signin"
headers = {
    "Connection": "keep-alive",
    "Host": "api.qiumeiapp.com",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2011K2C Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.65 Mobile Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "com.pifukezaixian.users",
    "Referer": "https://h5.qiumeiapp.com/"
}
data = {
    "qmUserToken": qmToken
}

def get_luckdraw():
    u_url = 'https://api.qiumeiapp.com/qm-activity/qdcj/getUserSigninInfo'
    u_res = requests.post(url=u_url, headers=headers, data=data).json()
    if u_res["code"] == 702:
        data["qmUserToken"] = get_qmToken()
        u_res = requests.post(url=u_url, headers=headers, data=data).json()
    else:
        pass
    zige = u_res['data']['haveLuckyDraw']
    if zige == 1:
        # 抽奖
        # print("开始抽奖")
        c_url = "https://api.qiumeiapp.com/qm-activity/qdcj/luckyDraw"
        c_res = requests.post(url=c_url, headers=headers, data=data).json()
        c_msg = c_res['msg']
        # 获取抽奖结果
        if c_res['code'] == 200:
            # print('获得:' + c_res['data']['prizeName'])
            result = str("🎉获得" + c_res['data']['prizeName'])
            return result
        elif c_res['code'] == 704:
            print(c_res['msg'])
        else:
            print(c_res)
            result = "🩸抽奖异常，具体请查看日志信息"
            return result
    elif zige == 0:
        result = "⛔今日没有抽奖资格"
        return result

def qm_sign(qm_url,qm_headers,qm_data):
    res = requests.post(url=qm_url, headers=qm_headers, data=qm_data).json()
    msg = res['msg']  # 获取msg信息
    code = res['code']
    return msg,code,res

def qm_signin():
    res = qm_sign(url,headers,data)
    # 获取抽奖结果
    luckdraw = get_luckdraw()
    if res[1] == 200:
        return "签到成功", pass_push, luckdraw   # 返回msg信息，推送信息，抽奖信息
    elif res[0] == "用户不存在!":
        print(res)
        print("Token失效，尝试重新获取Token")
        new_token = get_qmToken()
        if new_token is False:
            fail = "token获取失败，具体查看日志"
            return fail
        else:
            print(f"qm获取到Token：{new_token}")
            resign_data = {"qmUserToken": new_token}
            print("qm尝试重新签到")
            res1 = qm_sign(url,headers,resign_data)
            luckdraw = get_luckdraw()
            if res1[1] == 200:
                return "签到成功", pass_push, luckdraw
            elif res1[0] == "你今天已经签到过了！":
                return res1[0], already_push, luckdraw
            else:
                return res1, fail_push, luckdraw
    elif res[1] == 615:
        return res[0], fail_push, luckdraw
    elif res[0] == "你今天已经签到过了！":
        return res[0], already_push, luckdraw
    else:
        return res, fail_push, luckdraw