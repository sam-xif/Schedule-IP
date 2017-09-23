from sqlalchemy import *
from migrate import *

# models.py

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# Classes
class Class(Base):
    __tablename__= 'class'
    
    ID = Column(Integer, primary_key=True)
    className = Column(String)
    classCode = Column(String)
    periodCode = Column(Integer)
    section = Column(Integer)
    room = Column(String)
    instructor = Column(String)
    
    def __repr__(self):
        pass
        
class Student(Base):
    __tablename__ = 'student'
    
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    _class = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    
    def __repr__(self):
        return "Student<name={0}, _class={1}, studentId={2}, sex={3}>".format(self.name, self._class, self.studentId, self.sex);

    
class Schedule(Base):
    __tablename__ = 'schedule'
    
    ID = Column(Integer, primary_key=True)
    student = Column(Integer)
    _class = Column(Integer)
    
    
def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Base.metadata.bind = migrate_engine
    Base.metadata.create_all(migrate_engine)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Base.metadata.bind = migrate_engine
    Base.metadata.drop_all(migrate_engine)
