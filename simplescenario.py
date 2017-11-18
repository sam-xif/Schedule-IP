"""
Script that runs a simple scheduling scenario
"""

import os
import sys
import subprocess

from src import models
from src import pymodels

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from src.algoscheduler import HungarianScheduler

from src.db import *


if __name__=='__main__':
    sys.path.append(os.path.realpath('./')) # Assuming the script is run from within the src directory

CONNECT_STRING='sqlite:///schedule.db'

if __name__=="__main__":
    # Rebuild the database

    rebuild_db = subprocess.run(['rebuild_db.bat'], stdout=subprocess.PIPE)
    print(rebuild_db.stdout.decode('utf-8'))

    # Add classes to the databse
    addClassesToDB()

    # Add students
    addStudentsToDB(20)

    # Add requests
    addRequestsToDB()

    # Run scheduler

    cap = 18

    engine = create_engine(CONNECT_STRING, module=sqlite)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    students = session1.query(models.Student).all()

    # Load class, student, and request data from database
    students = [pymodels.Student.__import__(x) for x in session1.query(models.Student).all()]
    requests = [pymodels.SimpleRequest.__import__(x) for x in session1.query(models.SimpleRequest).all()]
    classes = [pymodels.Class.__import__(x) for x in session1.query(models.Class).all()]

    for c in classes:
        c.slotsRemaining = cap

    scheduler = HungarianScheduler(students, requests, classes, session1)
    scheduler.generateSchedule()

    print("DONE")