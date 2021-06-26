from googleapiclient.discovery import build
from datetime import date
from datetime import datetime
from json import dumps

youtube = build('youtube','v3', developerKey="AIzaSyCjrL9Av17oQaowg-MQ7xUoksOeTZ-rnJ0") 

def scrap(url_id):  
    video_request=youtube.videos().list(
        part='snippet,statistics',
        id= url_id
        )
  
    video_response = video_request.execute()
    try:
        likes = int(video_response['items'][0]['statistics']['likeCount'])
    except:
        likes = 0
    try:
        dislikes= int(video_response['items'][0]['statistics']['dislikeCount'])
    except:
        dislikes= 0
    try:
        views = int(video_response['items'][0]['statistics']['viewCount'])
    except:
        views= 0
    today = date.today()
    today= today.strftime("%d/%m/%y")
    today = dumps(today).strip('"')
    now = datetime.now()
    time = now.strftime("%H")
    now = int(dumps(time).strip('"'))
    try:
        likesper= str(round((dislikes)/int(likes) *100)) + "%"
    except:
        likesper= 0    
    data = [today, now , views, likes, dislikes, likesper]
    return data
    
    