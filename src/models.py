"""
models.py

This file should contain a reflection of the database schema.
The classes are linked to tables in the database with the sqlalchemy Declarative API.

If a change to this schema is made, it is important to follow these steps to perform a migration of the database:
1. Run the command, replacing <name> with a short description of the upgrade: python make_migration.py "<name>"
2. Run the command: python manage.py upgrade
"""
9
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
Base = declarative_base()


# Classes
class Class(Base):
    __tablename__= 'classes'

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
    __tablename__ = 'students'

    ID = Column(Integer, primary_key=True)
    name = Column(String)
    graduatingClass = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    cluster = Column(String)

    def __repr__(self):
        return "Student<name={0}, _class={1}, studentId={2}, sex={3}>".format(self.name, self._class, self.studentId, self.sex)

class Schedule(Base):
    __tablename__ = 'schedules'

    ID = Column(Integer, primary_key=True)
    student = Column(Integer)
    _class = Column(Integer)

class Request(Base):
    """
    Database object that represents a set of course requests.
    There is a one-to-one mapping between Request objects and Student objects
    """
   
    __tablename__ = "requests"
    ID = Column(Integer, primary_key=True)
    student = Column(Integer)

    # Other course request fields
    yearlong1 = Column(String)
    yearlong2 = Column(String)
    yearlong3 = Column(String)
    yearlong4 = Column(String)

    engElectiveTop = Column(String)
    engElective1 = Column(String)
    engElective2 = Column(String)
    engElective3 = Column(String)
    engElective4 = Column(String)
    engElective5 = Column(String)

    termContained1 = Column(String)
    cont1alt1 = Column(String)
    cont1alt2 = Column(String)
    cont1alt3 = Column(String)
    cont1alt4 = Column(String)

    termContained2 = Column(String)
    cont2alt1 = Column(String)
    cont2alt2 = Column(String)
    cont2alt3 = Column(String)
    cont2alt4 = Column(String)

    termContained3 = Column(String)
    cont3alt1 = Column(String)
    cont3alt2 = Column(String)
    cont3alt3 = Column(String)
    cont3alt4 = Column(String)

    termContained4 = Column(String)
    cont4alt1 = Column(String)
    cont4alt2 = Column(String)
    cont4alt3 = Column(String)
    cont4alt4 = Column(String)

    termContained5 = Column(String)
    cont5alt1 = Column(String)
    cont5alt2 = Column(String)
    cont5alt3 = Column(String)
    cont5alt4 = Column(String)

    courseLoad= Column(String)
    course6 = Column(String)
    topPriority = Column(String)

"""
DO NOT REMOVE THIS LINE
KEEP IT AT THE BOTTOM OF THE FILE
"""
metadata = Base.metadata
