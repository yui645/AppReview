import requests
import matplotlib.pyplot as plt
import json
import appreview
import matplotScatter
import tqdm
import numpy as np
import pandas as pd

# APIを使うためのキー
key = ''
url = f'https://language.googleapis.com/v1beta2/documents:analyzeSentiment?key={key}'
header = {'Content-Type': 'application/json'}

# レビューの評価とAPIのスコアの相関
"""
scoresは[{'magnitude':x,'score':y}]の形で渡される
"""

# 書き込むExcelファイルのパス指定
excel_path = "/Users/suenagayuinin/Horizon/appreview.xlsx"

def Getcorrelation(appID):
    # レビューの評価、APIのスコア、レビューテキスト
    review_data = []
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
        review_data.append([int(i[0]), score["score"], i[1]])

    # appレビューデータの整形
    sortReviewdata1 = sorted(review_data, reverse=True, key=lambda x:x[0])
    sortReviewdata2 = sorted(sortReviewdata1, reverse=True, key=lambda x:x[1])

    #print(correlation)

    # 相関係数と散布図の表示
    review_score = []
    API_score = []
    for i in review_data:
        review_score.append(i[0])
        API_score.append(i[1])
    print(np.corrcoef(review_score, API_score,rowvar=True))
    matplotScatter.correlationPlot(review_data)
    
    # Excelへのappレビューデータの書き込み
    #review = pd.DataFrame(sortReviewdata2)
    #review.to_excel(excel_path)

    
    

Getcorrelation(1068366937)
