from sqlalchemy import Column, String, Integer, orm, SmallInteger, Float
from sqlalchemy.orm import relationship

from app.models.base import Base


class UICer(Base):
    __tablename__ = 'uicer'
    stuID = Column(String(30), primary_key=True, unique=True, nullable=False)
    GPA = Column(String(30), nullable=True)
    name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=True)
    _password = Column('password', String(100))
    state = Column(SmallInteger, default=0)  # 0 is student, 1 is alumni
    enrollment = Column(Integer)
    gender = Column(String(10), nullable=False)
    graduate = Column(Integer, nullable=True, default=0)
    AnonymousName = Column(String(50), nullable=True, default='Anonymous')

    #offers = relationship('Offer', back_populates='uicer')

    def __init__(self, StuID, Name, Password, GPA, Email, enrollment, gender):
        super(UICer, self).__init__()
        self.enrollment = enrollment
        self.stuID = StuID
        self.name = Name
        self.email = Email
        self._password = Password
        self.GPA = GPA
        self.gender = gender
        if int(enrollment)< 2018:
            self.state = 1

    def verify(self):
        info = {
            'ID': self.stuID,
            'password': self._password,
            'name': self.name,
            'email': self.email,
            'state': self.state
        }
        print(type(info))
        return info

    def change_password(self, password):
        self._password = password
        return

    def view_password(self):
        return self._password

    def graduete_year(self, graduate):
        self.graduate = graduate
        return self.graduate

    def anomous(self, ano):
        self.AnonymousName = ano
        return