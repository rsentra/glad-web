from flask import flash, redirect, render_template, url_for,request,send_file,json,jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
from datetime import datetime,date

from .. import MyDateUtil as MyU  #자체 유틸리티 클래스 로딩
from .. import GladUtil as glad

from .. import db
from . import sales
import pandas as pd
from flask import current_app
from sqlalchemy import create_engine
import sys
import pymysql

EXCEL_EXTENSIONS=['xlsx','xsl']

getDT = MyU.getDateUtil()
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in EXCEL_EXTENSIONS

def getdata(by):
    fl='d:/글로벌/실적분석/곰스_2004.xlsx'
    df= pd.read_excel(fl,header=0)
    df['계약일자']=pd.to_datetime(df.계약일자,format='%Y-%m-%d')

    import datetime
    fr=pd.to_datetime('2020-04-01',format='%Y-%m-%d')
    to=pd.to_datetime('2020-04-30',format='%Y-%m-%d')
    cond2= (df.계약일자 >= fr) & (df.계약일자 <= to)
    if by=='brh':
        df2=pd.DataFrame(df[cond2].groupby(['지점'])['초회보험료'].agg('sum'))
    elif by=='day':
        df2=pd.DataFrame(df[cond2].groupby(['계약일자'])['초회보험료'].agg('sum'))
    else: return 'err'

    df2=df2.reset_index()
    return df2

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    
def getConnector():
    con_db = current_app.config['SQLALCHEMY_DATABASE_URI']
    con_db = con_db.rsplit('/')[len(con_db.rsplit('/'))-1]
    print('database ===== ' ,con_db)
    return pymysql.connect(host="localhost",user="glad",
             passwd="glad9",db=con_db)
    
def getSelects():
    results=[]
    db=getConnector()
    try:
        with db.cursor() as cursor:
            query="SELECT distinct year(계약일자),month(계약일자) FROM contracts order by 1 desc,2 desc ;"
            cursor.execute(query)
            records = cursor.fetchall()
 
        for row in records:
            results.append(str(row[0])+'.'+str(row[1]).zfill(2))
            # print('sql result----',row[0],row[1],results)
            
    except Exception as e:
        print("Error reading data from MySQL table", e)
    finally:
        db.close()
        return results    

def getDataframe(chk):
    results=[]
    db=getConnector()
    chk=chk.split('.')
    import datetime
    # print('param===',chk,int(chk[0]), int(chk[1]))
    d = datetime.date( int(chk[0]), int(chk[1]), 1)
    l_date= datetime.date(d.year+(d.month==12),(d.month+1 if d.month<12 else 1),1)-datetime.timedelta(1)
    
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:   
            query="SELECT * FROM contracts where 계약종류 in ('장기','생보') and 계약일자>='%s' and 계약일자 <= '%s' ;"%(d,l_date)
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            result = pd.DataFrame(result)
    except Exception as e:
        print("Error reading data from MySQL table", e)
    finally:
        db.close()
        return result  

def dfProc(df):
    df.loc[:,'월']=df.계약일자.map(lambda x: x[:7]+'월')
    df.loc[:,'계약일자']=pd.to_datetime(df.계약일자,format='%Y-%m-%d')
    df.rename(columns={'납입주기(방법)':'납입방법'}, inplace=True)
    temp = df.loc[df['납입방법']=='년납','초회보험료'] / 12
    df.loc[df['납입방법']=='년납','초회보험료'] = temp
    del temp
    temp = df.loc[df['납입방법']=='일시납','초회보험료'] / 10
    df.loc[df.납입방법=='일시납','초회보험료'] = temp
    del temp

    df.loc[:,'최종상태변경일']=pd.to_datetime(df.최종상태변경일,format='%Y-%m-%d')
    df.loc[:,'말일']=pd.to_datetime(df.계약일자.map(getDT.get_lastday))
    df.loc[:,'월말계약상태']= df.계약상태
    df.loc[df.말일 < df.최종상태변경일,'월말계약상태']='정상'
    df=df[df.월말계약상태=='정상']  #계약월 기준인 경우 계약월말 정상건만 추출
    df=glad.BrhConv(df,'지점그룹')
    df.loc[:,'영업일차']=df.계약일자.map(getDT.get_workdaysMonth)
    return df


def dfMake(maxDay):
    월=list(range(0,maxDay))
    일차=list(range(1,maxDay+1))
    실적= [0]* maxDay
    누계= [0]* maxDay
    dfd=pd.DataFrame()
    dfd=pd.DataFrame({'월':월,'일차':일차,'실적':실적,'누계':누계})
    return dfd

def workDates(dt):
    wd1=date(dt.year,dt.month,1)
    wd2=getDT.get_lastday(wd1)
    return getDT.get_workdates(wd1,wd2)

@sales.route("/line_chart", methods=['GET', 'POST'])
@login_required
def line_chart():
    values=[]
    labels=[]
    legend=''
    title="실적추세"
    # getDT = MyU.getDateUtil()
    maxDay=0  #최대영업일수
    workDateList=[] #당월의 영업일 list

    if request.method == 'POST': # submit
        legend = 'sales'
        #checkboxs = request.form.getlist('checkboxs')
        checkboxs = request.form.getlist('chkYm[]')
        name = request.form.get('Types')
        print('from req= ',checkboxs,name)
        
        dfList=[pd.DataFrame()]*len(checkboxs)
        i=0
        for chk in checkboxs:
            df=getDataframe(chk)
            df=dfProc(df)
            df2=df.groupby(['월','영업일차'])['초회보험료'].agg('sum')
            df2=df2.reset_index()
            dfList[i]=df2
            # li=list(df2.초회보험료)
            # values.append(li)   
            # la=list(df2.영업일차)
            # labels.append(la)
            maxDay=max(maxDay, df2.영업일차.max()) 
            if i==0:  #당월의 영업일 목록
               workDateList=workDates(df.계약일자[0])
            #    print(len(workDateList), workDateList)
            i = i + 1

        maxDay += 1   
        workDateList2=[]
        for x in workDateList:
            workDateList2.append(x.strftime('%Y-%m-%d') )

        #영업일 리스트가 적은 경우
        i = maxDay - len(workDateList2)
        if i  > 0:
            for k in range(1,i):
                dt=workDateList2[len(workDateList2)-1]
                workDateList2.append(dt)

        dfThis=pd.DataFrame()
        #dflist loop
        for seq, dfRow in enumerate(dfList):
            df_Temp = pd.DataFrame(dfRow.groupby(['월','영업일차'])['초회보험료'].agg('sum')).reset_index()  #집계
            df_Temp['초회보험료']=round(df_Temp['초회보험료']/ 1000,0)
            df_Temp['csum'] = df_Temp.groupby(['월'])['초회보험료'].cumsum()  #누계생성
            dfd = dfMake(maxDay)
            dfd['월']=df_Temp.월[0]   #컬럼 초기화
            dfd['실적']=0
            dfd['누계']=0
            # print('df_temp',seq, df_Temp)
            for seq1, row in enumerate(df_Temp.iterrows()):    # groupby df를 dfSum에 복사
                # print('m=',maxDay,'s=',seq1, row[1])
                dfd.iloc[seq1]=[row[1][0],row[1][1],row[1][2],row[1][3]]

            dfd['누계']=  dfd.실적.expanding().sum()  #빈 row의 값을 채움
            if seq==0:
                dfThis=dfd
            li=list(dfd.누계)
            values.append(li)   
            # la=list(dfd.일차)
            la=workDateList2
            labels.append(la)

        #당월분 추가--막대그래프용
        values.append(list(dfThis.실적))
        labels.append(workDateList2)
        
        # return render_template('sales/line_chart.html', values=values, labels=labels, legend=legend,title=title)
        return jsonify({'resdata':json.dumps({'data':values, 'labels':labels,'checks':checkboxs})})
    
    # db에서 년월 조회
    results=getSelects()
    return render_template('sales/line_chart.html', title=title,selects=results)    

def color_extreme(val):
    if val<0:
        return 'color: {}'.format('red')
    else:
        return 'color: {}'.format('black')

def make_clickable(val):
    # print('val=',val)
    # return '<a href="sales.brh_table?={}">{}</a>'.format(val,val)
    return '<a href=brh_table/{} target="_blank"> {} </a>'.format(val,val)
                    
@sales.route("/da_table", methods=['GET', 'POST'])
@login_required
def da_table():
    df=pd.DataFrame()
    if request.method == 'POST': # submit
        checkboxs = request.form.getlist('checkboxs')
        for chk in checkboxs:
            dfT=getDataframe(chk)
            dfT=dfProc(dfT)
            df= pd.concat([df,dfT])

        df=pd.DataFrame(df.groupby(['지점그룹','지점','월'])['초회보험료'].agg('sum'))
        df['초회보험료']=round(df['초회보험료']/ 1000,0)
        # pivot
        df = pd.pivot_table(df, values='초회보험료',
                       index=['지점그룹', '지점'],
                       columns=['월'],
                       fill_value=0, aggfunc=sum, dropna=True, )
        #subtotal, grand total
        df=pd.concat([
            d.append(d.sum().rename((k, 'Total')))
            for k, d in df.groupby(level=0)
            ]).append(df.sum().rename(('Grand', 'Total')))                       
        df=df.reset_index().sort_values(by=['지점그룹','지점'],ascending=[False,True])
        print('cols=',df.columns)
        col = []  #숫자컬럼만
        for i in df.columns:
            if not i in ['지점','지점그룹']:
                col.append(i)
        print('numeric cols===', col)
        #직영구성비
        dft=df[df.지점그룹=='Grand']
        df_jik= df[(df.지점그룹=='직영') & (df.지점=='Total') ]
        for i in col:
            df_jik[i]=round(float(df_jik[i])*100/float(dft[i]),0)
        df_jik['지점']='M/S'
        df=df.append(df_jik)

        df.reset_index(drop=True,inplace=True)

        # df_with_style=df.style.format(make_clickable,subset=pd.IndexSlice[:,'지점'])
        df_with_style = df.style.format(make_clickable)
        df_with_style = df_with_style.applymap(color_extreme,subset=pd.IndexSlice[:,col])
        ## data의 format을 변경할 때 
        for i in col:
            df_with_style = df_with_style.format({i:"{:,.0f}"})
        styles = [
        {'selector':'th', 'props':[('font-size', '12px'),('text-align', 'center'),('border','1px solid #7a7')]},
        {'selector':'td', 
         'props':[('text-align', 'right'), ('font-size', '12px'), ('height', '20px'), ('width', '100px')
            ,('border','1px solid #7a7')
         ]}, 
        {'selector':'tr', 'props':[('font-size', '12px'),('text-align', 'right'),('border','1px solid #7a7')]}
        ]
        df_with_style = df_with_style.set_table_styles(styles)

        ## html로 렌더링해주어야 함 
        return df_with_style.hide_index().render()


def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """

  if value < 0:
    color = 'red'
  elif value > 0:
    color = 'green'
  else:
    color = 'black'

  return 'color: %s' % color

@sales.route("/brh_table/<string:brh>", methods=['GET', 'POST'])
@login_required
def brh_table(brh):
    return redirect('/')

@sales.route('/bar_chart', methods=['GET', 'POST'])
@login_required
def bar_chart():
    title="지점별실적"
    values=[]
    labels=[]
    legend=''
    if request.method == 'POST': # submit
        legend = 'sales'
        checkboxs = request.form.getlist('chkYm[]')
        name = request.form.get('Types')
        print('from req= ',checkboxs,name)
        cols=['장기','생보']  #계약종류
        
        chk=checkboxs[0];  #첫번째 선택월만
        df=getDataframe(chk)
        df=dfProc(df)
        if name=='bar':
            df2=pd.pivot_table(df,index=['지점그룹','지점'],columns='계약종류',values='초회보험료'
                ,aggfunc=sum,fill_value=0).reset_index()

            for col in cols:
                li=list(round(df2[col]/1000))
                values.append(li)   
            la=list(df2.지점)
            labels.append(la)

        if name=='pie':   
            # df2=pd.pivot_table(df,index=['지점그룹','지점'],columns='계약종류',values='초회보험료'
            #     ,aggfunc=sum,fill_value=0).reset_index()

            df2=df[df.지점그룹=='직영'].groupby(['지점'])['초회보험료'].sum().reset_index().sort_values(by='초회보험료',ascending=False)
            df2['구성비']=round(df2.초회보험료*100/df2.초회보험료.sum(),1)
            li=list(df2['초회보험료'])
            values.append(li)   
            la=list(df2.지점)
            labels.append(la)

        print(values)
        print(labels)
        #당월분 추가--막대그래프용
        return jsonify({'resdata':json.dumps({'data':values, 'labels':labels,'checks':cols })})

    results=getSelects()
    return render_template('sales/bar_chart.html', title=title,selects=results)    

@sales.route('/pie_chart')
@login_required
def pie_chart():
    pie_labels = labels
    pie_values = values
    return render_template('sales/pie_chart.html', title='sales per branch',max=17000, values=pie_values, labels=pie_labels, colors=colors)

@sales.route('/manage_file', methods=['GET', 'POST'])
@login_required
def manage_file():
    """
    Edit a file
    """
    UPLOAD_ANAL_FOLDER= current_app.config['UPLOAD_ANAL_FOLDER']
    if request.method == 'POST': #파일첨부 submit
        gb = request.form.get('hiddenCnt','')
        print("gb=======",gb)
        if gb=='2':  #file to database
            result=fileToDatabase(request,UPLOAD_ANAL_FOLDER)
            flash(result)
            return render_template('sales/manage_file.html', title="File manage",gb="1")

        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
               filename = file.filename
               filesv= os.path.join(UPLOAD_ANAL_FOLDER, filename)
               file.save(filesv)
        import time
        abs_path = os.path.join(UPLOAD_ANAL_FOLDER)
        filelist = os.listdir(abs_path)
        full_list = [os.path.join(abs_path,i) for i in filelist]
        time_sorted_list = sorted(full_list, key=os.path.getmtime,reverse=True)
        filelist=[]
        datelist=[]
        for item in time_sorted_list:
            metadata = os.stat(item)
            filename=item.rsplit('\\')
            filename=filename[len(filename)-1]
            filedate=datetime.fromtimestamp(metadata.st_mtime).strftime('%Y-%m-%d-%H:%M')
            filelist.append(filename)
            datelist.append(filedate)

        filetable= dict(zip(filelist,datelist))
        if gb=='1':
           flash('...처리할 파일을 지정하고 처리버튼 클릭......')

        # return redirect(url_for('sales.manage_file',filelists=filelist))
        return render_template('sales/manage_file.html', title="File manage",filelists=filetable,gb="2")

    return render_template('sales/manage_file.html', title="File manage",gb="1")

#excel file to mysql with columns
def fileToDatabase(request,UPLOAD_ANAL_FOLDER):
    col=['지점','직할지점','팀','수금사원번호','수금사원명','증권번호','계약일자','보험사',
         '계약종류','상품종류','초회보험료','계약상태','납입회차','납입주기(방법)','최종상태변경일',
         '원수사성적','(신)글로벌성적','계약자','피보험자','최종납입년월','최종수금일']
    table_nm='contracts'

    try:
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI']+'?charset=utf8mb4')
        con=engine.connect()
        procs = request.form.getlist('procs')
        files = request.form.getlist('filenames')
        filetable= dict(zip(procs,files))
        print('ss==',procs,files,filetable)
        #for proc, filename in filetable.items():
        for proc, filename in zip(procs,files):
            if proc!='No Action':
                abs_path = os.path.join(UPLOAD_ANAL_FOLDER,filename)
                df= pd.read_excel(abs_path,header=0,encoding=sys.getfilesystemencoding())
                df= df[df.NO!='합계'][col]
            
            if proc=='Update data':   
                max_dt=df.계약일자.max()
                min_dt=df.계약일자.min()
                metadata = db.MetaData()
                test = db.Table(table_nm, metadata, autoload=True, autoload_with=engine)
                query = db.delete(test)
                query = query.where(db.and_(test.columns.계약일자 >= min_dt,test.columns.계약일자 <= max_dt))
                results = con.execute(query)

            if proc=='Insert data' or proc=='Update data':
                print('db procssing',proc,filename)
                df.to_sql(con=con, name=table_nm, if_exists='append')

    except :
        if not con.closed:
           con.close()     
        return 'db processing error'
    finally:
        if not con.closed:
           con.close()     
    return 'completed db processing......... '
