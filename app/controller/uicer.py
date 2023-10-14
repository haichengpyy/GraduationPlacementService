from flask import Blueprint, render_template, request, jsonify, redirect, url_for,flash
from  datetime import datetime
from app.controller.offer import add_offer
from app.models.base import db
from app.models.offer import Offer
from app.models.uicer import UICer
from sqlalchemy import or_, and_, all_, any_,func,extract
import re

uicerBP = Blueprint('uicer', __name__)


@uicerBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_uicer.html', title='Sample Login', header='Sample Case')

    else:

        ID = request.form.get('stuID')
        _password = request.form.get('password')

        print(ID, _password)

        if ID.isdigit():  # 并不严谨，仅作测试，应该用正则
            result = UICer.query.filter(and_(UICer.stuID == ID, UICer._password == _password)).first()
            # tr = TimetableRecord.query.filter(and_(TimetableRecord.tid==tid, TimetableRecord.day == day,TimetableRecord.status!=2)).first()
            # print(result.verify())
            stu = UICer.query.filter(UICer.stuID == ID).first()
            if stu == None:

                return render_template('login_uicer.html', title='Sample Login', header='Sample Case',reminder1 = 'no such student')
        else:
            return render_template('login_uicer.html', title='Sample Login', header='Sample Case',reminder2 = 'wrong input number')

        if result:
            return redirect(url_for('uicer.homepage',stuid = result.stuID))
        else:

            return render_template('login_uicer.html', title='Sample Login', header='Sample Case',reminder = 'wrong pass')


@uicerBP.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Sample Login', header='Sample Case')
    ID = request.form.get('stuID')
    gender = request.form.get('gender')
    start = request.form.get('start_time')
    graduate = request.form.get('graduate_time')
    password = request.form.get('password')
    name = request.form.get('uname')
    repass = request.form.get('repassword')
    #email = request.form.get('email')
    gpa = request.form.get('gpa')
    print(ID, password, name, repass, gpa)
    value = re.compile('^[0-4]|^[0-3]\.\d|^4.0')
    if not ID.isdigit():
        reminder = 'wrong student number!'
        return render_template('register.html', title='Sample Login', header='Sample Case', reminder0=reminder)

    if graduate:
        if int(graduate) - int(start) != 4:
            reminder = 'wrong graduate year!'
            return render_template('register.html', title='Sample Login', header='Sample Case', reminder1=reminder)

    if password != repass:
        reminder = 'wrong password!'
        return render_template('register.html', title='Sample Login', header='Sample Case', reminder2=reminder)
    result = UICer.query.filter(UICer.stuID == ID).first()
    if result:

        reminder = "already exist student!"
        return render_template('register.html', title='Sample Login', header='Sample Case', reminder3=reminder)

    elif password == repass:
        matchit = value.match(gpa)
        if gpa == '' :
            gpa = '0'
        elif not matchit:
            reminder = "wrong input GPA!"
            return render_template('register.html', title='Sample Login', header='Sample Case', reminder4=reminder)

        new = UICer(ID, name, password, gpa, 'not required', start, gender)
        if graduate:
            new.graduete_year(graduate)
        db.session.add(new)
        db.session.commit()
        reminder = 'succussful'
        print(reminder)
        return render_template('register.html', title='Sample Login', header='Sample Case',reminder = reminder)

@uicerBP.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')
    if request.method == 'GET':
        print(name)
        return render_template('change_pass.html', title='Sample Login', header='Sample Case', stuid=stuid,
                               stuname=name)

    print(stuid, request.args)
    bpass = request.form.get('beforepassword')
    password = request.form.get('password')
    repss = request.form.get('repassword')
    result = UICer.query.filter(UICer.stuID == stuid).first()
    print(type(result))
    if bpass != result.view_password():
        return 'wrong password!'

    if password != repss:
        return 'wrong second input password!'
    elif password == repss:
        result.change_password(password)
        db.session.commit()
    return redirect(url_for('uicer.login'))


@uicerBP.route('/search_admission', methods=['GET', 'POST'])
def search_admission():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')
    if request.method == 'GET':
        return render_template('search_admission.html', title='Sample Login', header='Sample Case',stuid=stuid,
                                   stuname=name)
    else:
        gpa = request.form.get('input_gpa')
        uni_name = request.form.get('uni_name')
        if gpa=='' and uni_name=='':
            reminder = 'Please input GPA or university!'
            return render_template('search_admission.html', title='Sample Login', header='Sample Case',
                                   stuid=stuid, reminder=reminder,
                                   stuname=name)
        table_head = ['University Name', 'Program Name', 'GPA']
        info=[]
        value = re.compile('^[0-4]|^[0-3]\.\d|^4.0')
        matchit = value.match(gpa)
        if uni_name =='' and gpa!='':


            if not matchit:
                reminder = "wrong input GPA!"
                return render_template('search_admission.html', title='Sample Login', header='Sample Case', info=info,
                                stuid=stuid, reminder=reminder,
                                stuname=name)
            gpa = float(gpa)
            result1 = db.session.query(Offer.University_name, Offer.Program_name, UICer.GPA).join(UICer).filter(
                UICer.GPA >= gpa - 0.15, UICer.GPA <= gpa + 0.15).order_by(Offer.University_name,Offer.Program_name,Offer.GPA).distinct().all()
            print(result1)
            if not result1:
                reminder = 'Sorry, no information for GPA '+str(gpa)
                table_head = []
            else:
                info = []
                for i in result1:
                    info.append(list(i))
                reminder = 'Information for GPA around '+str(gpa)

        if uni_name !='' and gpa=='':
            result2 = db.session.query(Offer.University_name, Offer.Program_name, UICer.GPA).join(UICer).filter(
                Offer.University_name == uni_name).order_by(Offer.University_name,Offer.Program_name,Offer.GPA).distinct().all()
            print(result2)
            if not result2:
                reminder = 'Sorry, no information for university: '+uni_name
                table_head = []
            else:
                info = []
                for i in result2:
                    print(list(i))
                    info.append(list(i))

                reminder = 'Information for university: '+uni_name
                print(info)

        if uni_name != '' and gpa != '':
            if not matchit:
                reminder = "wrong input GPA!"
                return render_template('search_admission.html', title='Sample Login', header='Sample Case', info=info,
                                stuid=stuid, reminder=reminder,
                                stuname=name)
            gpa = float(gpa)
            result3 = db.session.query(Offer.University_name, Offer.Program_name, UICer.GPA).join(UICer).filter(
                UICer.GPA >= gpa - 0.15, UICer.GPA <= gpa + 0.15,Offer.University_name == uni_name).order_by(
                Offer.University_name,Offer.Program_name,Offer.GPA).distinct().all()
            #print(result3[0].University_name)
            if not result3:
                reminder = 'Sorry, no information for the input'
                table_head =[]
            else:
                info = []
                for i in result3:
                    info.append(list(i))
                reminder = 'Information for university: '+uni_name+' && GPA around '+str(gpa)
        return render_template('search_admission.html', title='Sample Login', header='Sample Case', info=info,
                                   stuid=stuid,reminder = reminder,table_head=table_head,
                                   stuname=name)

@uicerBP.route('/provide_offer', methods=['GET', 'POST'])
def provide_offer():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')
    info = request.args.get('info')
    print(info)
    if request.method == 'GET':
        return render_template('provide_offer.html', title='Sample Login', header='Sample Case', stuid=stuid, stuname=name)
    else:
        date = request.form.get('date')
        gpa = request.form.get('gpa')
        uni = request.form.get('uni')
        pro = request.form.get('pro')
        #title = request.form.get('title')
        title = 'not know'
        type = request.form.get('type')
        comp = request.form.get('comp')
        if date  and uni and pro and title and type:
            print(date, stuid, uni, pro, title, type, comp)
            result = UICer.query.filter(UICer.stuID == stuid).first()
            if not result:
                return 'NO such ID! Please input your correct ID'
            if type == 'company' and not comp:
                return 'Unsuccessful Operation! Company Offer Should Input Company Name! Please Try Again~'
            if not result.GPA:
                if not gpa:
                    return 'no gpa'
                else:
                    result.GPA = gpa
                    db.session.commit()
            else:
                gpa = result.GPA

            add_offer(date, stuid, uni, pro, title, type, comp, gpa)
            #return 'Add offer information successfully!'
        return render_template('provide_offer.html', title='Sample Login', header='Sample Case', stuid=stuid, stuname=name, reminder = 'succussfully uploaded!')

@uicerBP.route('/report', methods=['GET', 'POST'])
def report():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')

    if request.method == 'GET':
        return render_template('report.html', title='Sample Login', header='Sample Case', stuid=stuid,
                               stuname=name, reminder = '')
    else:
        year = request.form.get('year')  # 需要查询的内容
        reminder = ''
        if year is None:
            reminder = 'please select year'

        datetime_object = datetime.strptime(year, '%Y')
        print(year,datetime_object.year,type(datetime_object))

        result1 = db.session.query(Offer.University_name, Offer.Program_name, Offer.GPA, func.avg(Offer.GPA),func.min(Offer.GPA),func.max(Offer.GPA),func.count(Offer.GPA)).filter(extract('year', Offer.Date) == datetime_object.year).group_by(Offer.University_name, Offer.Program_name)
        result2 = db.session.query(Offer.University_name, Offer.Program_name, Offer.GPA, func.min(Offer.GPA)).filter(extract('year', Offer.Date) == datetime_object.year).group_by(Offer.University_name, Offer.Program_name)
        result3 = db.session.query(Offer.University_name, Offer.Program_name, Offer.GPA, func.max(Offer.GPA)).filter(extract('year', Offer.Date) == datetime_object.year).group_by(Offer.University_name, Offer.Program_name)

        if result1.first():
            print(result1.first())
            table_head = ['University Name','Program Name','Average GPA', 'Minimum acceptable GPA', 'Maximum acceptable GPA','Receiving Number']
            reminder = 'Here is one report for year '+str(year)
            return render_template('report.html', title='Sample Login', header='Sample Case', stuid=stuid,
                                   stuname=name,yearly = result1,table_head = table_head,reminder = reminder)
        else:
            reminder = 'Sorry, no report for this year!'
    #return redirect(url_for('uicer.homepage',stuid = stuid))

    return render_template('report.html', title='Sample Login', header='Sample Case', stuid=stuid,
                               stuname=name,reminder = reminder)

@uicerBP.route('/home', methods=['GET', 'POST'])
def homepage():
    stuid = request.args.get('stuid')

    result = UICer.query.filter(UICer.stuID == stuid).first()
    info = {
        'Search admission requirements': 'uicer.search_admission',
        'View knowledge point': 'alumni.view_knowledge',
        'Provide offer information': 'uicer.provide_offer',
        'View yearly report': 'uicer.report',
        'View offer time': 'offer.view_time',

    }

    if result.state:
        info.update({"Provide knowledge point": "alumni.get_knowledge"})
    print('in login:', result.stuID)
    '''if request.method == 'GET':
        return render_template('homepage.html', title='Sample Login', header='Sample Case')'''
    return render_template('homepage.html', stuid=result.stuID, stuname=result.name, info=info)
