import datetime
import json
import logging
import sys
import requests
import SEATS


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


def search_used_seats():
    r = requests.post("https://jxnu.huitu.zhishulib.com/Seat/Index/searchSeats?LAB_JSON=1",\
    data = search_data_form, cookies = cookies)
    all_seats = json.loads(r.text)['data']['POIs']
    used_seats = {}
    for i in all_seats:
        if i['state'] == 0:
            used_seats[i['title']] = i['id']
    return used_seats


def get_best_seat(used_seats):
    if setting["seat"] in used_seats:
        best_seat = used_seats[setting["seat"]]
        return best_seat

    distinct = 9999
    for i in used_seats:
        temp = abs(int(i)-int(setting["seat"]))
        if temp < distinct:
            best_seat = used_seats[i]
            distinct = temp
    return best_seat


def set_begintime():
    time = 1541347200
    date = setting['date']
    if date == 'today' and datetime.datetime.now().hour < 22:
        time = 1541347200 - 3600 * 24
    date = datetime.datetime.strptime('2018-11-04', '%Y-%m-%d')
    sec = 86400
    now = datetime.datetime.now()
    begintime = time + sec * (now - date).days
    return begintime


def get_data_form(data_json):
    beginTime = setting['beginTime']
    duration = setting['duration']

    search_data_form = {
    'beginTime': set_begintime() + beginTime * 3600,
    'duration': duration * 3600,
    'num': 1,
    'space_category[category_id]' : 591,
    'space_category[content_id]' : '',
    }

    studyroom = setting["studyroom"]
    while(studyroom):
        if studyroom == "3S" or studyroom == "3s":
            seat = SEATS.t_s[setting["seat"]]
            search_data_form['space_category[content_id]'] = 31
            break
        elif studyroom == "3N" or studyroom == "3n":
            seat = SEATS.t_n[setting["seat"]]
            search_data_form['space_category[content_id]'] = 37
            break
        elif studyroom == "2S" or studyroom == "2s":
            seat = SEATS.s_s[setting["seat"]]
            search_data_form['space_category[content_id]'] = 36
            break
        elif studyroom == "2N" or studyroom == "2n":
            seat = SEATS.s_n[setting["seat"]]
            search_data_form['space_category[content_id]'] = 35
            break
        break
    
    data_form = {
    'beginTime': set_begintime() + beginTime * 3600,
    'duration': duration * 3600,
    'seats[0]': seat,
    'seatBookers[0]': json.loads(login.text)['id']
    }

    return data_form,search_data_form


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
data_form,search_data_form = get_data_form(data_json)


r = connecting(data_form)
preview = json.loads(r.text)
result = preview['DATA']['result']
while result == 'fail':
    logging.error(preview['DATA']['msg'])
    if '已经被其他人锁定或占用' in preview['DATA']['msg']:
        used_seats = search_used_seats()
        while(not used_seats):
            used_seats = search_used_seats()
        best_seat = get_best_seat(used_seats)
        data_form['seats[0]'] = best_seat
    r = connecting(data_form)
    print(r)
    preview = json.loads(r.text)
    result = preview['DATA']['result']


if result == 'success':
    logging.info("succeed!")









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
