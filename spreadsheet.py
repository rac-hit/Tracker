import gspread
from oauth2client.service_account import ServiceAccountCredentials
from youtube_data import scrap
from rebrand import rebrand
from signups_through_gsheet import main_utm
from datetime import date
from datetime import datetime
from json import dumps
from current_time import time_now

def yt_data():
    time_now()
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    #ipm -> Influencer Performance Metrics
    #vdb -> Video Database
    #vpm -> Video Performace Metrics
    vdb= client.open('InfluencersDB').worksheet("Videos DB")
    vpm= client.open('InfluencersDB').worksheet("Video Performace Metrics")
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    now = datetime.now()
    time = now.strftime("%H")
    now = int(dumps(time).strip('"'))
    
    ipm.update_cell(1, 5, today)
    ipm.update_cell(1, 7, now)
    
    #total number of youtube videos in the sheet 
    video_number= str(vdb.cell(1, 2))
    video_number= video_number[12:-2]
    video_number= int(float(video_number))
    print(video_number)
    for i in range(video_number):
        #if i==159:
            #continue
        try:
            v_n= str(vdb.cell(i+3, 2))
            v_n = v_n.split("'")[1]
            v_n= int(float(v_n))
            inf= str(vdb.cell(i+3, 1))
            inf = inf.split("'")[1]
            inf= int(float(inf))
        except:
            continue
        #link of the youtube video extracted
        youtube_link= str(vdb.cell(i+3, 3))
        youtube_link = youtube_link.split(" ")[2]
        youtube_link = youtube_link[1:-2]
        x = youtube_link.split("=", 1)[1]
        print(x)
        rebrandly_link= str(vdb.cell(i+3, 4))
        #youtube data is scrapped from youtube_data
        data= scrap(x)
        clicks = rebrand(rebrandly_link)
        signups = main_utm(i)
        #insert video number into the data list
        #row heading --> Video ID,Date, Time, Total Views, Website Clicks, 
        #CTR, Likes, Dislikes, Dislikes/ Likes %age, Sign Ups
        data.insert(0, v_n)
        data.insert(4, clicks)
        ctr= str(round(((clicks)/int(data[3])*100), 2))
        ctr = ctr + "%"
        data.insert(5, ctr)
        data.insert(10, signups)
        data.insert(11, inf)
        #insert into the spreadsheet
        vpm.insert_row(data, 2)
    return

