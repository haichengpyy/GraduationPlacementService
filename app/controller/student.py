from flask import Blueprint, render_template, request
from app.models.base import db
from app.models.student import Student
from app.models.offer import Offer


studentBP = Blueprint('student', __name__)


@studentBP.route('', methods=['GET'])
def add_student():
    #with db.auto_commit():
        #student = Student('hejing', 20, 'UIC', 'hejing@mail.uic.edu.hk', '123456')
        # 数据库的insert操作
        #db.session.add(student)
    curuser = db.session.query(Student).filter_by(id=1).one()
    print(curuser.name)
    result = db.session.query(Offer.University_name).join(Offer.student).filter(Student.GPA >= 3.0).distinct().all()
    print(result)
    return 'hello student'
