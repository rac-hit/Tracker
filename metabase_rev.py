import requests 
import pandas as pd

def meta_rev(x):
    res = requests.post('', 
                        headers = {"Content-Type": "application/json"},
                        json =  {"username": "", 
                                 "password": ""}
                       )
    assert res.ok == True
    token = res.json()['id']
    
    res = requests.post('https://relevel-metabase.herokuapp.com/api/card/100/query/json', 
                  headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token
                            }
                )
    
    data= pd.DataFrame(res.json())
    #print(data.head())
    revenue = 0
    for i in range (len(data['User Referral Codes - Re Ferrer → Referral Code'])):
        if(data['User Referral Codes - Re Ferrer → Referral Code'][i] == x):
            revenue = data['Sum of Orders → Final Amount'][i]
            return revenue
    return 0
