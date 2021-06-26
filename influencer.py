import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from json import dumps

def inf_summary():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    numerics = client.open('InfluencersDB').worksheet("Numerics")
    infnumerics = client.open('InfluencersDB').worksheet("Summary Influencers")
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    vpm= client.open('InfluencersDB').worksheet("Video Performace Metrics")
    
    psumm= str(numerics.cell(19, 2))
    psumm= psumm[12:-2]
    psumm= int(float(psumm))
    
    inf_number= str(ipm.cell(1, 2))
    inf_number= inf_number[12:-2]
    inf_number= int(float(inf_number))
    
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    
    time1= str(vpm.cell(2, 3))
    #print(time1)
    time1 = time1.split("'")
    time1= time1[1]

    for i in range(inf_number):
        infnumerics.update_cell(psumm+1+i, 1, today) 
        infnumerics.update_cell(psumm+1+i, 2, time1)
        infnumerics.update_cell(psumm+1+i, 3, i+1)
    return 
    





