from flask import flash, redirect, render_template, url_for,request,send_file,jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
from datetime import datetime


from .. import db
from . import sales
import pandas as pd
from flask import current_app
from sqlalchemy import create_engine
import sys
import pymysql

EXCEL_EXTENSIONS=['xlsx','xsl']

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
    return pymysql.connect(host="localhost",user="glad",
             passwd="glad9",db="glad_dev")
    
def getSelects():
    results=[]
    db=getConnector()
    try:
        with db.cursor() as cursor:
            query="SELECT distinct year(계약일자),month(계약일자) FROM contracts ;"
            cursor.execute(query)
            records = cursor.fetchall()
 
        for row in records:
            results.append(str(row[0])+'.'+str(row[1]).zfill(2))
            print('sql result----',row[0],row[1],results)
            
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
    print('param===',chk,int(chk[0]), int(chk[1]))
    d = datetime.date( int(chk[0]), int(chk[1]), 1)
    l_date= datetime.date(d.year+(d.month==12),(d.month+1 if d.month<12 else 1),1)-datetime.timedelta(1)
    
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:   
            query="SELECT * FROM contracts where 계약일자>='%s' and 계약일자 <= '%s' ;"%(d,l_date)
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            result = pd.DataFrame(result)
    except Exception as e:
        print("Error reading data from MySQL table", e)
    finally:
        db.close()
        return result  

@sales.route("/line_chart", methods=['GET', 'POST'])
@login_required
def line_chart():
    values=[]
    labels=[]
    legend=''
    title="지점별실적"
    if request.method == 'POST': # submit
        legend = 'sales'
        checkboxs = request.form.getlist('checkboxs')
        print('sss000011-------------------',checkboxs)
        for chk in checkboxs:
            print('sss',chk,bool(chk)) 
            df=getDataframe(chk)
            df2=df.groupby(['계약일자'])['초회보험료'].agg('sum')
            df2=df2.reset_index()
            li=list(df2.초회보험료)
            values.append(li)
            labels=list(df2.계약일자)
        
        print('val len========',len(values))
        return render_template('sales/line_chart.html', values=values, labels=labels, legend=legend,title=title)

    results=getSelects()
    print('sss======',results)
    return render_template('sales/line_chart.html', title=title,selects=results)    

@sales.route('/bar_chart')
@login_required
def bar_chart():
    df=getdata('brh')
    legend = 'sales'
    bar_labels=df.지점
    bar_values=df.초회보험료
    print("len=",len(bar_values))
    return render_template('sales/bar_chart.html', title='sales by branch',max=17000,labels=bar_labels, values=bar_values,legend=legend)


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
        for proc, filename in filetable.items():
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
                df.to_sql(con=con, name=table_nm, if_exists='append')

    except :
        if not con.closed:
           con.close()     
        return 'db processing error'
    finally:
        if not con.closed:
           con.close()     
    return 'completed db processing......... '
