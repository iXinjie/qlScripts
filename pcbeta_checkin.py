import requests
from datetime import datetime
import time
import re

cookies = "jqCP_887f_saltkey=; jqCP_887f_auth="
pcUrl = "https://i.pcbeta.com/home.php?mod=task&do=apply&id=149"
pcHeaders = {
    "Host": "i.pcbeta.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie": cookies
}

pcbbsHeaders = {
    "Host": "bbs.pcbeta.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie": cookies
}


# 领取奖励链接
lqurl = "https://i.pcbeta.com/home.php?mod=task&do=draw&id="
# 获取新任务链接
newUrl = "https://i.pcbeta.com/home.php?mod=task&item=new"
# 查看已完成任务链接
doneUrl = "https://i.pcbeta.com/home.php?mod=task&item=done"
# 获取签到状态信息
newTaskRes = requests.get(url=newUrl,headers=pcHeaders).text
doneTaskRes = requests.get(url=doneUrl, headers=pcHeaders).text
doingRes = requests.get("https://i.pcbeta.com/home.php?mod=task&item=doing",headers=pcHeaders)


def writeLog(file):
    time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open(f"./log/pcBetalog-{time}.html", "w") as f:
        f.write(file)

def pcbetaCheckin():
    import time
    id = "149"
    if "每日打卡" in newTaskRes:
        # 开始执行签到
        taskRes = requests.get(url=pcUrl, headers=pcHeaders).text
        if "抱歉，本期您已申请过此任务，请下期再来" in taskRes:
            return "已签到，请勿重复签到"
        elif "恭喜您，任务已成功完成" in taskRes:
            return "签到成功"
        else:
            time.sleep(1)
            lqRes = requests.get(url=lqurl+id, headers=pcHeaders).text
            if "任务已成功完成" in lqRes:
                return "签到成功，PB币+1"

            if "不是进行中的任务" in lqRes:
                # 检查是否签到成功
                doneTaskRes_check = requests.get(url=doneUrl, headers=pcHeaders).text
                if "每日打卡" in doneTaskRes_check:
                    return "签到已完成"
                else:
                    return "签到失败"
            else:
                writeLog(lqRes)
                return "签到失败，具体情况请查看日志"
    elif "每日打卡" in doneTaskRes:
        return "今日已签到，重复签到"

def getTaskUrl():
    # 获取任务贴URL
    viewRes = requests.get(url=f"https://i.pcbeta.com/home.php?mod=task&do=view&id={idd}", headers=pcHeaders)
    tieUrl = re.search(r'在“<a href="(.+?)">', viewRes.text).group(1)
    replyRes = requests.get(url=tieUrl,headers=pcbbsHeaders)
    # 获取fid
    fid = re.search(r'fid=(.+?)&', replyRes.text).group(1)
    # 获取tid
    tid = re.search(r'tid=(.+?)&', replyRes.text).group(1)
    formhash = re.search(r'formhash=(.+?)&', replyRes.text).group(1)
    replyUrl = f"https://bbs.pcbeta.com/forum.php?mod=post&action=reply&fid={fid}&tid={tid}&extra=page=1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    return replyUrl,formhash

def getTaskID():
    news = requests.get(url=newUrl,headers=pcHeaders).text
    idd = re.search('id=(.+?)">回帖打卡', news).group(1)
    return idd

def pcbetaReply():
    taskName = "回帖打卡福利"
    # 获取任务id
    global idd
    idd = getTaskID()
    if taskName in newTaskRes:
        # 申请回帖打卡任务
        reRes = requests.get(url=f"https://i.pcbeta.com/home.php?mod=task&do=apply&id={idd}", headers=pcHeaders)
        if "任务申请成功" in reRes.text:
            result = getTaskUrl()
            # 回复帖子
            data = {"message":"%C3%BF%C8%D5%B4%F2%BF%A8%C7%A9%B5%BD",
                    "posttime":int(time.time()),
                    "formhash": result[1],
                    "subject":"",
                    "usesig":"1"}
            resRes = requests.post(url=result[0], headers=pcbbsHeaders, data=data)
            if "回复发布成功" in resRes.text:
                # 领取奖励
                lqRes1 = requests.get(url=lqurl+idd,headers=pcHeaders)
                # 获取任务状态
                doneTaskRes1 = requests.get(url=doneUrl, headers=pcHeaders)
                if taskName in doneTaskRes1.text:
                    return "打卡成功，PB币+2"
                else:
                    writeLog(lqRes1.text)
                    return "奖励领取失败"
            else:
                writeLog(resRes.text)
                return "回帖失败"
        else:
            writeLog(reRes.text)
            return "打卡任务申请失败"

    elif taskName in doneTaskRes:
        return "打卡已完成，重复打卡"

    elif taskName in doingRes.text:
        result = getTaskUrl()
        # 回复帖子
        data = {"message":"%C3%BF%C8%D5%B4%F2%BF%A8%C7%A9%B5%BD",
                "posttime":int(time.time()),
                "formhash": result[1],
                "subject":"",
                "usesig":"1"}
        resRes = requests.post(url=result[0], headers=pcbbsHeaders, data=data)
        if "回复发布成功" in resRes.text:
            # 领取奖励
            lqRes1 = requests.get(url=lqurl+idd, headers=pcHeaders)
            # 获取任务状态
            doneTaskRes1 = requests.get(url=doneUrl, headers=pcHeaders)
            if taskName in doneTaskRes1.text:
                return "打卡成功，PB币+2"
            else:
                writeLog(lqRes1.text)
                return "奖励领取失败"
        else:
            writeLog(resRes.text)
            return "回帖失败"
    else:
        return "没有此任务"

if __name__ == "__main__":
pcbetaCheckin()
pcbetaReply()
