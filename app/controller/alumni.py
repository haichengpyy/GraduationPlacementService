from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.base import db
from app.models.alumni import Alumni
from app.models.uicer import UICer
from app.models.knowledgePoint import KnowledgePoint
from sqlalchemy import or_, and_, all_, any_

alumniBP = Blueprint('alumni', __name__)


@alumniBP.route('', methods=['GET'])
def get_student():
    with db.auto_commit():
        student = Alumni('15030026152', 'hejing', '123456', '3.5', 'hejing@mail.uic.edu.hk', 'MR.HE', 2011, 'Male')
        student.graduete_year(2015)
        # 数据库的insert操作
        db.session.add(student)
    return 'hi alumni'


@alumniBP.route('/write', methods=['GET', 'POST'])
def get_knowledge():
    stuid = request.args.get('stuid')
    stuname = request.args.get('stuname')
    if request.method == 'GET':
        return render_template('writeKnowledgePoint.html',stuid = stuid,stuname = stuname)

    courseNameList = request.form['cname']
    programName = request.form['pname']
    KnowledgePoint1 = request.form['KnowledgePoint1']
    niming = request.form['ano']
    if niming == 'Original Name':
        result = UICer.query.filter(UICer.stuID == stuid).first()
        result.anomous(result.name)
    new = KnowledgePoint(stuid, courseNameList, programName, KnowledgePoint1)
    db.session.add(new)
    db.session.commit()
    return render_template('writeKnowledgePoint.html',stuid = stuid,stuname = stuname,reminder = 'succussfully uploaded!')


@alumniBP.route('/view', methods=['GET', 'POST'])
def view_knowledge():
    stuid = request.args.get('stuid')
    name = request.args.get('stuname')
    if request.method == 'GET':
        return render_template('viewKnowledgePoint.html', title='Sample Login', header='Sample Case', stuid=stuid,
                               stuname=name)
    keywords = request.form.get('keywords')
    results = db.session.query(KnowledgePoint.programName,KnowledgePoint.courseNameList,KnowledgePoint.KnowledgePoint1,KnowledgePoint.create_time).filter(or_(KnowledgePoint.programName.ilike('%{keywords}%'.format(keywords=keywords)),
                                              KnowledgePoint.courseNameList.ilike('%{keywords}%'.format(keywords=keywords)),
                                              KnowledgePoint.KnowledgePoint1.ilike('%{keywords}%'.format(keywords=keywords)))).limit(6)
    print(results.first())
    result3 = db.session.query(KnowledgePoint.programName,KnowledgePoint.courseNameList,KnowledgePoint.KnowledgePoint1,KnowledgePoint.create_time,
                               UICer.AnonymousName).filter(or_(KnowledgePoint.programName.ilike('%{keywords}%'.format(keywords=keywords)),
                          KnowledgePoint.courseNameList.ilike('%{keywords}%'.format(keywords=keywords)),
                        KnowledgePoint.KnowledgePoint1.ilike('%{keywords}%'.format(keywords=keywords)))).filter(
                      KnowledgePoint.id == UICer.stuID).distinct().all()
    print(result3)
    if (not results.first()):
        hint = "No results found."
    else:
        hint = ""
    return render_template('viewKnowledgePoint.html', keyword=keywords, results=result3, hint=hint, stuid=stuid,
                               stuname=name)
