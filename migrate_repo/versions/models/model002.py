"""
models.py

This file should contain a reflection of the database schema.
The classes are linked to tables in the database with the sqlalchemy Declarative API.

If a change to this schema is made, it is important to follow these steps to perform a migration of the database:
1. Run the command, replacing <name> with a short description of the upgrade: python make_migration.py "<name>"
2. Run the command: python manage.py upgrade
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
Base = declarative_base()


# Classes
class Class(Base):
    __tablename__= 'class_'
    
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
    graduatingClass = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    cluster = Column(String)
    
    def __repr__(self):
        return "Student<name={0}, _class={1}, studentId={2}, sex={3}>".format(self.name, self._class, self.studentId, self.sex);

    
class Schedule(Base):
    __tablename__ = 'schedule'
    
    ID = Column(Integer, primary_key=True)
    student = Column(Integer)
    _class = Column(Integer)
    
    
"""
DO NOT REMOVE THIS LINE
KEEP IT AT THE BOTTOM OF THE FILE
"""
metadata = Base.metadata