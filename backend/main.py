from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import trange
import re
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

##### 모델링 #####
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from collections import Counter
from konlpy.tag import Mecab
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

### GRU 리뷰 감정 분석
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

### DB 연결
from pydantic import BaseModel
from sql_app.database import engineconn
from sql_app.models import Review_info, Test
from sqlalchemy import desc

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

def crawling_modeling(productName):
    # product_name = input("상품명을 입력하세요: ")
    product_name = productName
    product_name_url = quote_plus(product_name)

    search_url = f"https://www.musinsa.com/search/musinsa/integration?q={product_name_url}"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

    response = requests.get(search_url, headers=headers)
    html = BeautifulSoup(response.text, 'html.parser')

    product_url = html.select('p.list_info > a')[0]['href']

    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    service = Service(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 자동 업데이트
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 웹페이지 해당 주소 이동
    driver.get(product_url)
    style_review_text = driver.find_element(By.CSS_SELECTOR, '#estimate_style').text
    match = re.search(r'\(([\d,]+)\)', style_review_text)
    image_url = driver.find_element(By.CSS_SELECTOR, '#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-p62agb-0.daKJsk > div > img').get_attribute('src')
    print('image_url:', image_url)

    if match:
        style_review_count = int(match.group(1).replace(',', ''))
        print(f"스타일리뷰 개수: {style_review_count}")
    else:
        print("No match found.")

    time.sleep(0.1)

    # 리뷰 텍스트
    data = []
    count = 0
    while (True):
        try:
            position = count % 10 + 1
            rate = driver.find_element(By.CSS_SELECTOR, f'#reviewListFragment > div:nth-child({position}) > div.review-list__rating-wrap > span > span > span.review-list__rating__active').get_attribute('style').split(":")[1].split("%")[0]
            review = driver.find_element(By.CSS_SELECTOR, f'#reviewListFragment > div:nth-child({position}) > div.review-contents > div.review-contents__text').text
            
            review_text = re.sub(r'\n+', ' ', review)
            data.append(review_text)

            count += 1
            if count % 50 == 10:
                driver.find_element(By.CSS_SELECTOR, '#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > a:nth-child(4)').send_keys(Keys.ENTER)
            elif count % 50 == 20:
                driver.find_element(By.CSS_SELECTOR, '#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > a:nth-child(5)').send_keys(Keys.ENTER)

            if count >= style_review_count:
                break
            
            if count == 30:
                break

            time.sleep(0.05)
        except:
            print(f'error: no review data or page at count {count}')
            count += 1
            continue

    driver.quit()

    print("COMPLETE CRAWLING")

    total_data = pd.read_table('reviews.txt', names=['rate', 'review'])
    print('review datset count:', len(total_data))

    total_data['label'] = np.select([total_data.rate > 3], [1], default=0)

    total_data.drop_duplicates(subset=['review'], inplace=True) # reviews 열에서 중복인 내용이 있다면 중복 제거
    train_data, test_data = train_test_split(total_data, test_size = 0.25, random_state = 42)

    # 한글과 공백을 제외하고 모두 제거
    train_data['review'] = train_data['review'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    train_data['review'] = train_data['review'].replace('', np.nan)

    test_data.drop_duplicates(subset = ['review'], inplace=True) # 중복 제거
    test_data['review'] = test_data['review'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
    test_data['review'] = test_data['review'].replace('', np.nan) # 공백은 Null 값으로 변경
    test_data = test_data.dropna(how='any') # Null 값 제거

    mecab = Mecab()

    stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

    train_data['tokenized'] = train_data['review'].apply(mecab.morphs)
    train_data['tokenized'] = train_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])

    test_data['tokenized'] = test_data['review'].apply(mecab.morphs)
    test_data['tokenized'] = test_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])

    X_train = train_data['tokenized'].values
    y_train = train_data['label'].values
    X_test= test_data['tokenized'].values
    y_test = test_data['label'].values

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)

    threshold = 2
    total_cnt = len(tokenizer.word_index) # 단어의 수
    rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
    total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

    # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
    for key, value in tokenizer.word_counts.items():
        total_freq = total_freq + value

        # 단어의 등장 빈도수가 threshold보다 작으면
        if(value < threshold):
            rare_cnt = rare_cnt + 1
            rare_freq = rare_freq + value

    vocab_size = total_cnt - rare_cnt + 2

    tokenizer = Tokenizer(vocab_size, oov_token = 'OOV')
    tokenizer.fit_on_texts(X_train)

    max_len = 80
    loaded_model = load_model('best_model.keras')

    keywords = ['가성비', '편한', '편안한', '편해요', '트렌디', '트렌드', '가벼워요', '가볍다', '가벼움', '무거움', '무겁다', '무거워요'
                , '저렴하다', '저렴해요', '저렴', '싸다', '싸요', '비싸요', '비싸다', '운동', '스포츠', '산책용', '데이트', '출근', '직장'
                , '직장용', '회사', '무난', '예뻐요', '멋지다', '멋져요', '예쁘다', '예쁘네요', '이쁘다', '이쁘네요', '이쁨', '예쁨', '품질'
                , '귀엽다', '귀여워요', '귀여움', '얇아요', '얇다', '두껍다', '두꺼워요', '더워요', '덥다', '춥다', '추워요', '간단', '간단해요'
                , '꾸안꾸', '매력적', '부드러움', '부드러워요', '부드럽다', '푹신푹신', '따뜻함', '힙해요', '힙하다', '힙함', '핏이 좋아요'
                ]
    
    fre_list = [0] * len(keywords)

    def predict_review(new_sentence):
        new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
        new_sentence = mecab.morphs(new_sentence)
        new_sentence = [word for word in new_sentence if not word in stopwords]
        for sen in new_sentence:
            if sen in keywords:
                index = keywords.index(sen)
                fre_list[index] += 1
                break
        encoded = tokenizer.texts_to_sequences([new_sentence])
        pad_new = pad_sequences(encoded, maxlen = max_len)

        score = float(loaded_model.predict(pad_new))
        return score

    score_sum = 0
    for i, d in enumerate(data):
        score_sum += predict_review(d)

    max_value = max(fre_list)
    max_index = fre_list.index(max_value)
    keyword = keywords[max_index]
    avg_score = score_sum / len(data)

    return avg_score, image_url, keyword, product_url

def convert_to_rate(score):
    return str(round(score / 20 * 100, 2))

engine = engineconn()
session = engine.sessionmaker()

class Item(BaseModel):
    product_name: str
    image_url: str
    rate: float
    keyword: str

@app.get("/re-review/")
async def get_review(productName: str):

    get_db_data = session.query(Review_info).filter(Review_info.product_name.like(f'%{productName}%')).first()
    if get_db_data is None:
        avg_score, image_url, keyword, product_url = crawling_modeling(productName)
        rate = convert_to_rate(avg_score)
        response = {"productName": productName, "rate": rate, "imageUrl": image_url, "productUrl": product_url, "keyword": keyword}
        saved_data = Review_info(product_name=productName, image_url=image_url, product_url=product_url, rate=rate, keyword=keyword)
        session.add(saved_data)
        session.commit()

        return response
    else:
        response = {"productName": get_db_data.product_name, "rate": get_db_data.rate, "imageUrl": get_db_data.image_url, "productUrl": get_db_data.product_url, "keyword": get_db_data.keyword}

        return response
    
@app.get("/keyword/")
async def get_keyword(keyword: str):
    get_db_data_by_keyword = session.query(Review_info)\
                            .filter(Review_info.keyword\
                            .like(f'%{keyword}%'))\
                            .order_by(desc(Review_info.rate))\
                            .all()

    return get_db_data_by_keyword