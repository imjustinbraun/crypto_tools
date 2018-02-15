import datetime
import calendar
import requests
import csv


#######CONFIG######
baseUrl = 'https://api.gemini.com/v1/trades/'
symbol = 'ethbtc'
tradeLimit = 500


def get_start_time():
    today = datetime.date.today()
    week_ago = calendar.timegm((today - datetime.timedelta(days=6)).timetuple())
    return week_ago


def get_url(timestamp):
    url = baseUrl+symbol+'?timestamp='+str(timestamp)+'&limit_trades='+str(tradeLimit)
    print(url)
    return url


startTime = get_start_time()
startURL = get_url(startTime)
result = requests.get(startURL).json()
nextStartTime = startTime
csvfile = open(symbol+'.csv','w')
fieldnames = ['timestamp', 'type', 'qty', 'prc', 'tid']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

while nextStartTime < calendar.timegm(datetime.date.today().timetuple()):
    for ts in result:
        timestamp = ts['timestamp']
        if timestamp > nextStartTime:
            nextStartTime = timestamp

        type = ts['type']
        qty = ts['amount']
        prc = ts['price']
        tid = ts['tid']
        writer.writerow({'timestamp': timestamp, 'type': type, 'qty': qty, 'prc': prc, 'tid': tid})
        print(type + ',' + str(qty) + ',' + str(prc) + ',' + str(timestamp) + ',' + str(tid))

    url = get_url(nextStartTime)
    result = requests.get(url).json()
