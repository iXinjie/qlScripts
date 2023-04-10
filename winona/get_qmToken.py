import requests
from ql_api import get_envs,put_envs

def get_qmToken():
    # 获取qm相关环境变量
    qmAccount = get_envs("qmAccount")[0]
    qmToken = get_envs("qmToken")[0]
    # 登录api参数
    qmlogin_url = "https://api.qiumeiapp.com/qm/10001/qmLogin"
    qmlogin_headers = {
        "appMarket": "android-qm",
        "appVersion": "8.2.0",
        # "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "api.qiumeiapp.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.11.0"
    }
    qmlogin_data = {
        "anonymousId": "3e8c61a511c438aa",
        "appMarket": "android",
        "appVersion": "8.2.0",
        "deviceModel": "Redmi K20 Pro",
        "deviceNumber": "3e8c61a511c438aa-unknown-null",
        "deviceToken": "Tk9SSUQuMSNmMzI3MWFjYzAyMzkxNTk4MmJjZDVmNDI2YmI5ODM4NS1oLTE2Nzc1MTg0ODk2MjktYjY5MDZhMjUxZmRhNDYwZjlhOTExM2ViYjU2NjQ4NjcjRHZkcEdadkU3Sis1cHI5djFiTm5VbUhrdUtoeWxhWS82bEVJNmZydjNuTFNYaURMYnFoM214OUlqeklBWkFpUjBPd2dYbWhzZFdQRDR6bFJsMGFBM3czS1ltMzE2T2YrZnRhSFcvSi9pZ2VDckZma1lqU2hVeDdTZlpRWmpJOUR1dlJ3aHJmZkV0Rms5ZlJYbm1rUUZnVmNLL1AxS3lpblVXZUxpM2pUMTlpc3VybnlKVUJmSnlTRUpLaXNBY3p5OEt4TlB6bTZYc3d1MEl4MkRpMVF4RjNSMEdOeEtIbWRuRE9MUXMvL094bHRXRDRWVytkQXljcHdwaVJEdzIrZUN2YmhYSEhZenprT29ReWJDdzU1a0ZEUGRheDlXSmttZHY2UFFjLzlPZVlnYzJUb2Vjbm1Ed2FDWkkweGRjbjBaSWxpZVVNd3dCd3BhR0pHemVpYmNLTnZhUTB5SFdTZmhiZTFKZmRRSU94bHFhQ0tVanF0ajRoM1FvRTN4eHo1WTFINS81elpyN2prK1Znb1F1WGFDKzBxUyt0elpOak9CQXh6dmhueTBxK0JxQmdMNlU3dGFXMjdwT0hxYi96UXg1d21sMmVTYVFzVDR5WVlXQVhlVWdTMm1FOTJzM0FRUTEyTjFON2djQytRUjdKWnJ0T0l0Q0xpUzBISllaNHJGekZuQkY4UDZUajdXbWNic2RLc0h6S1VsQzhjVWhYa2hicmJERDkwQnByeWk5aVNSclBFeDlQdkRDNC9URlFzTTMzWGFEbGFTSXh0bEFtbS92Q0E2NUJjRlZ6UVFqUnN4b2M3UVdxTzZUNllBUkhLTDFnV1VlZm0jNjkuODYzI0M0I2M3NmQ3MDc2M2ZiMDU3ZmRjYjkxZmJiMGFkNjIzYzQw",
        "phoneNumber": qmAccount["value"].split(",")[0],
        "password": qmAccount["value"].split(",")[1],
        "sign": "403ef4e2c9aaa838f689a9b35c650730"
    }
    # 执行接口
    qmlogin_res = requests.post(qmlogin_url, headers=qmlogin_headers, data=qmlogin_data).json()
    if qmlogin_res["code"] == 200:
        result = qmlogin_res["data"]["qmUserToken"]
        print(f"获取成功:{result}")
        put_envs(qmToken["id"],qmToken["name"],result)
        return result
    else:
        print("获取失败，返回结果：\n" + str(qmlogin_res))
        return False

if __name__ == "__main__":
    print(get_qmToken())