from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class Human(Base):
    __abstract__ = True  # 抽象类 不会生成表
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    email = Column(String(50), unique=True, nullable=True)
    _password = Column('password', String(100))


