
from migrate import *


"""
models.py

This file should contain a reflection of the database schema.
The classes are linked to tables in the database with the sqlalchemy Declarative API.

If a change to this schema is made, it is important to follow these steps to update the database file:
* open a command prompt and navigate to this directory
* type without quotes (replace script name with a description of the changes you made): python manage.py script "<script name>"
* navigate to migrate-repo/versions and find the script with the name you just gave it.
* open this script
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
    _class = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    #cluster = Column(String)
    #date_of_birth = Column(String)
    
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

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    Base.metadata.bind = migrate_engine
    Base.metadata.create_all(migrate_engine)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    Base.metadata.bind = migrate_engine
    Base.metadata.drop_all(migrate_engine)
