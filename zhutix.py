"""
任务名称
name: 致美化签到
定时规则
cron: 0 0 9 * * *
"""

import requests
import notify

request = requests.session()

def getToken(u,p):
    url = 'https://zhutix.com/wp-json/jwt-auth/v1/token'
    header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
      "Connection": "keep-alive",
      "Accept": "application/json, text/plain, */*",
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    data = {
      "username": u,
      "password": p
    }
    res = request.post(url=url,headers=header,data=data).json()
    if res['token']:
        token = res['token']
        return token
    else:
        return False



def getMission(token):
    getUrl = 'https://zhutix.com/wp-json/b2/v1/getUserMission'
    getHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}"
    }
    res = request.post(url=getUrl,headers=getHeaders).json()
    return res


def signIn(token):
    postUrl = 'https://zhutix.com/wp-json/b2/v1/userMission'
    postHeader = {
        "Host": "zhutix.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Origin": "https://zhutix.com",
        "Authorization": f"Bearer {token}"
    }
    res = request.post(url=postUrl, headers=postHeader)
    return res


if __name__ == '__main__':
    u = ''  # 在此填写账号
    p = ''  # 在此填写密码
    token = getToken(u,p)
    if token:
        missionRes = getMission(token)
        # print(missionRes)
        if missionRes["mission"]["date"]:
            print("今日已签到")
        else:
            response = signIn(token)
            if "Vary" in response.headers:
                msg = response.json()
                # print(msg)
                if "date" in msg:
                    credit = msg["credit"]
                    always = msg["mission"]["always"]
                    my_credit = msg["mission"]["my_credit"]
                    notice = f"签到成功\n连续签到{always}天\n获得{credit}锋币\n总{my_credit}锋币"
                    notify.send("致美化签到",notice)
                else:
                    print(msg)
            else:
                print("签到失败")
                notify.send("致美化签到","签到失败")
    else:
        print("登录失败")
