#직영, 지사구분 리스트
GROUP1= ('엠피송내',     '엠피메트로', '엠피성공', '엠피의정부',
         '엠피여주',     '엠피레전드', '엠피라온',
         '엠피아이리치', 'HL지점'
        )
GROUP2= ('엠피조은',     '엠피상동',  '엠피피스토스', '엠피가온',
         '엠피프라임',   '엠피방이',  '엠피경기',
         '엠피제이엔제이',  '씨티엠지점', '엠피시흥'
        )

#메트로 코드 오류 보정
import pandas as pd
def Metro(brh,j_brh,team):
    if pd.isnull(team): team='00'
    if pd.isnull(j_brh): j_brh='00'
    if '시흥' in (team):         return '엠피시흥'
    elif '제이엔제이' in (j_brh):  return '엠피제이엔제이'
    elif '씨티엠' in (j_brh):       return '씨티엠지점'
    else: return brh

#1. 메트로 코드 분리.  2. 직영,지사구분값 (colNm에 생성)
def BrhConv(dfC,colNm):
    #---메트로 코드 분리
    dfC['지점'].fillna('엠피메트로', inplace=True)  #결측치 보정
    dfC.loc[:,'변환지점']=dfC.apply(lambda x: Metro(x['지점'], x['직할지점'], x['팀']), axis=1)
    dfC.rename(columns={'지점':'원지점','변환지점':'지점'},inplace=True)
    #---직영,지사 구분  => 속도느리면 df만들어 join할 것
    dfC.loc[:,colNm] = dfC.지점.map(lambda x: '지사'  if x in GROUP2 else ('직영' if x in GROUP1 else '오류'))
    return dfC

'''
str='엠피아이리치'
if str in GROUP1: print('직영')
elif str in GROUP2: print('직사')
else: print('err')
'''