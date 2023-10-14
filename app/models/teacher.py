from sqlalchemy import Column, String, Integer, orm
from app.models.human import Human


class Teacher(Human):
    id = Column(Integer, primary_key=True, autoincrement=True)
    major = Column(String(50), nullable=False)

    def __init__(self, name, age, major, email, password):
        super(Teacher, self).__init__(name, age, email, password)
        self.major = major
