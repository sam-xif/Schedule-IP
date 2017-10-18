"""
This command must be run from the directory where the database is, or it won't work.
Alternatively, you can change the path in the CONNECT_STRING variable
"""

import os
import sys
if __name__=='__main__':
    sys.path.append(os.path.realpath('../')) # Assuming the script is run from within the src directory

from src import models
from src import pymodels

import subprocess

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from random import *

DEBUG=False
CONNECT_STRING='sqlite:///schedule.db'


def randomString(length): 
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join([alphabet[randrange(len(alphabet))] for x in range(length)])

def generateStudentObject():
    return models.Student(name=randomString(20), graduatingClass=randint(2015, 2020), studentId=randomString(7), sex=randomString(5), cluster=randomString(10))

def integrity_test():
    print("Beginning integrity test...")

    print("Rebuilding the database...")
    rebuild_db = subprocess.run(['rebuild_db.bat'], stdout=subprocess.PIPE)
    print(rebuild_db.stdout.decode('utf-8'))
    
    print("Connecting to the database...")
    # Part 1: Generate objects and write them to the database
    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()
    
    print("Generating 1000 student objects...")
    # Generate 1000 objects
    students = []
    for i in range(1000):
        students.append(generateStudentObject())
       
    # Add student objects to database
    for student in students:
        session1.add(student)
    
    print("Committing the transaction...")
    session1.commit()

    # studentObjects must be populated after the transaction is committed so that the primary key IDs are assigned
    studentObjects = [pymodels.Student.__import__(x) for x in students] 

    session1.close()
    
    print("Wrote 1000 student objects to the database")
    print("Opening new session...")
    session2 = Session()
    print("Querying database...")
    student_query = [pymodels.Student.__import__(x) for x in session2.query(models.Student).all()]
    
    success = True
    for i in range(1000):
        if studentObjects[i] != student_query[i]:
            print("Integrity check failed at", i)
            success = False
            break

    if success:
        print("Test passed")
    
    print("Done")

def test_hashes():
    # Generate 1000 objects
    students = []
    for i in range(1000):
        students.append(models.Student(name=randomString(20), graduatingClass=randint(2015, 2020), studentId=randomString(7), sex=randomString(5), cluster=randomString(10)))
        print(students[i].__hash__())

    hashes = [x.__hash__() for x in students]
    print("total number of unique hashes:", len(set(hashes)))

    
    
if __name__ == "__main__":
    integrity_test()