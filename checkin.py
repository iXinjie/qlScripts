"""
cron: 0 0 8 ? * *
new Env('远景论坛签到');
"""
import checkin_pcbeta
pcBetaCheckinlog = f"远景论坛签到： {checkin_pcbeta.pcbetaCheckin()}"
print(pcBetaCheckinlog)
pcBetaReplyLog = f"远景论坛打卡： {checkin_pcbeta.pcbetaReply()}"
print(pcBetaReplyLog)
