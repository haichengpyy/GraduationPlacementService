from sqlalchemy import Column, String, Integer, orm, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Offer(Base):  # 继承db对象
    NO = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    Date = Column(Date, nullable=False, )  # nulltable=Flase表示不能为空
    photocopy = Column(Integer, nullable=False)  #
    stuID = Column(String(30), ForeignKey('uicer.stuID'), nullable=False)  #
    University_name = Column(Text(1000), nullable=False)
    Program_name = Column(Text(1000), nullable=False)
    title = Column(Text(1000), nullable=False)
    CorT = Column(Text(1000), nullable=False)
    Company_name = Column(Text(1000), nullable=True)
    GPA = Column(String(30),nullable=False)
    #uicer = relationship('UICer', back_populates='offers')
