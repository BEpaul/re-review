# RE:Review - 감정분석을 활용한 리뷰 신뢰성 검증 프로그램

## 개요
무신사 플랫폼에서 별점은 상향평준화가 이루어져 소비자 입장에서 좋은 제품인지 아닌지 변별이 어렵습니다.  
그래서 **소비자에게 보다 도움이 되는 점수를 제공하자**는 취지에서 해당 프로젝트를 진행하게 되었습니다.

<br>

## 설치 방법
### 개발 환경
- `Svelte 4.2.7`
- `tailwindcss 3.4.3`
- `Daisyui 4.10.2`
- `FastAPI 0.110.3`
- `MySQL 8.3.0`

### 사용 방법
#### Frontend
```
cd frontend
npm install
npm run dev
```

#### Backend
데이터베이스 사용을 위해 MySQL 실행이 선행되어야 합니다. 그리고 `sql_app/database.py`에서 DB 로컬 서버 연동이 필요합니다.
```
cd backend
pip3 install
uvicorn main:app --reload
```

<br>

## 기능 설명
### 상품평 확인하기
<img width="350" alt="image" src="https://github.com/BEpaul/re-review/assets/104749551/e4697c20-799a-4c05-8055-b112e0e3c032">  

- DB에 해당 상품에 대한 분석 정보가 존재하는 경우
    - 저장된 값 출력
- DB에 해당 상품 정보가 없는 경우
    1. 실시간 크롤링
    2. 자연어 처리 학습 모델 적용
    3. 산출된 값 출력
    

<br>

### 키워드 검색하기
<img width="550" alt="image" src="https://github.com/BEpaul/re-review/assets/104749551/496a02dd-f4b9-4992-8482-376257706116">  

- 키워드: 리뷰의 특정 단어 빈도를 기반으로 한 측정
- 새롭게 산출된 점수를 기준으로 내림차순 출력

<br>

## 상세 설명
### 서비스 아키텍처
<img width="1000" alt="image" src="https://github.com/BEpaul/re-review/assets/104749551/c4f1aa36-e1ab-44bd-b1a6-c6980a1580ee">

<br>

### 데이터 수집
- BS4를 사용한 정적 크롤링
- Selenium을 활용한 동적 크롤링

### 자연어 처리 모델
- 데이터 전처리
    - Dataset Train : Test = 3 : 1
    - Labeling: 별점 3점을 기준으로 1(긍정), 0(부정) 부여
    - Mecab 라이브러리를 활용한 형태소 분석
- 분류 모델 학습
    - GRU 모델 활용 (`konlpy` 라이브러리 사용)
    - Embedding vector dimesion: 100
    - Hidden Unit: 128
    - Epoch: 15
    - 정확도: 0.92624