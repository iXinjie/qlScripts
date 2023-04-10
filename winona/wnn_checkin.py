import datetime
import time


from checkin_zgxcx import xcx_signin
zgxcx = xcx_signin()
zglog = f"专柜小程序签到： {zgxcx[0]}"
print(zglog)


time.sleep(5)

from checkin_web import mobile_web_signin_action
web = mobile_web_signin_action()
weblog = f"移动网页端签到： {web[0]}"
print(weblog)


'''
time.sleep(6)

from checkin_gfxcx import gfxcx_signin
gfxcx = gfxcx_signin()
gfxcxlog = f"官方小程序签到： {gfxcx[0]}"
print(gfxcxlog)
'''

time.sleep(4)

from checkin_qm import qm_signin
qm = qm_signin()
qmlog = f"逑美APP签到： {qm[0]}\n逑美APP抽奖：{qm[-1]}"
print(qmlog)


from ql_serverJ import serverJ
# server酱推送
msg = f'专柜小程序：{zgxcx[1]}\n\n移动网页端：{web[1]}\n\n逑  美  APP ：{qm[1]}\n\n逑美APP抽奖：{qm[-1]}'
push = f'serverJ推送日志：{serverJ(msg)}'
