from flask import Blueprint, render_template, request
from app.models.base import db
from app.models.offer import Offer
from datetime import datetime
from sqlalchemy import or_, and_, all_, any_,func,extract
offerBP = Blueprint('offer', __name__)


@offerBP.route('', methods=['GET'])
def add_offer(date, id, uni, pro, title, type, comp, GPA):
    with db.auto_commit():
        offer = Offer()
        offer.Date = date
        offer.photocopy = 1
        offer.stuID = id
        offer.University_name = uni
        offer.Program_name = pro
        offer.title = title
        offer.CorT = type
        offer.Company_name = comp
        offer.GPA =GPA
        # 数据库的insert操作
        db.session.add(offer)
    return 'hello offer'

@offerBP.route('/view', methods=['GET','POST'])
def view_time():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')


    if request.method == 'GET':
        return render_template('view_offer_time.html', title='Sample Login', header='Sample Case', stuid=stuid,
                               stuname=name)
    university = request.form.get('university')
    program = request.form.get('program')
    year = request.form.get('year')
    print(year)
    print(program=='')
    table_head = []
    table_row=[]
    datetime_object = datetime.strptime(year, '%Y')
    if university == '' or program == '':
        return 'Nothing input!'


    if university and program:
        max = db.session.query(func.max(Offer.Date)).filter(and_(Offer.University_name==university , Offer.Program_name==program , extract('year', Offer.Date) == datetime_object.year)).first()
        min = db.session.query(func.min(Offer.Date)).filter(and_(Offer.University_name==university , Offer.Program_name==program , extract('year', Offer.Date) == datetime_object.year)).first()
        latemonth = ''
        earlymonth = ''
        table_head= ['University Name','Program Name','Earliest offer received(month)','Latest offer received(month)']
        print(max, min)
        if max[0] != None:
            latemonth = max[0].month
        if min[0] != None:
            earlymonth = min[0].month
        if min[0] == None and max[0] == None:
            reminder = 'Sorry, no information in '+year
            return render_template('view_offer_time.html', title='Sample Login', header='Sample Case', stuid=stuid,stuname=name, reminder = reminder, table_row = table_row)
        table_row = [university,program,earlymonth,latemonth]
        reminder = 'Offer time information in '+year
        #print(max, min[0].month)
    #return 'no!'

    return render_template('view_offer_time.html', title='Sample Login', header='Sample Case', stuid=stuid,stuname=name,reminder=reminder, table_head =table_head, table_row = table_row)

'''
  elif university == '':
        pass
    elif program == '':
        max = db.session.query(func.max(Offer.Date)).filter(
            Offer.University_name == university  and extract('year',Offer.Date) == datetime_object.year).group_by(Offer.Program_name)
        min = db.session.query(func.min(Offer.Date)).filter(
            Offer.University_name == university  and extract('year',Offer.Date) == datetime_object.year).group_by(Offer.Program_name)
        table_head = ['University Name', 'Program Name', 'Earliest offer received(month)',
                      'Latest offer received(month)']
        table_row = [university, program, min[0].month, max[0].month]
        print(max, min)
        for i in min:
            print(i)
        return  'nono'
'''


