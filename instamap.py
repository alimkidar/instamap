import pandas as pd
import requests, json, time

headers = "User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"

def load_json(link, headers):
    flag = False
    while flag == False:
        try:
            req = requests.get(link, headers)
            flag = True
            time.sleep(0.01)
        except:
            time.sleep(2)
            print('Req. failed. Try again...')
    attemp = 0
    while req.status_code != requests.codes.ok:
        #Gagal
        if attemp < 5:
            req = requests.get(link, headers)
        else:
            req = 0
            break
    if req.status_code == requests.codes.ok:
        x = json.loads(req.text)
        # print ("OK.")
    else:
        x = 0
    return x

