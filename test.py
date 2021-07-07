import pandas as pd
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main_utm():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=mixpanel") 

    rebrandly_link = "https://relvl.co/f7p"
    print(rebrandly_link)
    domain_id= rebrandly_link[8:16]
    print(domain_id)
    slashtag = rebrandly_link[17:]
    print(slashtag)
    url = "https://api.rebrandly.com/v1/links/"
    
    headers = {
        "Accept": "application/json",
        "apikey": "4df8865745f54fa89d4ed08030c9d143",
    }
    
    querystring = {"domain.fullName" : domain_id, "slashtag" : slashtag}
    
    response = requests.request("GET", url, headers=headers, params= querystring)
    response = json.loads(response.text)
        
    
    url_id = url + response[0]['id']
        
    response_id = requests.request("GET", url_id, headers=headers)
    response_id = json.loads(response_id.text)
    destination = response_id['destination']
    
    #from here 
    destination = (destination.split("?"))[1]
    print(destination)
    destination = destination.split("&")
    print(destination)
    utm_term = ""
    utm_source = ""
    utm_medium= ""
    utm_campaign = ""
    for i in destination:
      utm = i.split("=")
      print(utm)
      if(utm[0] =="utm_term"):
        utm_term= utm[1]
      if(utm[0] =="utm_source"):
        utm_source= utm[1]
      if(utm[0] =="utm_medium"):
        utm_medium= utm[1]
      if(utm[0] =="utm_campaign"):
        utm_campaign= utm[1]
    ###
    print(utm_source)
    print(utm_medium)
    print(utm_campaign)
    print(utm_term)
    
    df1 = df[df['$properties.utm_term'] == utm_term]
    df1 = df1[df1['$properties.utm_source'] == utm_source]
    df1 = df1[df1['$properties.utm_medium'] == utm_medium]
    df1 = df1[df1['$properties.utm_campaign'] == utm_campaign]
    result = (len(df1))
    print(result) 

main_utm()
