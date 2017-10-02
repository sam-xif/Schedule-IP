import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from models import *

DEBUG=True

engine = create_engine('sqlite+pysqlite:///schedule.db', module=sqlite, echo=DEBUG)
print(engine)
allStudents = []

allStudents = []

if __name__=="__main__":

    ifile  = open('Contact Information.csv', "rt")
    read = csv.reader(ifile)
    i = 0
    Session = sessionmaker(bind=engine)
    session1 = Session()
    for row in read:
        allStudents[i] = Student(name=row[2], graduatingClass=row[3], studentId=row[4], sex=row[5],
            cluster=row[6], yearlong1=row[7], yearlong2=row[8], yearlong3=row[9], yearlong4=row[10],
            engElectiveTop=row[11], engElective1=row[12], engElective2=row[13], engElective3=row[14],
            engElective4=row[15], engElective5=row[16], termContained1=row[17], cont1alt1=row[18],
            cont1alt2=row[19], cont1alt3=row[20], cont1alt4=row[21], termContained2=row[22],
            cont2alt1=row[23], cont2alt2=row[24], cont2alt3=row[25], cont2alt4=row[26], termContained3=row[27],
            cont3alt1=row[28], cont3alt2=row[29], cont3alt3=row[30], cont3alt4=row[31], termContained4=row[32],
            cont4alt1=row[33], cont4alt2=row[34], cont4alt3=row[35], cont4alt4=row[36], termContained5=row[37],
            cont5alt1=row[38], cont5alt2=row[39], cont5alt3=row[40], cont5alt4=row[41], courseLoad=row[42],
            course6=row[43], topPriority=row[44])
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
