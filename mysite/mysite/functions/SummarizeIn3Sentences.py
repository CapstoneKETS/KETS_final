import bs4.element
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import math
import numpy as np
from sklearn.preprocessing import normalize
from _datetime import datetime
from keybert import KeyBERT
from kiwipiepy import Kiwi
text = """
프리미어리그에서 맞대결을 펼친 손흥민(토트넘)과 황희찬(울버햄프턴)이 함께 입국했다.
하지만 두 선수는 시간차를 두고 입국장을 나와 사뭇 다른 풍경을 연출했다.
손흥민과 황희찬이 12일 오후 인천국제공항 제2터미널을 통해 입국했다.
같은 비행기를 타고 왔기 때문에 두 선수가 함께 나올 것이라고 예상 됐지만, 먼저 모습을 드러낸 선수는 손흥민이었다.
이날 입국장에는 수백명의 팬들이 두 선수의 모습을 지켜보기 위해 기다리고 있었다.
손흥민은 기다리고 있던 팬들을 향해 정중하게 인사한 후 밝은 표정으로 손을 흔들며 팬들과 인사를 나눴다.
하지만, 입국장은 손흥민 주위로 몰려든 팬으로 금세 북새통이 되고 말았다.
팬들 속에 파묻힌 손흥민은 연신 손을 흔들고 고개를 숙이며 입국장 밖에 주차된 차량으로 이동했다.
손흥민이 빠져나가자 입국장에 진을 치고 있던 인파의 수도 줄어들었다.
남은 팬들이 질서정연하게 기다리고 있는 가운데, 황희찬이 모습을 드러냈다.
황희찬은 곧바로 팬들에게 다가가 '즉석 팬사인회'를 시작했다.
황희찬은 통로를 반복해서 가로지르며 출구 양쪽에 도열한 팬들을 한 사람도 빼놓지 않고 사인과 기념촬영을 이어갔다.
덕분에 이날 마지막까지 기다린 팬들은 거의 모두 황희찬의 사인을 받을 수 있었다.
손흥민과 황희찬의 시간차 등장, 입국장을 혼란스럽게 하지 않으면서도 차분하게 팬서비스를 하기 위한 두 사람의 영리하면서도, 배려깊은 선택이었다.
손흥민, 황희찬은 지난 11일 영국 울버햄프턴 몰리뉴 스타디움에서 열린 잉글랜드 프리미어리그(EPL) 12라운드 경기에서 맞붙었다.
프리미어리그에서 뛰고 있는 두 사람의 첫 맞대결로 관심을 모은 이 대결에서 울버햄프턴이 2대1 역전승을 거뒀다.
하지만 이날 경기에서 두 사람 모두 상대 수비수의 집중적인 견제를 뚫지 못한 채 공격포인트를 올리지 못했다.
손흥민과 황희찬은 경기 전 손을 잡고 활짝 웃으며 인사를 나눴지만, 울버햄프턴의 극적인 역전승으로 희비가 엇갈렸다.
황희찬이 동료들과 얼싸안으며 승리의 기쁨을 만끽하는 사이 손흥민은 굳은 표정으로 경기장을 떠날 수밖에 없었다.
소속 리그에서는 적으로 만났지만, 대표팀에서 두 사람은 힘을 합쳐야 한다.
이날 함께 귀국한 두 사람은 클린스만 감독이 이끄는 대표팀에 합류해 16일(싱가포르)과 21일(중국)에 열리는 2026 북중미 월드컵 아시아 2차 예선전에 출격한다.
13일 소집되는 대표팀 선수들은 목동종합운동장에서 첫 훈련을 시작한다.
"""

def textrank(x, df=0.85, max_iter=50): # df = Dumping Factor : 0.85라고 가정, max_iter = 최대 반복횟수, 제한 조건을 두고 적절한 값에 수렴할떄까지 반복해야 하나 임의적으로 50회라고 지정
    assert 0 < df < 1

    # initialize
    A = normalize(x, axis=0, norm='l1')
    R = np.ones(A.shape[0]).reshape(-1, 1)
    bias = (1 - df) * np.ones(A.shape[0]).reshape(-1, 1)
    # iteration
    for _ in range(max_iter):
        R = df * (A @ R) + bias

    return R

def get_list(url): # 이 시각 많이 본 뉴스에서 리스트를 가져옴
    print(f"현재 시간은 {datetime.now()}입니다. 상위 10개의 기사를 조회합니다.")
    soup = get_soup(url)
    # news_list = soup.find('ol', attrs={"class" : "news_list"})
    news_list = soup.select('.news_list') # select를 써 본 기억이 없는것 같아 select로 구현
    news_link = {} # 딕셔너리로 선언
    for li in range(0, 8):
        print(f"{li+1}번 기사 : {news_list[0].findAll('a')[li].get_text()}")
        news_link[li] = news_list[0].findAll('a')[li].get('href')

    print("================================")

    checking_number = int(input("조회하고 싶은 기사를 입력하세요 : ")) # 조회를 원하는 기사 본문의 url 저장

    return "https://sports.news.naver.com/" + news_link[checking_number-1]


def get_soup(url): # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")

def get_content(soup):
    article = soup.find('div', attrs={"id": "newsEndContents"})
    for child in article.children: # 내부에 들은 텍스트를 제외한 자식 태그들(쓸모없는 정보들) 전부 처리
        if isinstance(child, bs4.element.Tag):
            child.decompose()
    content = article.text.replace("\n","")
    content = re.split("[\.?!]\s+", content) # 문장을 요소 단위로 분화, 문장 구분

    return content

def get_head(soup):
    head = soup.find('div', attrs={"class": "news_headline"})
    date_info = head.find('div', attrs={"class": "info"})

    print("기사 제목 : " + head.select_one('.title').get_text())
    print("기사 작성 시간 : " + date_info.select_one('span').get_text())

def get_keyword(content):
    keyword_model = KeyBERT()
    keywords = keyword_model.extract_keywords(content, top_n=5, stop_words='korean')
    return keywords

def get_nouns(text):
    kiwi = Kiwi()
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('NN'):
            results.append(token)
    return results

def summarize_text(content):

    data = []
    for text in content:
        if (text == "" or len(text) == 0):
            continue
        elif text == "All right reserved": # 기사가 끝났으면 반복문 종료
            break
        temp_dict = dict()
        temp_dict['sentence'] = text
        temp_dict['token_list'] = get_nouns(text)  # kiwi 형태소 분석으로 구분
        data.append(temp_dict)

    data_frame = pd.DataFrame(data)  # DataFrame에 넣어 깔끔하게 보기
    print(data_frame)
    print("================================")

    # 여기서부터
    # reference : https://hoonzi-text.tistory.com/68, 문서 요약 하기 (with textrank)
    # reference2 : https://lovit.github.io/nlp/2019/04/30/textrank/, TextRank 를 이용한 키워드 추출과 핵심 문장 추출 (구현과 실험)

    similarity_matrix = []
    for i, row_i in data_frame.iterrows():
        i_row_vec = []
        for j, row_j in data_frame.iterrows():
            if i == j:
                i_row_vec.append(0.0)
            else:
                intersection = len(set(row_i['token_list']) & set(row_j['token_list'])) # 유사도 계산의 분자 부분
                log_i = math.log(len(set(row_i['token_list'])))
                log_j = math.log(len(set(row_j['token_list'])))
                similarity = intersection / (log_i + log_j)
                i_row_vec.append(similarity)

        similarity_matrix.append(i_row_vec)

        weightedGraph = np.array(similarity_matrix)

    R = textrank(weightedGraph)

    R = R.sum(axis=1)

    indexs = R.argsort()[-5:] # 랭크값 상위 세 문장의 인덱스를 가져옴

    for index in sorted(indexs): # 뉴스 구조의 순서를 유지하기 위해 정렬함
        print(data_frame['sentence'][index])


if __name__ == '__main__':
    # url = get_list("https://sports.news.naver.com/wfootball/index")
    # soup = get_soup(url)
    # get_head(soup)
    # print("================================")
    # get_content(soup)
    # summarize_text(get_content(soup))

    text = text.split('\n')
    summarize_text(text)