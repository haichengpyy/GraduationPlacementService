from sqlalchemy import Column, String, Integer, orm, Float
from app.models.base import Base

# 定义ORM模型,新建一个PROGRAM数据库表
class Program(Base):  # 继承db对象
    #__tablename__ = 'Program'  # 表名
    University_name = Column(String(100), primary_key=True)  # 主键
    Program_name = Column(String(200), nullable=False, )  # nulltable=Flase表示不能为空
    GPA_LOW = Column(Float, nullable=False)  # GPA LOWEST
    GPA_UPPER = Column(Float, nullable=False)  # GPA HIGHEST