from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

# step2.크롤링할 url 주소를 입력한다. (네이버에서 코로나 검색 후, 뉴스 탭 클릭)
url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=코로나'

# step2-1.만약 다른 키워드를 매번 다르게 입력하고 싶다면 아래와 같이 하셔도 됩니다.
query = input('검색할 키워드를 입력하세요: ')
url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+'%s' % query
requests.get(url, headers={'User-Agent':'Mozilla/5.0'})

# step3.requests 패키지의 함수를 이용해 url의 html 문서를 가져온다.
response = requests.get(url)
html_text = response.text

# step4.bs4 패키지의 함수를 이용해서 html 문서를 파싱한다.
soup = bs(html_text, 'html.parser')

newsdbs = dict()

# 모든 info의 href 가져오기

infos = soup.select('a.info')
naver_news_links = []
naver_news_idenfier = 'n.news.naver.com'

for info in infos:
    link = info.attrs['href']
    if naver_news_idenfier in link:
        naver_news_links.append(link)

for naver_news in naver_news_links:
    print(naver_news)


for i, naver_news in enumerate(naver_news_links):
    newsdb = dict()
    naver_news_response = requests.get(naver_news, headers={'User-Agent':'Mozilla/5.0'})
    naver_news_html_text = naver_news_response.text
    naver_news_soup = bs(naver_news_html_text, 'html.parser')
    body = naver_news_soup.select('div._article_body')[0].get_text()
    text = re.sub(r'\<[^)]*\>','', body)
    # print(text)
    newsdb['title'] = '몰라'
    newsdb['text'] = text
    newsdbs[i] = newsdb


import json

with open("result.json", 'w') as file:
    json.dump(newsdbs, file,ensure_ascii=False, indent=4)     #ensure_ascii=False, indent=4   json파일에서 중요!
   




