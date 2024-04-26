# list = ['좋아요', '따뜻함']
# fre_list = [0, 0]
# if '따뜻함' in list:
#     index = list.index('따뜻함')
#     fre_list[index] += 1
#     print('좋아요가 있습니다.')
# else:
#     print('좋아요가 없습니다.')

# print(fre_list)

keywords = [('가성비'), '편한', '편안한', '편해요', '트렌디', '트렌드', '가벼워요', '가볍다', '가벼움', '무거움', '무겁다', '무거워요'
                , '저렴하다', '저렴해요', '저렴', '싸다', '싸요', '비싸요', '비싸다', '운동', '스포츠', '산책용', '데이트', '출근', '직장'
                , '직장용', '회사', '무난', '예뻐요', '멋지다', '멋져요', '예쁘다', '예쁘네요', '이쁘다', '이쁘네요', '이쁨', '예쁨', '품질'
                , '귀엽다', '귀여워요', '귀여움', '얇아요', '얇다', '두껍다', '두꺼워요', '더워요', '덥다', '춥다', '추워요', '간단', '간단해요'
                , '꾸안꾸', '매력적', '부드러움', '부드러워요', '부드럽다', '푹신푹신', '따뜻함', '힙해요', '힙하다', '힙함', '핏이 좋아요'
                ]

print(len(keywords))
fre_list = [0] * len(keywords)
if '따뜻함' in keywords:
    index = keywords.index('따뜻함')
    fre_list[index] += 1
    print('있음')

max_value = max(fre_list)
max_index = fre_list.index(max_value)

print(keywords[max_index])