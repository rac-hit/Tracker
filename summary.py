import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import datetime
from json import dumps
import pandas as pd

def summary():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    summary = client.open('InfluencersDB').worksheet("Summary1")
    numerics = client.open('InfluencersDB').worksheet("Numerics")
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    
    #Date, Time, DV, TV, IV, Total S, , CCU, TP, TR
    summ= str(numerics.cell(4, 2))
    summ= summ[12:-2]
    summ= int(float(summ))
    
    tvid= str(numerics.cell(1, 2))
    tvid= tvid[12:-2]
    tvid= int(float(tvid))
    summary.update_cell(summ+2, 5, tvid)
    
    dvid= str(numerics.cell(2, 2))
    dvid= dvid[12:-2]
    dvid= int(float(dvid))
    summary.update_cell(summ+2, 3, dvid)
    
    ivid= str(numerics.cell(3, 2))
    ivid= ivid[12:-2]
    ivid= int(float(ivid))
    summary.update_cell(summ+2, 4, ivid)
    
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    summary.update_cell(summ+2, 1, today)
    
    now = datetime.now()
    time = now.strftime("%H")
    summary.update_cell(summ+2, 2, time)
    
    total_inf= str(ipm.cell(1, 2))
    total_inf=total_inf[12:-2]
    total_inf= int(float(total_inf))
    
    coupon= str(numerics.cell(5, 2))
    coupon = coupon.split("'")[1]
    coupon= int(float(coupon))
    summary.update_cell(summ+2, 17, coupon)
    
    payments= str(numerics.cell(6, 2))
    payments = payments.split("'")[1]
    payments= int(float(payments))
    summary.update_cell(summ+2, 18, payments)
    
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=mixpanel")
    summary.update_cell(summ+2, 12, df.shape[0])   
    
    revenue= str(numerics.cell(7, 2))
    revenue = revenue.split("'")[1]
    revenue= int(float(revenue))
    summary.update_cell(summ+2, 23, revenue)
    return 
