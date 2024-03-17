from kiwipiepy import Kiwi
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import math
import numpy as np
from sklearn.preprocessing import normalize
from _datetime import datetime
import bs4

kiwi = Kiwi(model_type='knlm')
kiwi.add_user_word('발락', 'NNP', 0)

#print(*kiwi.analyze('손흥민의'), sep='\n')

def quotation_preprocess(sen): # 인용절 속 종결 기호를 마킹
    alphabet_list = []
    in_quotation = 0  # 문장 마침 기호가 인용문에 있는지
    in_SB = 0 # 문자가 대괄호 안에 있는지
    
    for a in sen:
        if ((a == '\"') | (a == '\'')) & (in_quotation == 0): # 쿼테이션 열림
            in_quotation = 1
        elif ((a == '\"') | (a == '\'')) & (in_quotation == 1): # 쿼테이션 닫힘
            in_quotation = 0
        if a == '[': # 대괄호 열림
            in_SB = 1
        elif a == ']': # 대괄호 닫힘
            a = ""
            in_SB = 0

        if in_SB == 1: #대괄호 안에 있는 문자 삭제
            a = ""
        if (a == '.') & (in_quotation == 1):
            a = '<spot>'
        if (a == '!') & (in_quotation == 1):
            a = '<exclamation>'
        if (a == '?') & (in_quotation == 1):
            a = '<question>'
        if (a == ';') & (in_quotation == 1):
            a = '<semicolon>'
        if (a == '\\') & (in_quotation == 1):
            a = '<backslash>'
            
        alphabet_list.append(a)
    
    return ''.join(alphabet_list)

def quotation_postprocess(text): # 마킹한 종결 기호를 원래대로
    for i in range(len(text)):
        text[i] = text[i].replace("<spot>", '.')
        text[i] = text[i].replace("<exclamation>", '!')
        text[i] = text[i].replace("<question>", '?')
        text[i] = text[i].replace("<semicolon>", ';')
        text[i] = text[i].replace("<backslash>", '\\')

    return text

def textPreprocessing(text):
    text = quotation_preprocess(text)
