import json
import requests
import urllib
import pandas as pd
import re
from bs4 import BeautifulSoup

def itunes_api_search_encoder(d):
    s = ""
    for k, v in d.items():
        if k == "term":
            v.replace(" ", "+")
        
        s += k + "=" + v + "&"
    s = s[0:-1]
    return s
    
def itunes_api_song_parser(json_data):
    lst_in = json_data.get("results")
    lst_ret = []
    
    for d_in in lst_in:
        d_ret = {
            "title":     d_in.get("trackName"),
            "artist":    d_in.get("artistName"),
            "album":     d_in.get("collectionName"),
            "title":     d_in.get("trackName"),
            "id_track":  d_in.get("trackId"),
            "id_artist": d_in.get("artistId"),
            "id_album":  d_in.get("collectionId"),
            "no_disk":   d_in.get("discNumber"),
            "no_track":  d_in.get("trackNumber"),
            "url":       urllib.parse.unquote(d_in.get("trackViewUrl")),
        }
        lst_ret.append(d_ret)
        
    return lst_ret

review_data = []
review_texts = []
review_scores_texts = []
def main(appID):
    # アプリIDをキーにして各アプリのレビュー情報を取得する
    app_url = 'https://itunes.apple.com/jp/rss/customerreviews/id={}/json'.format(appID)
    app_res = requests.get(app_url)
    app_json_data = json.loads(app_res.text)
    # リンク情報を取得
    link_data = app_json_data['feed']["link"]
    # 最後のリンク情報を取得
    last_link = link_data[3]['attributes']['href']
    # リンクのページ数を取得
    if re.sub(r'\D', '', last_link[52:56]) == '':
        page_count = 0
    else:
        page_count = int(re.sub(r'\D', '', last_link[52:56]))
        print('レビューのページ数', page_count)
        # 最初の50件のレビューを取得
        for review in app_json_data['feed']['entry']:
            review_rating = review['im:rating']['label']
            review_id = review['id']['label']
            review_title = review['title']['label']
            review_content = review['content']['label']
            review_data.append([review_id, review_rating, review_title, review_content])
        # 残りのレビューを取得
        if page_count > 2:
            for page in range(2, page_count):
                res_url = 'https://itunes.apple.com/jp/rss/customerreviews/page=' + str(page)+'/id={}/sortby=mostrecent/xml?urlDesc=/customerreviews/id={}/json'.format(appID,appID)
                res = requests.get(res_url)
                res.encoding = "utf-8"
                soup = BeautifulSoup(res.text, 'xml')
                for i in range(len(soup.find_all('entry'))):
                    review_rating = soup.find_all('entry')[i].find_all('im:rating')[0].text
                    review_id = soup.find_all('entry')[i].find_all('id')[0].text
                    review_title = soup.find_all('entry')[i].find_all('title')[0].text
                    review_content = soup.find_all('entry')[i].find_all(type="text")[0].text
                    review_data.append([review_id, review_rating, review_title, review_content])
        elif page_count == 2:
            res_url = 'https://itunes.apple.com/jp/rss/customerreviews/page=2/id={}/sortby=mostrecent/xml?urlDesc=/customerreviews/id={}/json'.format(appID,appID)
            res = requests.get(res_url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'xml')
            for i in range(len(soup.find_all('entry'))):
                review_rating = soup.find_all('entry')[i].find_all('im:rating')[0].text
                review_id = soup.find_all('entry')[i].find_all('id')[0].text
                review_title = soup.find_all('entry')[i].find_all('title')[0].text
                review_content = soup.find_all('entry')[i].find_all(type="text")[0].text
                review_data.append([review_id, review_rating, review_title, review_content])
    for review in review_data:
            review_texts.append([review[1], review[3]])

    

    for review in review_data:
        if len(review[3]) > 15:
            review_scores_texts.append([review[1], review[3]])  

    
    return review_scores_texts
