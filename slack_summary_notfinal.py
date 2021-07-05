import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from json import dumps
import pandas as pd
from slack import slack
from poc import poc_summary
from influencer import inf_summary 
from datetime import timedelta
from current_time import time_now

def summary():
    time_now()
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    summary = client.open('InfluencersDB').worksheet("Summary1")
    numerics = client.open('InfluencersDB').worksheet("Numerics")
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    vpm= client.open('InfluencersDB').worksheet("Video Performace Metrics")
    dnd = client.open('InfluencersDB').worksheet("DayonDay")
    #'''
    #Date, Time, DV, TV, IV, Total S, , CCU, TP, TR
    summ= str(numerics.cell(4, 2))
    summ= summ[12:-2]
    summ= int(float(summ))
    
    prevmid= str(numerics.cell(1, 8))
    print(prevmid)
    prevmid= prevmid[12:-2]
    prevmid= int(float(prevmid))

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
    #dnd.update_cell(summ+2, 1, today)
    
    time1= str(vpm.cell(2, 3))
    #print(time1)
    time1 = time1.split("'")
    time1= time1[1]
    summary.update_cell(summ+2, 2, time1)
    #dnd.update_cell(summ+2, 2, time1)
    
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
    
    #add total number of clicks of the entry mul sheet
    #add total number of atrributed sign ups of the entry mul sheet 
    tcem= str(numerics.cell(14, 2))
    tcem = tcem.split("'")[1]
    tcem = int(float(tcem))
    tc= str(summary.cell(summ+2, 7))
    tc = tc.split("'")[1]
    tc = int(float(tc))
    tcc = tcem +tc
    summary.update_cell(summ+2, 7, tcc)
    
    asuu= str(numerics.cell(15, 2))
    asuu = asuu.split("'")[1]
    asuu = int(float(asuu))
    asu= str(summary.cell(summ+2, 11))
    asu = asu.split("'")[1]
    asu = int(float(asu))
    aas = asuu +asu
    summary.update_cell(summ+2, 11, aas)

    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=mixpanel")
    summary.update_cell(summ+2, 12, df.shape[0])   
    
    revenue= str(numerics.cell(7, 2))
    revenue = revenue.split("'")[1]
    revenue= int(float(revenue))
    summary.update_cell(summ+2, 23, revenue)

    #Total Views, Total Clicks, T CTR, T Sign Ups
    
    total_views = str(summary.cell(summ+1, 6))
    total_views = total_views.split("'")[1]
    numerics.update_cell(9, 2, total_views)
    

    total_c = str(summary.cell(summ+1, 7))
    total_c = total_c.split("'")[1]
    numerics.update_cell(10, 2, total_c)

    total_ctr = str(summary.cell(summ+1, 8))
    total_ctr = total_ctr.split("'")[1]
    numerics.update_cell(11, 2, total_ctr)
        
    total_su = str(summary.cell(summ+1, 11))
    total_su = total_su.split("'")[1]
    numerics.update_cell(12, 2, total_su)
    #dayonday
    #call prev mid row and current summary row to perform subtractions 
    #current summary = summ + 1
    #call prev mid row on day on day to calculate next day on day
    sum1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=Summary1")
    prevmidrow = sum1.iloc[prevmid-1]
    currentrow = sum1.iloc[summ]
    
    ddsum1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1LsbFck7tqQWgqVx2UAOB8IUDDc9CdcCcq76m9zSELkE/gviz/tq?tqx=out:csv&sheet=DayonDay")
    prevmidrowdnd = ddsum1.iloc[prevmid-1]
    
    
    #Date	Time	Videos made live today	
    #PVideos made live today	Total views today	Total views today	
    #Total clicks today	Total clicks today	CTR for today 	CTR for today 	
    #Attributed sign ups today	Attributed sign ups today	Attributed registrations today	
    #Attributed registrations today	Attributed revenue today 	Attributed revenue today
    dnd.update_cell(summ+2, 1, today)
    dnd.update_cell(summ+2, 2, time1)
    
    videosmlt = currentrow[4] - prevmidrow[4]
    print(videosmlt)
    dnd.update_cell(summ+2, 3, int(videosmlt))
    pvideosmlt = (videosmlt - prevmidrowdnd[2])/ prevmidrowdnd[2]
    print(pvideosmlt)
    dnd.update_cell(summ+2, 4, float(pvideosmlt))
    
    viewsmlt = currentrow[5] - prevmidrow[5]
    dnd.update_cell(summ+2, 5, float(viewsmlt))
    pviewsmlt = (viewsmlt - prevmidrowdnd[4])/prevmidrowdnd[4]
    dnd.update_cell(summ+2, 6, float(pviewsmlt))
    
    cmlt = currentrow[6] - prevmidrow[6]
    dnd.update_cell(summ+2, 7, float(cmlt))
    pcmlt = (cmlt - prevmidrowdnd[6])/prevmidrowdnd[6]
    dnd.update_cell(summ+2, 8, float(pcmlt))
    
    c_ctr = currentrow[7]
    dnd.update_cell(summ+2, 9, c_ctr)
    currentrow1 = currentrow[7].split("%")[0]
    prevmidrow1 = prevmidrow[7].split("%")[0]
    cd_ctr = float(currentrow1) - float(prevmidrow1)
    cd_ctr = str(cd_ctr) + "%"
    dnd.update_cell(summ+2, 10, cd_ctr)
    
    dndasu = currentrow[10] - prevmidrow[10]
    dnd.update_cell(summ+2, 11, float(dndasu))
    pdndasu = (dndasu - prevmidrowdnd[10])/ prevmidrowdnd[10]
    dnd.update_cell(summ+2, 12, float(pdndasu))
    
    dndtp = int(currentrow[17] - prevmidrow[17])
    dnd.update_cell(summ+2, 13, float(dndtp))
    pdndtp = (dndtp - prevmidrowdnd[12])/ prevmidrowdnd[12]
    dnd.update_cell(summ+2, 14, float(pdndtp))
    
    dndrev = currentrow[22] - prevmidrow[22]
    dnd.update_cell(summ+2, 15, float(dndrev))
    pdndrev = (dndrev - prevmidrowdnd[14])/ prevmidrowdnd[14]
    dnd.update_cell(summ+2, 16, float(pdndrev))
    slack()
    #poc_summary()
    #inf_summary()
    #update previous values when time is midnight
    if(time1=="0"):
        #update all the old values
        #old videos
        numerics.update_cell(1, 8, summ+1)
        '''
        numerics.update_cell(1, 4, tvid)
        numerics.update_cell(6, 4, payments)
        numerics.update_cell(7, 4, revenue)
        
        spend= str(numerics.cell(8, 2))
        spend = spend.split("'")[1]
        spend= int(float(spend))
        numerics.update_cell(8, 4, spend)
        
        numerics.update_cell(9, 4, total_views)
        numerics.update_cell(10, 4, total_c)
        numerics.update_cell(11, 4, total_ctr)
        numerics.update_cell(12, 4, total_su)
        '''
    return
