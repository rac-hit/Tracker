import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from json import dumps

def poc_summary():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    numerics = client.open('InfluencersDB').worksheet("Numerics")
    pocnumerics = client.open('InfluencersDB').worksheet("Team Performance Metrics")
    vpm= client.open('InfluencersDB').worksheet("Video Performace Metrics")
    
    psumm= str(numerics.cell(17, 2))
    psumm= psumm[12:-2]
    psumm= int(float(psumm))
    
    tpoc= str(numerics.cell(18, 2))
    tpoc= tpoc[12:-2]
    tpoc= int(float(tpoc))
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    
    time1= str(vpm.cell(2, 3))
    #print(time1)
    time1 = time1.split("'")
    time1= time1[1]

    for i in range(tpoc):
        pocnumerics.update_cell(psumm+1+i, 1, i+1) 
        pocnumerics.update_cell(psumm+1+i, 2, today)
        pocnumerics.update_cell(psumm+1+i, 3, time1)
    return 
    


