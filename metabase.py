import requests 
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from metabase_rev import meta_rev

def meta():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    
    ########## METABASE CODE ###############
    
    res = requests.post('https://relevel-metabase.herokuapp.com/api/session', 
                        headers = {"Content-Type": "application/json"},
                        json =  {"username": "rachit@relevel.com", 
                                 "password": "YUBBHeQs5owV-0"}
                       )
    assert res.ok == True
    token = res.json()['id']
    
    res = requests.post('https://relevel-metabase.herokuapp.com/api/card/99/query/json', 
                  headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token
                            }
                )
    
    df= pd.DataFrame(res.json())
    inf_number= str(ipm.cell(1, 2))
    inf_number= inf_number[12:-2]
    inf_number= int(float(inf_number))
    #print(inf_number)
    for j in range(inf_number):
        print(j)
        ref_code = str(ipm.cell(j+3, 4))
        ref_code = ref_code.split(" ")[2]
        ref_code = ref_code[1:-2]
        total=0
        for i in range (len(df['User Referral Codes - Re Ferrer → Referral Code'])):
            if(df['User Referral Codes - Re Ferrer → Referral Code'][i] == ref_code):
                total = df['Count'][i]   
                break
        revenue = meta_rev(ref_code)
        ipm.update_cell(j+3, 5, int(total))
        ipm.update_cell(j+3, 7, int(revenue))
    return