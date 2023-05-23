'''
cron:  0 8 * * *
new Env('MT论坛签到')
'''
import requests
import re
import os
from notify import send

bbs_url = "https://bbs.binmt.cc/member.php"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'}
session = requests.session()
def getLoginHashes():
    params = {
        'mod': 'logging',
        'action': 'login'
    }
    login_res = session.get(url=bbs_url,headers=headers,params=params)
    try:
        loginhash = re.search(r'loginhash=(.+?)"', login_res.text).group(1)
    except:
        print("登录loginhash查找失败，退出")
        return False
    try:
        formhash = re.search(r'name="formhash" value="(.+?)"', login_res.text).group(1)
    except:
        print("登录formhash查找失败，退出")
        return False
    return loginhash,formhash

def login(loginhash,formhash,u,p,loginfield = "username"):
    params = {
        'mod': 'logging',
        'action': 'login',
        'loginsubmit': 'yes',
        'loginhash': loginhash,
        'inajax': '1'
    }
    data = {
        'formhash': formhash,
        'loginfield': loginfield,
        'username': u,
        'password': p,
        'questionid': '0',
        'answer': ''
    }
    res = session.post(url=bbs_url,headers=headers,params=params,data=data)
    if '欢迎您回来' in res.text:
        print('登录成功')
    elif "手机号登录成功" in res.text:
        print('手机号登录成功')
    else:
        print("登录失败\n",res.text)
        return False

def checkin():
    checkin_res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html',headers=headers)
    try:
        checkin_formhash = re.search('name="formhash" value="(.+?)"',checkin_res.text).group(1)
    except:
        return "签到formhash查找失败，退出"
    res= session.get(f'https://bbs.binmt.cc/plugin.php?id=k_misign%3Asign&operation=qiandao&format=empty&formhash={checkin_formhash}',headers=headers)
    if "![CDATA[]]" in res.text:
        return '🎉签到成功'
    elif "今日已签" in res.text:
        return '🐔今日已签'
    else:
        print(res.text)
        return '签到失败'

def checkinfo():
    res = session.get(url='https://bbs.binmt.cc/k_misign-sign.html',headers=headers)
    user = re.search('class="author">(.+?)</a>',res.text).group(1)
    lxdays = re.search('id="lxdays" value="(.+?)"',res.text).group(1)
    lxlevel = re.search('id="lxlevel" value="(.+?)"',res.text).group(1)
    lxreward = re.search('id="lxreward" value="(.+?)"',res.text).group(1)
    lxtdays = re.search('id="lxtdays" value="(.+?)"',res.text).group(1)
    paiming = re.search('您的签到排名：(.+?)<',res.text).group(1)
    msg = f'【MT论坛账号】{user}\n【连续签到】{lxdays}\n【签到等级】Lv.{lxlevel}\n【积分奖励】{lxreward}\n【签到天数】{lxtdays}\n【签到排名】{paiming}\n\n'
    return msg

if __name__ == "__main__":
    if 'MT_BBS' in os.environ:
        print("###MT论坛签到###")
        config = os.environ['MT_BBS'].split(';')
        username = config[0]
        password = config[1]
        hashes = getLoginHashes()
        if hashes is False:
            msg = 'hash获取失败'
        else:
            if "@" in username:
                loginfield = "email"
            else:
                loginfield = "username"
            if login(hashes[0],hashes[1],username,password,loginfield) is False:
                msg = '账号登录失败'
                print(f'{username}\n{password}')
            else:
				c = checkin()
				info = checkinfo()
                msg = c + info
        # 青龙通知推送
        send('MT论坛签到',msg)
    else:
        print('未添加"MT_BBS"变量，退出')
		