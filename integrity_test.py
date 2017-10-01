import src.models
import src.pymodels

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from random import *

DEBUG=False
CONNECT_STRING='sqlite:///schedule.db'


def randomString(length): 
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join([alphabet[randrange(len(alphabet))] for x in range(length)])

def integrity_test():
    print("Beginning integrity test...")
    
    # Part 1: Generate objects and write them to the database
    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()
    
    # Generate 1000 objects
    students = []
    for i in range(1000):
        students.append(src.models.Student(name=randomString(20), graduatingClass=randint(2015, 2020), studentId=randomString(7), sex=randomString(5), cluster=randomString(10)))
       
    # Add student objects to database
    for student in students:
        session1.add(student)
    
    session1.commit()

    studentObjects = [src.pymodels.Student.__import__(x) for x in students] 

    session1.close()
    
    print("Wrote 1000 student objects to the database")
    print("Opening new session...")
    session2 = Session()
    print("Querying database...")
    student_query = [src.pymodels.Student.__import__(x) for x in session2.query(src.models.Student).all()]
    
    success = True
    for i in range(1000):
        if studentObjects[i] != student_query[i]:
            print("Integrity check failed at", i)
            success = False
            break

    if success:
        print("Test passed")
    
    print("Done")
    
    
if __name__ == "__main__":
    integrity_test()