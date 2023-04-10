import requests
def airportCheckin():
    usrurl = "https://glados.rocks/api/user/checkin"
    usrheaders = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
        "Cookie": "koa:sess=eyJ1c2VySWQiOjI1Njg5MCwiX2V4cGlyZSI6MTY5ODQ4NDk1MDA0MiwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=NOn0P-kAGStxhFNbeERzmIBe74E"
    }
    usrdata = {"token": "glados.network"}
    checkinResponse = requests.post(url=usrurl,headers=usrheaders,json=usrdata).json()
    return checkinResponse["message"]
