import requests
from ql_api import get_envs

def serverJ(msg):
    try:
        serverJtoken = get_envs("wnn_serverJ")[0]["value"]
    except:
        print("没有添加server酱push_key，本次不推送")
        return False
    sUrl = f"https://sctapi.ftqq.com/{serverJtoken}.send"
    sData = {
        "title": "薇诺娜签到推送",
        "desp": msg
    }
    res = requests.post(sUrl,sData).json()
    return res

if __name__ == "__main__":
    pass