import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

def entry():
    scope= ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client= gspread.authorize(creds)
    
    entry= client.open('InfluencersDB').worksheet("Entry")
    entry_comp= client.open('InfluencersDB').worksheet("Entry Status")
    vdb= client.open('InfluencersDB').worksheet("Videos DB")
    ipm= client.open('InfluencersDB').worksheet("Influencer Performace Metrics")
    
    #check how many new entries are present
    entry_number= str(entry.cell(1, 2))
    entry_number= entry_number[12:-2]
    entry_number= int(float(entry_number))
    if(entry_number == 0):
        return
    #print(entry_number)
    for i in range(entry_number):
        #extract row coupon code -> unique value for Influencer
        entry_code= str(entry.cell(i+3, 5))
        #entry_code= entry_code[12:-2]
        entry_code = entry_code.split(" ")[2]
        entry_code = entry_code[1:-2]

        entry_reb= str(entry.cell(i+3, 4))
        entry_reb = entry_reb.split("'")[1]
        entry_reb = entry_reb.replace(" ", "")
        
        entry_you= str(entry.cell(i+3, 3))
        entry_you = entry_you.split("'")[1]
        entry_you = entry_you.split("&")[0]
        entry_you = entry_you.replace(" ", "")
        
        fixed= str(entry.cell(i+3, 7))
        fixed = fixed.split("'")[1]
        
        fixed= str(entry.cell(i+3, 7))
        fixed = fixed.split("'")[1]
        fixed = int(float(fixed))
        
        varia= str(entry.cell(i+3, 8))
        varia = varia.split("'")[1]
        #print(entry_reb)
        #case -> new influencer, new video
        #case -> old influencer, new video   
        #case -> old influencer, old video -> return status as Present
        
        flag_inf = 0
        flag_video = 0
        inf_channel= ""
        try:
            cell_inf = str(ipm.find(entry_code, in_column=4))
            #split in such a way that we get everything we need
            cell_inff = cell_inf.split('C')
            cell_inf = (cell_inff[1].split('R'))[1]
            cell_inf= int(float(cell_inf))
            
        except gspread.exceptions.CellNotFound:
            flag_inf=1
            
        try:
            cell_video = str(vdb.find(entry_reb, in_column=4))
            cell_videoo = cell_video.split('C')
            cell_video = (cell_videoo[1].split('R'))[1]
            cell_video= int(float(cell_video))
            print(cell_video)
        
        except gspread.exceptions.CellNotFound:
            flag_video=1
        
        #for new influencer
        if(flag_inf == 1):
            #enter into the ipm table
            inf_number= str(ipm.cell(1, 2))
            inf_number= inf_number[12:-2]
            inf_number= int(float(inf_number)) +1
            data = []
            #influencer id
            data.insert(0, inf_number)
            #influencer name
            inf_name = str(entry.cell(i+3, 1))[12:-2]
            data.insert(1, inf_name)
            #influencer channel
            inf_channel = str(entry.cell(i+3, 2))[12:-2]
            data.insert(2, inf_channel)
            #influencer coupon code
            data.insert(3, entry_code)
            ipm.insert_row(data, inf_number + 2)
            
        #for old influencer
        else:
            inf_number = str(ipm.cell(cell_inf, 1))
            inf_number = (inf_number.split('C'))[1]
            #inf_number = (inf_number[1].split('R'))[1]
            inf_number = int(float(inf_number[5:]))
            inf_number = inf_number -2
            inf_name = str(ipm.cell(cell_inf, 2))[12:-2]
            
        #for new video   
        status = ""
        if(flag_video==1):   
            #enter into the vdb table
            video_number= str(vdb.cell(1, 2))
            video_number= video_number[12:-2]
            video_number= int(float(video_number))+1
            data_vdb = []
            data_vdb.insert(0, inf_number)
            data_vdb.insert(1, video_number)
            data_vdb.insert(2, entry_you)
            data_vdb.insert(3, entry_reb)
            if(str(entry.cell(i+3, 6))[12:-2] == '1'):
                type= 1
            else:
                type= 0
            data_vdb.insert(4, type)
            data_vdb.insert(5, fixed)
            data_vdb.insert(6, varia)
            vdb.insert_row(data_vdb, video_number)
            status= "Completed"
        #for old video
        else:
            status = "Repeated"
            video_number = 0
            
        if(i%4 == 0):
            time.sleep(20)
            #insert entry into entry status sheet 
        #data_entry= []
        #data_entry.insert(0, inf_name)
        #data_entry.insert(1, inf_channel)
        #data_entry.insert(2, entry_you)
        #data_entry.insert(3, entry_reb)
        #data_entry.insert(4, entry_code)
        #changes as per condition
        #data_entry.insert(5, status)
        #data_entry.insert(6, video_number)
        #entry_comp.insert_row(data_entry, 2)
    entry.delete_rows(3, entry_number+ 3)
    return 



