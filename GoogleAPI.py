import requests
import matplotlib.pyplot as plt
import json
import appreview
import matplotScatter
import tqdm
import numpy as np

# APIを使うためのキー
key = 'AIzaSyB4iZ8c6vX_tsoZEGo8StNnEqcwBsXpm6A'
url = f'https://language.googleapis.com/v1beta2/documents:analyzeSentiment?key={key}'
header = {'Content-Type': 'application/json'}

# レビューテキストのAPI判別
"""
scoresは[{'magnitude':x,'score':y}]の形で渡される
"""
def Getscores(appID):
    scores = []
    for i in tqdm.tqdm(appreview.main(appID)):
        text = i[1]
        body = {
            "document":{
                "type":"PLAIN_TEXT",
                "language": "JA",
                "content":text
            },
            "encodingType":"UTF8"
        }
        res = requests.post(url, headers=header, json=body)
        score = res.json()['documentSentiment']
        scores.append(score)
    #print(scores)
    matplotScatter.swarmPlot(scores)
    #print(scores)
    #matplotbar.scoreplot(scores)

Getscores(497214545)
