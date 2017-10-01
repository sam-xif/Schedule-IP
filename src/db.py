import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from models import *

DEBUG=True

engine = create_engine('sqlite+pysqlite:///schedule.db', module=sqlite, echo=DEBUG)

allStudents = []

if __name__=="__main__":

    ifile  = open('Contact Information.csv', "rt")
    read = csv.reader(ifile)
    i = 0
    Session = sessionmaker(bind=engine)
    session1 = Session()
    for row in read :
        allStudents[i] = Student(name=row[2], graduatingClass=row[3], studentId=row[4], sex=row[5], cluster=row[6])
        i+=1

    x = 1
    for x in len(allStudents):
        session1.add(allStudents[x])
        stu_query = session1.query(Student).filter_by(studentId="000001").first()
        session1.commit()




    # # A simple database test
    # Session = sessionmaker(bind=engine)
    # session1 = Session()
    # stu = Student(name="Samm Xifaras", _class=2017, studentId="101010", sex="male", cluster="WQN")
    #
	# # This addition is considered 'pending.' It's changes will not be reflected in the database until a query is executed, which will first flush all pending changes.
    # session1.add(stu)
    #
    # # Execute query to flush
    # stu_query = session1.query(Student).filter_by(studentId=000001).first()
    #
    # # Commit changes to database
    # session1.commit()


    # print(repr(stu_query))
