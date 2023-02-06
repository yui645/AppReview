#appreview.pyの「残りのレビューを取得」以下

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
    