"""
Scheduler module
The module that does the actual scheduling
"""


import sys
import os
if __name__=='__main__':
    sys.path.append(os.path.realpath('../')) # Assuming the script is run from within the src directory


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from src import pymodels
from src import models

from src.integrity_test import generateStudentObject

import random

CONNECT_STRING='sqlite+pysqlite:///../schedule.db'
DEBUG=True

class Scheduler:
    """
    Base scheduler interface
    """

    def __init__(self, students, requests, classes, session):
        # These are data that are already pre-made
        # All of these are assumed to be from the pymodels types with initialized primary keys, except requests
        # Session is the database session that these objects are bound to
        self.students = students
        self.requests = requests
        self.classes = classes
        self.session = session
    
    def generateSchedule(self): 
        """
        Generates the schedule using some algorithm to be defined in the subclasses of Scheduler
        """
        pass
    
    def commit(self, sessionMaker):
        if not self.schedule:
            raise AttributeError('Run generateSchedule() to generate the schedule before committing')

        # Creates and binds the engine
        session1 = sessionMaker()

        # For each row, generates the database entry
        for row in self.schedule:
            scheduleEntry = pymodels.Schedule(None, row[0].ID, row[0], row[1].ID, row[1])
            session1.add(scheduleEntry.__export_new__())

        # Commits the transaction
        session1.commit()


    # cost function that evalutes performance of the algorithm
    def cost(self):
        # Hyperparameters
        alpha = 1
        beta = 1
        gamma = 1
        delta = 1

        genderCost = 0
        prefCost = 0
        loadBalanceCost = 0
        gradReqCost = 0

        # the input is the ratio of one gender (i.e. boys) to the total number of students
        genderCostFunc = lambda x : 1 + 4(x**2 - x)

        for student, course, pref in self.schedule:
            prefCost += pref**2
            # ...

        return alpha * genderCost + beta * loadBalanceCost + gamma * prefCost + delta * gradReqCost


class BasicScheduler(Scheduler):
    def generateSchedule(self):
        schedule = []

        # Shuffle the order of request objects, and process them sequentially
        random.shuffle(self.requests)
        for req in self.requests:
            # Get associated student object
            student = req.student

            schedule.append(self.assign(student, [req.course1, req.c1alt1, req.c1alt2, req.c1alt3]))
            schedule.append(self.assign(student, [req.course2, req.c2alt1, req.c2alt2, req.c2alt3]))
            schedule.append(self.assign(student, [req.course3, req.c3alt1, req.c3alt2, req.c3alt3]))
            schedule.append(self.assign(student, [req.course4, req.c4alt1, req.c4alt2, req.c4alt3]))
            schedule.append(self.assign(student, [req.course5, req.c5alt1, req.c5alt2, req.c5alt3]))

        self.schedule = schedule
        return schedule

    def assign(self, student, request):
        # returns a (student, section, preference) triple, or None if no class could be assigned

        for alt, course in enumerate(request):
            # Get all sections of a particular course
            courses = [x for x in self.classes if x.classCode == course]
            random.shuffle(courses)

            for course in courses:
                if course.slotsRemaining > 0:
                    course.slotsRemaining -= 1
                    return (student, course, alt)

        # If this is consistently returned, then there is no space left in any of the alternates
        return None


def generateSchedule():
    """Main procedure for generating schedules"""
    # Add students

    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    students = session1.query(models.Student).all()

    # Load class, student, and request data from database
    students = [pymodels.Student.__import__(x) for x in session1.query(models.Student).all()]
    requests = [pymodels.SimpleRequest.__import__(x) for x in session1.query(models.SimpleRequest).all()]
    classes = [pymodels.Class.__import__(x) for x in session1.query(models.Class).all()]

    scheduler = BasicScheduler(students, requests, classes, session1)

    # Perform scheduling
    scheduler.generateSchedule()

    # TODO: Update objects modified in generateSchedule(), then commit

    # Commit
    session1.commit()
    session1.close()

    scheduler.commit(Session)


if __name__=="__main__":
    generateSchedule()