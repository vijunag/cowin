import urllib, json
from twilio.rest import Client
from datetime import date, timedelta

def CheckSlots(client,day, from_whatsapp_number, to_whatsapp_number):
    today= date.today().strftime('%d/%m/%Y')
    resp=urllib.urlopen('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=%s'%day)
    data=json.loads(resp.read())

    total_avail=0
    hosp_list=[]
    for center in data['centers']:
        if center['fee_type'] == 'Free':
            continue
        hosp = center['name']
        for slot in center['sessions']:
            if slot["available_capacity"] >0 and slot['min_age_limit']<45:
                slot['name']=hosp
                slot['pin']=center['pincode']
                hosp_list.append(slot)
                total_avail = total_avail + slot['available_capacity']
#            print "**********************"
#            print "Hospital Name: ", hosp
#            print "Min Age: ", slot['min_age_limit']
#            print "Availability: ", slot["available_capacity"]
#            print "Date: ", slot["date"]
#            print "Vaccine: ", slot["vaccine"]
#            print "**********************"
    if total_avail > 0:
        client.messages.create(body='%d available: Hurry up'%total_avail,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)
    for hosp in hosp_list:
        print msg%(hosp['name'],hosp['pin'],hosp['date'],hosp['min_age_limit'],hosp['available_capacity'],hosp['date'],hosp['vaccine'])
        client.messages.create(body=msg%(hosp['name'],hosp['pin'],hosp['date'],hosp['min_age_limit'],hosp['available_capacity'],hosp['date'],hosp['vaccine']),
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)


client=Client()
# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:xxxxxxxxxx'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:xxxxxxxxxxx'

msg="""
   Hospital Name: %s
   Hospital Pin: %d
   Date: %s
   Age: %d
   Availability: %d
   Date: %s
   Vaccine: %s
"""

today = date.today()
CheckSlots(client, today.strftime('%d-%m-%Y'), from_whatsapp_number, to_whatsapp_number)
#for x in xrange(1,10):
#    print "Slots for %s"%today.strftime('%d-%m-%Y')
#    CheckSlots(client, today.strftime('%d-%m-%Y'), from_whatsapp_number, to_whatsapp_number)
#    today = today + timedelta(1)
