import requests
import json
import logging
import SEATS
import sys


def get_setting():
    with open(sys.argv[1],"r") as f:
        setting = json.load(f)
    return setting


def get_data_json():
    data_json = {
    "login_name":"",
    "password":"",
    "login_name_type":"school_number",
    "org_id":"142",
    "code":"",
    "str":""
    }
    data_json["login_name"] = setting['number']
    data_json["password"] = setting['password']
    preview = json.loads(requests\
    .get('https://jxnu.huitu.zhishulib.com/User/Index/login?forward=/Seat/Index/searchSeats&LAB_JSON=1').text)
    data_json["code"] = preview['content']['data']['code']
    data_json["str"] = preview['content']['data']['str']
    return data_json


# def get_cookies(data_json):
#     import http.cookiejar as cj
#     s = requests.session()
#     s.cookies = cj.LWPCookieJar()
#     s.post("https://jxnu.huitu.zhishulib.com/api/1/login", json = data_json )
#     s.close()
#     fp = open("cookies.txt", "r")
#     t = fp.readlines()
#     fp.close()
#     cookies = ''
#     for i in t[1:]:
#         start_pos = i.find("Set-Cookie3: ")+13
#         end_pos = i.find(";")+1
#         i = i[start_pos:end_pos]
#         i = i.replace('\"','')
#         cookies += i
#     return cookies


def set_begintime():
    import datetime
    time = 1541347200
    date = setting['date']
    if date == 'today':
        time = 1541347200 - 3600 * 24
    date = datetime.datetime.strptime('2018-11-04', '%Y-%m-%d')
    sec = 86400
    now = datetime.datetime.now()
    begintime = time + sec * (now - date).days
    return begintime


def get_data_forms(data_json):
    data_forms = []
    studyroom = setting["studyroom"]
    while(studyroom):
        if studyroom == "3S" or studyroom == "3s":
            seats = list(SEATS.t_s[i] for i in setting["seats"])
            break
        elif studyroom == "3N" or studyroom == "3n":
            seats = list(SEATS.t_n[i] for i in setting["seats"])
            break
        elif studyroom == "2S" or studyroom == "2s":
            seats = list(SEATS.s_s[i] for i in setting["seats"])
            break
        elif studyroom == "2N" or studyroom == "2n":
            seats = list(SEATS.s_n[i] for i in setting["seats"])
            break
        break
    seatBooker = Booker
    for i in seats:
        data_form = {
        'beginTime': '',
        'duration': '',
        'seats[0]': '',
        'seatBookers[0]': ''
        }
        beginTime = setting['beginTime']
        duration = setting['duration']
        data_form['seatBookers[0]'] = seatBooker
        data_form['beginTime'] = set_begintime() + beginTime * 3600
        data_form['duration'] = duration * 3600   
        data_form['seats[0]'] = i
        data_forms.append(data_form)
    return data_forms


def connecting(data_form):
    try:
        r = requests.post('https://jxnu.huitu.zhishulib.com/Seat/Index/bookSeats?LAB_JSON=1',\
        data = data_form, cookies = cookies,timeout = 3 )       
        while(r.status_code!=200):
            logging.info("status_code = "+ r.status_code + ", retry...")
            return connecting(data_form)
        # logging.info("Connect successfully!")
        # print(r.text)
        return r
    except:
        return connecting(data_form)
        

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='status.log', level=logging.DEBUG, format=LOG_FORMAT)
# logging.debug("This is a debug log.")
# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log.")


setting = get_setting()
data_json = get_data_json()
login = requests.post("https://jxnu.huitu.zhishulib.com/api/1/login", json = data_json)
cookies = login.cookies.get_dict()
Booker = json.loads(login.text)['id']
data_forms = get_data_forms(data_json)


r = connecting(data_forms[0])
preview = json.loads(r.text)
result = preview['DATA']['result']
n = len(data_forms)
while result == 'fail':
    logging.error(preview['DATA']['msg'])
    n = n+1
    # print(data_forms[n%len(data_forms)]['seats[0]'])
    r = connecting(data_forms[n%len(data_forms)])
    print(r)
    preview = json.loads(r.text)
    result = preview['DATA']['result']

if result == 'success':
    logging.info("succeed!")
