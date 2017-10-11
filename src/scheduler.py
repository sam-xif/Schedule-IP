"""
Scheduler module
The module that does the actual scheduling
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from pymodels import *
import random

class Scheduler:
    """
    Base scheduler interface
    """

    def __init__(self, students, requests, classes):
        # These are data that are already pre-made
        self.students = students
        self.requests = requests
        self.classes = classes
    
    def generateSchedule(self): pass
    def commit(self): pass

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
        random.shuffle(requests)
        for req in requests:
            # Get associated student object
            student = req.student

            schedule.append(self.assign(student, [req.termContained1, req.cont1alt1, req.cont1alt2, req.cont1alt3, req.cont1alt4]))
            schedule.append(self.assign(student, [req.termContained2, req.cont2alt1, req.cont2alt2, req.cont2alt3, req.cont2alt4]))
            schedule.append(self.assign(student, [req.termContained3, req.cont3alt1, req.cont3alt2, req.cont3alt3, req.cont3alt4]))
            schedule.append(self.assign(student, [req.termContained4, req.cont4alt1, req.cont4alt2, req.cont4alt3, req.cont4alt4]))
            schedule.append(self.assign(student, [req.termContained5, req.cont5alt1, req.cont5alt2, req.cont5alt3, req.cont5alt4]))

        self.schedule = schedule
        return schedule

    def assign(self, student, request):
        # returns a (student, section, preference) triple, or None if no class could be assigned

        for alt, course in enumerate(request):
            # Get all sections of a particular course
            courses = [x for x in classes if x.classCode == course]
            random.shuffle(courses)

            for course in courses:
                if course.slotsRemaining > 0:
                    course.slotsRemaining -= 1
                    return (student, course, alt)

        # If this is consistently returned, then there is no space left in any of the alternates
        return None

    def commit(self, connectString):
        # Creates and binds the engine
        engine = create_engine(connectString, module=sqlite)
        Session = sessionmaker(bind=engine)
        session1 = Session()

        # For each row, generates the database entry
        for row in schedule:
            scheduleEntry = Schedule(None, row[0].ID, row[0], row[1].ID, row[1])
            session1.add(scheduleEntry.__export__())

        # Commits the transaction
        session1.commit()