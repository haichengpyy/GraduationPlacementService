from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class KnowledgePoint(Base):
    no = Column(Integer,primary_key=True, unique=True,autoincrement=True, nullable=False)
    id = Column(String(50), nullable=False)
    courseNameList = Column(String(50), nullable=False)
    programName = Column(String(50), nullable=False)
    KnowledgePoint1 = Column(String(1000))


    def __init__(self, id, courseNameList, programName, KnowledgePoint1):
        super(KnowledgePoint, self).__init__()
        self.id = id
        self.courseNameList = courseNameList
        self.programName = programName
        self.KnowledgePoint1 = KnowledgePoint1

