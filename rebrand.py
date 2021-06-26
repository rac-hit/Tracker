import requests
import json

def rebrand(rebrandly_link):
    rebrandly_link = rebrandly_link.split(" ")[2]
    rebrandly_link = rebrandly_link[1:-2]
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
    return int(response_id['clicks'])
    #vpm.update_cell(2, 5, int(response_id['clicks']))
