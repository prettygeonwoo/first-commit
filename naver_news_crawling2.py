from bs4 import BeautifulSoup as bs         #웹에 있는 데이터를 가져와서 추출할 경우에 사용하는 외부 라이브러리
import requests
import re
import pandas as pd

# step2.크롤링할 url 주소를 입력한다. (네이버에서 코로나 검색 후, 뉴스 탭 클릭)
url = 'https://search.naver.com/search.naver?where=news&query=%ED%98%84%EB%8C%80%EC%B0%A8&sm=tab_opt&sort=0&photo=0&field=0&pd=5&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0'

# step2-1.만약 다른 키워드를 매번 다르게 입력하고 싶다면 아래와 같이 하셔도 됩니다.
query = input('검색할 키워드를 입력하세요: ')
url = 'https://search.naver.com/search.naver?where=news&query=%ED%98%84%EB%8C%80%EC%B0%A8&sm=tab_opt&sort=0&photo=0&field=0&pd=5&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1y&is_sug_officeid=0&query='+'%s' % query
requests.get(url, headers={'User-Agent':'Mozilla/5.0'})

# step3.requests 패키지의 함수를 이용해 url의 html 문서를 가져온다.
response = requests.get(url)  #url주소로 get요청 보내기
html_text = response.text     #text 속성을 통해 UTF-8로 인코딩된 문자열을 얻기

# step4.bs4 패키지의 함수를 이용해서 html 문서를 파싱(어떤 페이한지(문서,html)에서 내가 원하는 데이터를 특정 패턴이나 순서로 추출해 가공)다.
soup = bs(html_text, 'html.parser')

newsdbs = dict()

# 모든 info의 href 가져오기

infos = soup.select('a.info')
naver_news_links = []
naver_news_idenfier = 'n.news.naver.com'

#attr = 속성값 모두 출력
for info in infos:
    link = info.attrs['href']  
    if naver_news_idenfier in link:
        naver_news_links.append(link)

for naver_news in naver_news_links:
    print(naver_news)

#enumerate 함수 = 인덱스와 원소를 동시에 접근하면서 루프 돌리기 가능
# i = 0
# for naver_news in naver_news_links:
#     print(i,naver_news_links)
#     i += 1



for i, naver_news in enumerate(naver_news_links):
    newsdb = dict()
    navr_news_response = requests.get(naver_news,headers={'User-Agent':'Mozilla/5.0'})    #서버에서 봇으로 인지해서 원하는 정보를 주지 않고 차단 --> 해더를 추가해줌으로써 사람인걸 알려줌
    naver_news_html_text = naver_news_response.text
    naver_news_soup = bs(naver_news_html_text, 'html.parser')
        
    title = naver_news_soup.select('h2.media_end_head_headline')[0].get_text()          #
    date = naver_news_soup.select('div.media_end_head_info_datestamp')[0].get_text()
    body = naver_news_soup.select('div._article_body')[0].get_text()
    text1 = title
    text2 = re.sub(r'\<[^)]*\>','', body)           #<>안의 문자들 제거
    text3 = date
    newsdb['title'] = text1
    newsdb['text'] = text2
    newsdb['date'] = text3
    newsdbs[i] = newsdb

import json

with open("result.json", 'w') as file:
    json.dump(newsdbs, file,ensure_ascii=False, indent=4)     #ensure_ascii=False, indent=4   json파일에서 중요!

  
