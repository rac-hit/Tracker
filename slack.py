import requests 
import json 
import gspread
import pandas as pd
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials
from json import dumps

def slack():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
        
    vpm= client.open('InfluencersDB').worksheet("Video Performace Metrics")
    
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    print(today)
    
    time1= str(vpm.cell(2, 3))
    time1 = time1.split("'")
    time1= time1[1]
    print(time1)
    
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=DayonDay")
    df = df.iloc[-1]
        
    notif= 'Metrics for ' + str(today) +' ' + str(time1) + ':00'+ '\n' + 'Videos made live today: ' + str(df[2]) + ' ' + '(' + str(df[3]) + ')' + '\n' + 'Total views today: ' + str(df[4]) + ' (' + str(df[5]) + ')' + '\n' + 'Total clicks today: ' + str(df[6]) + ' (' + str(df[7]) + ')' + '\n' + 'CTR for today: ' + str(df[8]) + ' (' + str(df[9]) + ')' + '\n' + 'Attributed sign ups today: ' + str(df[10]) + ' (' + str(df[11]) + ')' + '\n' + 'Attributed registrations today: ' + str(df[12]) + ' (' + str(df[13]) + ')' + '\n' + 'Attributed revenue today: ' + str(df[14]) + ' (' + str(df[15]) + ')' + '\n'
    #+ 'Net spend today '  + str(df[14]) + ' (' + str(df[15]) + ')'+ '\n'
    print(notif)
    msg = {'text': notif}
    requests.post(web_hook_url, data=json.dumps(msg))
    return




