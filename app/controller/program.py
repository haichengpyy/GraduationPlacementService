from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.program import Program

programBP = Blueprint('program',__name__)

@programBP.route('', methods=['GET'])
def add_program():
    with db.auto_commit():
        program = Program()
        program.University_name = 'CMU'
        program.Program_name = 'CS'
        program.GPA_LOW = 3.79
        program.GPA_UPPER = 3.98
        # 数据库的insert操作
        db.session.add(program)
    return 'hello program'