import xml.etree.ElementTree as ET
import requests
import json
from os import path, chdir, environ

APIKEY = environ["SIMPLECAST"]
CASTID = "1105"

def get():
    junk =  requests.get("https://api.simplecast.com/v1/podcasts.json",auth=(APIKEY,''))
    decode = json.loads(junk.text)

    eyed = decode[0]['id']

    episodes = requests.get("https://api.simplecast.com/v1/podcasts/"+str(eyed)+"/episodes.json",auth=(APIKEY,''))
    decode = json.loads(episodes.text)

    ep = decode[5]
    print ep['title']
    epID = ep['id']
    print epID
    url = "https://api.simplecast.com/v1/podcasts/"+str(eyed)+\
                         "/statistics/episode.json?episode_id=" +\
                         str(epID) + "&timeframe=all"
    stats = requests.get(url,auth=(APIKEY,''))
    print stats.text

    url = "https://api.simplecast.com/v1/podcasts/"+str(eyed)+\
                         "/statistics/overall.json"
    stats = requests.get(url,auth=(APIKEY,''))
    print stats.text

def daySummary(pod, dateStart, dateEnd):
    """
    returns a dictionary in the form {'episode title' : listens}
    takes a given start and end date

    Recommended to not set large spans per call since each request to Simplecast
    had a tendency to return a server error if the return was too large
    """

    baseUrl = "https://api.simplecast.com/v1/podcasts/"+CASTID+\
                         "/statistics/episode.json?episode_id="
    timeframe = "&timeframe=custom&start_date="+dateStart+\
                "&end_date="+dateEnd
    
    #get episode ids
    resp= requests.get("https://api.simplecast.com/v1/podcasts/"+\
                       pod+"/episodes.json",auth=(APIKEY,''))

    res = []
    if resp.status_code == 404:
        return res
    episodes = json.loads(resp.text)
    total = 0
    count = 0
    for e in episodes:
        eyeD = str(e['id'])
        title = e['title']
        data = json.loads(requests.get(baseUrl+eyeD+timeframe,auth=(APIKEY,'')).text)
        listens = data['total_listens']
        if(listens != 0):
            res.append([title,listens])
            count += 1
            total += listens

    res.append(['Total', total])
    res.append(['Number of Episodes with listens', count])
    return res


