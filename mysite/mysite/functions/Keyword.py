import requests
from bs4 import BeautifulSoup as bs
from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel
from mainpage.models import kwHistory

# 참조 : https://bab2min.tistory.com/544, 한국어 불용어 사전 100
stop_words = ['지난해', '올해', '시즌', '향후', '한국', 'kbo', '야구','게티이미지코리아', '게티이미지', '스포탈코리아',
              '연합뉴스', '유럽축구연맹', '국제축구연맹', '경기', '아시아축구연맹']

# url = "https://t1.daumcdn.net/cfile/tistory/241D6F475873C2B101"
model_type = 'skt/kobert-base-v1'

def get_soup(url): # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")

def modelLoad(model_type):
    model = BertModel.from_pretrained(f'{model_type}')
    kw_model = KeyBERT(model)
    return kw_model

def keywordExtract(keyBERT_model, text):
       keywords = keyBERT_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=stop_words, top_n=5, use_mmr=True)
       return keywords 

def textPreprocessing(text):
    kiwi = Kiwi()
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('NNP') or pos.startswith('SL'):
            results.append(token)
    results = ' '.join(results)
    return results

def getKwFromArticles(text):
    kw_model = modelLoad(model_type)
    keywords = []
    keyword = keywordExtract(kw_model, textPreprocessing(text))
    for kw in keyword:
        if kw[1] > 0.5:
            keywords.append(kw)
    return keywords

'''if __name__ == '__main__':
    t = kwHistory.objects.filter(keyword='이', datetime=0)
    print(t, len(t))'''