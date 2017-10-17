"""
models.py

This file should contain a reflection of the database schema.
The classes are linked to tables in the database with the sqlalchemy Declarative API.

If a change to this schema is made, it is important to follow these steps to perform a migration of the database:
1. Run the command, replacing <name> with a short description of the upgrade: python make_migration.py "<name>"
2. Run the command: python manage.py upgrade

Note:
Only use single line comments in this file for generate_pymodels.py to work correctly
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
Base = declarative_base()


# Classes
class Class(Base):
    __tablename__= 'classes'

    ID = Column(Integer, primary_key=True)
    className = Column(String) # The name of the class, such as 'AP BC Calculus'
    classCode = Column(String) # Class code is the internal name of the class, such as 'MTH-590'
    period = Column(String)
    days = Column(String) 
    section = Column(Integer)
    room = Column(String)
    instructor = Column(String)
    slotsRemaining = Column(Integer)
    targetCapacity = Column(Integer)
    maxCapacity = Column(Integer)

class Student(Base):
    __tablename__ = 'students'

    ID = Column(Integer, primary_key=True)
    name = Column(String)
    graduatingClass = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    cluster = Column(String)
    priority = Column(String)

class Schedule(Base):
    __tablename__ = 'schedules'

    ID = Column(Integer, primary_key=True)
    
    student_id = Column(Integer, ForeignKey("students.ID"))
    student = relationship(Student, primaryjoin=student_id == Student.ID)
    
    _class_id = Column(Integer, ForeignKey("classes.ID"))
    _class = relationship(Class, primaryjoin=_class_id == Class.ID)

class SimpleRequest(Base):
    # A simpler requests class added for convenience

    __tablename__ = "simplereqs"

    ID = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.ID"))
    student = relationship(Student, primaryjoin=student_id == Student.ID)

    courseload = Column(Integer)

    # Courses are integers because they are represented as IDs from the classes table
    course1 = Column(Integer, ForeignKey("classes.ID"))
    c1alt1 = Column(Integer, ForeignKey("classes.ID"))
    c1alt2 = Column(Integer, ForeignKey("classes.ID"))
    c1alt3 = Column(Integer, ForeignKey("classes.ID"))

    course2 = Column(Integer, ForeignKey("classes.ID"))
    c2alt1 = Column(Integer, ForeignKey("classes.ID"))
    c2alt2 = Column(Integer, ForeignKey("classes.ID"))
    c2alt3 = Column(Integer, ForeignKey("classes.ID"))

    course3 = Column(Integer, ForeignKey("classes.ID"))
    c3alt1 = Column(Integer, ForeignKey("classes.ID"))
    c3alt2 = Column(Integer, ForeignKey("classes.ID"))
    c3alt3 = Column(Integer, ForeignKey("classes.ID"))

    course4 = Column(Integer, ForeignKey("classes.ID"))
    c4alt1 = Column(Integer, ForeignKey("classes.ID"))
    c4alt2 = Column(Integer, ForeignKey("classes.ID"))
    c4alt3 = Column(Integer, ForeignKey("classes.ID"))

    course5 = Column(Integer, ForeignKey("classes.ID"))
    c5alt1 = Column(Integer, ForeignKey("classes.ID"))
    c5alt2 = Column(Integer, ForeignKey("classes.ID"))
    c5alt3 = Column(Integer, ForeignKey("classes.ID"))

    course6 = Column(Integer, ForeignKey("classes.ID"))
    c6alt1 = Column(Integer, ForeignKey("classes.ID"))
    c6alt2 = Column(Integer, ForeignKey("classes.ID"))
    c6alt3 = Column(Integer, ForeignKey("classes.ID"))

class Request(Base):
    __tablename__ = "requests"
    
    ID = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.ID"))
    student = relationship(Student, primaryjoin=student_id == Student.ID)
    
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
