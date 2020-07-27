import os
import re
import requests
import urllib.request

os.chdir(os.path.dirname(os.path.abspath(__file__)))

### Weather News ###
with open(r'..\settings\Weather_webscraping.ini') as f: # 個々人でsettings.iniの場所を指定する
    lines = f.readlines()
Weather_URL = lines[0].rstrip('\n')
msg = '\n'+'今日の天気予報です.' + '\n' + '\n' #r'\n'では改行不可

with urllib.request.urlopen(Weather_URL) as response:
    html = response.read().decode()
    seiki = r'<div class="weather-day__head">(.|\s)*?<div class="weather-day">'
    reseiki = re.search(seiki, html).group()
    time = re.findall(r'<p class="weather-day__time">((?:.|\s)*?)</p>', reseiki)
    rain = re.findall(r'<p class="weather-day__r">((?:.|\s)*?)</p>', reseiki)
    temp = re.findall(r'<p class="weather-day__t">((?:.|\s)*?)</p>', reseiki)

for i in range (0,len(time)): 
    if i == len(time)-1:
        msg = msg + time[i]+' ' + rain[i]+ ' ' + temp[i]
    else:
        msg = msg + time[i]+' ' + rain[i]+ ' ' + temp[i] + '\n'

### LINE Notify ###
line_notify_token = lines[1].rstrip('\n')
line_notify_api = 'https://notify-api.line.me/api/notify'
payload = {'message': msg}
headers = {'Authorization': 'Bearer ' + line_notify_token}  
line_notify = requests.post(line_notify_api, data=payload, headers=headers)