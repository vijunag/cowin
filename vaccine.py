import urllib, json, time
from twilio.rest import Client
from datetime import date, timedelta
import requests, sys, argparse, os, datetime
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.cowin.gov.in',
    'Accept-Encoding': 'br, gzip, deflate',
    'If-None-Match': 'W/"24ee0-F1EQJcBUEPm7Mb6yjM/xe9PvIXc"',
    'Host': 'cdn-api.co-vin.in',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://www.cowin.gov.in/',
    'Connection': 'keep-alive',
}

params = (
    ('district_id', '294'),
    ('date', '07-05-2021'),
)

response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=07-05-2021', headers=headers)

def PushTelegramNotification(msg):
    files = {
       'chat_id': (None, '-1001458001301'),
       'text'   : (None, msg),
    }
    try:
        response = requests.post('https://api.telegram.org/bot1835927105:AAGODqdH14iQATaAVd-V0iZDdxMZaoUFHOw/sendMessage', files=files)
        return response
    except Exception as e:
        print("Error pushing notification: %s"%str(e))
        return None

def SendReqHeader(day):
    params = ( ('district_id', '294'), ('date',day))
    try:
        resp = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict', headers=headers, params=params)
        return resp.json()
    except Exception as e:
        print("Error: %s"%str(e))
        return None

def CheckSlots(day):
    data=SendReqHeader(day)
    if data is None:
        return False
    total_avail=0
    hosp_list=[]
    for center in data['centers']:
#        if center['fee_type'] == 'Free':
#            continue
        hosp = center['name']
        for slot in center['sessions']:
            if slot["available_capacity"]>0 and slot['min_age_limit']<45:
                slot['name']=hosp
                slot['pin']=center['pincode']
                hosp_list.append(slot)
                total_avail = total_avail + slot['available_capacity']
                print("**********************")
                print("Hospital Name: ", hosp)
                print("Fee Type: ", center['fee_type'])
                print("Pincode: ", slot["pin"])
                print("Min Age: ", slot['min_age_limit'])
                print("Availability: ", slot["available_capacity"])
                print("Date: ", slot["date"])
                print("Vaccine: ", slot["vaccine"])
                print("**********************")
    if total_avail > 0:
#        client.messages.create(body='%d available: Hurry up'%total_avail,
#                               from_=from_whatsapp_number,
#                               to=to_whatsapp_number)
        for hosp in hosp_list:
            print(msg%(hosp['name'],hosp['pin'],hosp['date'],hosp['min_age_limit'],hosp['available_capacity'],hosp['date'],hosp['vaccine']))
            PushTelegramNotification(msg%(hosp['name'],hosp['pin'],hosp['date'],hosp['min_age_limit'],hosp['available_capacity'],hosp['date'],hosp['vaccine']))

    return True

msg="""
   Hospital Name: %s
   Hospital Pin: %d
   Date: %s
   Age: %d
   Availability: %d
   Date: %s
   Vaccine: %s
"""

today = date.today() + timedelta(1)
dlst = [date.today() + timedelta(x) for x in range(4)]
while True:
  for t in dlst:
      CheckSlots(t.strftime('%d-%m-%Y'))
  time.sleep(15)
