from flask import flash, redirect, render_template, url_for,send_from_directory,request,send_file,jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from . import cars
from .forms import RegistrationForm
from .. import db
from ..models import Cars
from ..models import Employee,GladFc
from flask import current_app


@cars.route('/cars/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    add_cars=True
    usern=current_user.username
    form = RegistrationForm()
    if form.validate_on_submit():
        #처리자 지점값 설정
        usern=current_user.username
        employee = Employee.query.filter_by(username=usern).first()
        brh_name= getBrhName(employee.glad_id)

        #from Forms to columns
        cars=Cars()
        SetCars(cars,form,'n',brh_name)       
        cars.status = '요청'          
        # add cars to the database
        files = request.files.getlist('file')
        if files:
           filenm=uploads(files,cars.customer_name)
           cars.filename=filenm
           # print('files = ', cars.filename)
        db.session.add(cars)
        db.session.commit()

        # flash('You have successfully registered! cars!!.')
        # redirect to the page
        return redirect(url_for('cars.carslist'))

    # load registration template
    form.cov_object.default = '5천'   #초기값
    form.cov_self.default = '자신3'
    form.process()    #
    return render_template('cars/register.html', form=form, title='Register cars',add_cars=add_cars)

def getBrhName(glad_id):
    if glad_id==None:
        return 'None'
    if glad_id.startswith('MPK'):
       gladfc = GladFc.query.filter_by(glad_id=glad_id).first()
       brh_name= gladfc.glad_brh
    else: 
       brh_name = '본부'
    return brh_name 

@cars.route('/cars/carslist', methods=['GET', 'POST'])
@login_required
def carslist():
    """
    List all cars
    """
    # CARS_PER_PAGE=10
    CARS_PER_PAGE= current_app.config['CARS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    ##username으로 employee 테이블을 읽어 admin이 아닌 경우 본인건만 select
    usern=current_user.username
    employee = Employee.query.filter_by(username=usern).first()
    if employee.is_admin:  #admin는 all 권한
        cars = Cars.query.order_by(Cars.id.desc()).paginate(
            page, CARS_PER_PAGE, False)
    elif employee.role_id==1:  #지점장 or 실장은 자기지점만      
        brh_name= getBrhName(employee.glad_id)     
        cars = Cars.query.filter_by(brh_name=brh_name).order_by(Cars.id.desc()).paginate(
            page, CARS_PER_PAGE, False)
    else: 
        cars = Cars.query.filter_by(fc_id=usern).order_by(Cars.id.desc()).paginate(
            page, CARS_PER_PAGE, False)

    ##next,prev url은 미사용 --참고용으로 남겨놓음
    next_url = url_for('cars.carslist', page=cars.next_num) \
        if cars.has_next else None
    prev_url = url_for('cars.carslist', page=cars.prev_num) \
        if cars.has_prev else None        
    next_num= str(cars.next_num) + 'page'
    prev_num= str(cars.prev_num) + 'page'

    # cars = Cars.query.order_by(Cars.id.desc()).all()

    return render_template('cars/carslist.html',
                           cars=cars, title="carslist",next_url=next_url,
                           prev_url=prev_url,next_num=next_num,prev_num=prev_num)

@cars.route('/cars/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_car(id):
    """
    Edit a car
    """
    # check_admin()

    add_cars = False

    car = Cars.query.get_or_404(id)  #from table
    form = RegistrationForm(obj=car) #if not 404
    if form.validate_on_submit():
        SetCars(car,form,'u',"")
        car.updated = datetime.now()
        files = request.files.getlist('file')
        if files:
           filenm= uploads(files,car.customer_name)     
           car.filename=filenm
           #print('files = ', car.filename)
        db.session.commit()
        # flash('You have successfully edited the cars.')

        # redirect to the departments page
        return redirect(url_for('cars.carslist'))
    filenm=''
    if car.filename:
       filenm = 'attached img= ' + car.filename
    return render_template('cars/register.html', action="Edit",
                           add_cars=add_cars, form=form,
                           title="Edit car",filename=filenm)

@cars.route('/cars/update_car', methods=['GET', 'POST'])
def update_car():
    data={}  #empty dict
    data['id'] = request.args.get('id', 0, type=int)
    data['car_rcompany'] = request.args.get('rst_company', 0, type=str)
    data['car_rdate'] = request.args.get('rst_date', 0, type=str)
    data['status'] = request.args.get('status', 0, type=str)
    data['rt_cause'] = request.args.get('rt_cause', 0, type=str)
    # print(data['rt_cause'])
    car = Cars.query.get_or_404(data['id']) 
    if car: 
        if data['car_rcompany']:
           car.rst_company=data['car_rcompany']
        else: car.rst_company=None
        if data['car_rdate']:
           car.rst_date = data['car_rdate']
        else: car.rst_date=None           
        car.status = data['status']
        car.rt_cause = data['rt_cause']
        car.updated = datetime.now()
        db.session.commit()
    # print('upd============',data['id'],data['status'],data['car_rcompany'])
    # return jsonify(data)  #browser로 return
    return data  #browser로 return

def SetCars(car,form,gb,brh_name):
        car.company = form.company.data
        car.customer_name = form.customer_name.data
        car.customer_id = form.customer_id.data
        car.customer_telno = form.customer_telno.data
        car.customer_address = form.customer_address.data
        car.customer_job = form.customer_job.data
        car.customer_eq = form.customer_eq.data
        car.owner_name = form.owner_name.data
        car.owner_id = form.owner_id.data
        car.owner_telno = form.owner_telno.data
        car.owner_address = form.owner_address.data
        car.owner_job = form.owner_job.data

        car.car_no = form.car_no.data
        car.car_name = form.car_name.data
        car.car_code = form.car_code.data
        car.car_year = form.car_year.data
        car.car_acc = form.car_acc.data

        car.fc_id = form.fc_id.data
        car.proc_id = current_user.username
        car.description = form.description.data.encode('utf8')

        car.age_limit=form.age_limit.data
        car.driver_limit=form.driver_limit.data
        car.driver_id=form.driver_id.data
        car.driver_name=form.driver_name.data        
        car.cov_mandatory=form.cov_mandatory.data        
        car.cov_person=form.cov_person.data        
        car.cov_object =form.cov_object.data        
        car.cov_self =form.cov_self.data        
        car.cov_car =form.cov_car.data        
        car.cov_noncover  =form.cov_noncover.data        
        car.spc_emergency   =form.spc_emergency.data        
        car.spc_blackbox    =form.spc_blackbox.data   
        car.spc_mileage     =form.spc_mileage.data
        if gb=='n':
           car.created = datetime.now()
           car.brh_name= brh_name
        car.exp_date = form.exp_date.data
        return car


@cars.route('/cars/filedown/<string:filename>', methods=['GET', 'POST'])
def download_file(filename):	
    # UPLOAD_FOLDER='../uploads/'
    UPLOAD_FOLDER= current_app.config['UPLOAD_FOLDER']
    # UPLOAD_FOLDER= '../'+UPLOAD_FOLDER
    files = filename.split(',')
    for filenm in files:
        filepath= os.path.join(UPLOAD_FOLDER, filenm)
       # send_file(filepath, as_attachment=True)  ##-파일 즉시 다운
        print(UPLOAD_FOLDER,filenm)
        return send_from_directory(directory=UPLOAD_FOLDER, filename=filenm)	
    
def allowed_file(filename):
    # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_EXTENSIONS= current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploads(files,key):
    UPLOAD_FOLDER= current_app.config['UPLOAD_FOLDER']
    # file = request.files.getlist('file')
    result_nm=''
    if files: 
       for file in files:
           if allowed_file(file.filename):
#              filename = secure_filename(key+'_'+file.filename)
              filename = key+'_'+file.filename 
              filesv= os.path.join(UPLOAD_FOLDER, filename)
              file.save(filesv)
              if result_nm == '':
                  result_nm = filename
              else: 
                  result_nm += ','+ filename
        #return filename   #파일명만 저장
       return result_nm

@cars.route('/cars/fileupload', methods=['GET', 'POST'])
@login_required
def fileupload():	
    if request.method == 'POST':	
        f=request.files['file']	
        print('--------upload 11-',f.filename)	
        a=f.filename	
       # a = a.decode('cp949').encode('utf-8')	
        print('--------upload 11-1--',a)	
        f.save('./files/'+ secure_filename(a))	
        return redirect(url_for('blog.index'))	
       #return 'succ load'	
   	
    return render_template('uploads/fileupload.html')	