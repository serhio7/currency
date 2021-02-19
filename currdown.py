#!/usr/bin/env python
import threading

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import time
from functools import reduce
import requests
import mysql.connector
from datetime import datetime 
import time
import requests
import json
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError

app = Flask(__name__)
CORS(app)

def Average(lst): 
        return reduce(lambda a, b: a + b, lst) / len(lst)

@app.route('/metrics')
def api_line():
   

    return ''


def generate_report():

    
    sams = []
    for elem in range(1,3):
        params =  {"coinId":"2",
          "currency":"1",
          "tradeType":"buy",
          "currPage":str(elem),
          "payMethod":"0",
          "acceptOrder":"-1",
          "country":"",
          "blockType":"general",
          "online":"1",
          "range":"0",
          "amount":""
        }
        url = "https://otc-api.huobi.com/v1/data/trade-market"
        
        payload={}
        headers = {
          'Cookie': '__cfduid=dbac236bce430f08b2bb4cc6589d5fb741612475945'
        }
        
        response = requests.request("GET", url, params = params,headers=headers, data=payload)
        
        samcont = response.json()['data']
        sams =  sams + samcont

    samsprice = [float(ofprice['price']) for ofprice in   sams]  

      
    
      
    # Driver Code 
    
    average = Average(samsprice) 

    
    url = "https://www.freeforexapi.com/api/live?pairs=USDRUB"
    
    payload={}
    headers = {
      'Cookie': '__cfduid=d3d0cb65d181dc02b527d0648e978833b1613406753'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    usdrub = response.json()['rates']['USDRUB']['rate']

    print(usdrub)
    
    
    
    
    
    
    

    params = (
    ('market', 'usdtrub'),
)

    response = requests.get('https://garantex.io/api/v2/trades', params=params)

    usdt_rub= float(response.json()[0]['price'])
    status = False
    while status == False:
        try:
            cnx=mysql.connector.connect(user='admin',password='several23',host='204.2.63.74',port=20666,database = 'currency')
            status = True
        except mysql.connector.Error as err:
            pass
    cursor=cnx.cursor()

    timeupd =datetime.now()
    
    

    
    
    sql = "INSERT INTO cur_rate (cny_usdt,usd_rub, btc_rub,time_rate) VALUES (%s, %s,%s,%s)"
    val = (average,	usdrub,	usdt_rub,timeupd)
    
    cursor.execute(sql, val)
    
    cnx.commit()




def _do_update():
    while True:
        generate_report()
        time.sleep(300)


if __name__ == '__main__':
    mThread = threading.Thread(target=_do_update)
    mThread.daemon = True
    mThread.start()

    app.run(host='0.0.0.0', port=9099)
