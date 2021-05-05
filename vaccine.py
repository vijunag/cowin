import urllib, json
from twilio.rest import Client

client = Client() #WhatsApp Client
resp=urllib.urlopen('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=294&date=06-05-2021')
data=json.loads(resp.read())

total_avail=0
hosp_list=[]
for center in data['centers']:
    hosp = center['name']
    for slot in center['sessions']:
        if slot["available_capacity"] >0 and slot['min_age_limit']<=45:
            slot['name']=hosp
            hosp_list.append(slot)
            total_avail = total_avail + slot['available_capacity']
#            print "**********************"
#            print "Hospital Name: ", hosp
#            print "Min Age: ", slot['min_age_limit']
#            print "Availability: ", slot["available_capacity"]
#            print "Date: ", slot["date"]
#            print "Vaccine: ", slot["vaccine"]
#            print "**********************"

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+919844802808'

msg="""
Hospital Name: %s
Availability: %d
Date: %s
Vaccine: %s
"""

if total_avail > 0:
    client.messages.create(body='%d available: Hurry up'%total_avail,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
for hosp in hosp_list:
    print msg%(hosp['name'],hosp['available_capacity'],hosp['date'],hosp['vaccine'])
    client.messages.create(body=msg%(hosp['name'],hosp['available_capacity'],hosp['date'],hosp['vaccine']),
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
