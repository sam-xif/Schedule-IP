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
from src.classcode import ClassCode

from src.integrity_test import generateStudentObject

import random

from tqdm import tqdm

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

    def commit(self, close=False):
        if not self.schedule:
            raise AttributeError('Run generateSchedule() to generate the schedule before committing')

        # Creates and binds the engine

        # For each row, generates the database entry
        for course in self.schedule:
            for student in self.schedule[course]:
                courseObj = self.hashDict[course]
                scheduleEntry = pymodels.Schedule(None, student.ID, student, courseObj.ID, courseObj.__export__())
                self.session.add(scheduleEntry.__export_new__())

        if close:
            self.session.commit()
            self.session.close()

    def getCourseHash(self, course):
        """
        Utility function for getting the course object's hash, which excludes mutable fields such as slotsRemaining
        """
        return course.hash(exclude=['slotsRemaining'])


    """
    Cost functions
    """
    def genderCostPerCourse(self, course):
        """
        Calculates the gender cost for each course
        """
        genderCostFunc = lambda x :  1 + (4)*(x**2 - x) #optimized at 1/2 at which point y = 1

        # No need to call getCourseHash on these because the keys of the self.schedule dictionary are already hashes
        genderRatio = sum([int(x.sex) for x in self.schedule[course]]) / len(self.schedule[course])
        genderCost = genderCostFunc(genderRatio)
        
        return genderCost

    # cost function that evalutes performance of the algorithm
    def cost(self):
        # Hyperparameters - not prioritized
        alpha = 1
        beta = 1
        gamma = 1
        delta = 1

        # Cost values
        genderCost = 0
        prefCost = 0
        loadBalanceCost = 0
        gradReqCost = 0

        prefCostFunc = lambda x : (-1/16)*(x**2) + 1

        for course in self.schedule:
            # *** Calculate gender cost ***
            genderCost += self.genderCostPerCourse(course)

            # TODO: Calculate other costs here

        return alpha * genderCost + beta * loadBalanceCost + gamma * prefCost + delta * gradReqCost #want this to be as big as possible


class BasicScheduler(Scheduler):
    def generateSchedule(self):
        self.fails = 0
        self.totalassignments = 0

        self.schedule = {}
        self.hashDict = {}

        # Shuffle the order of request objects, and process them sequentially
        random.shuffle(self.requests)

        # tqdm is experimental here; it is used to show progress of scheduling
        for req in tqdm(self.requests, ascii=True, desc="scheduler progress"):
            # Get associated student object
            
            # req.student is a regular models object !!!
            student = req.student

            self.assign(student, [[req.course1, req.c1alt1, req.c1alt2, req.c1alt3], 
                                  [req.course2, req.c2alt1, req.c2alt2, req.c2alt3], 
                                  [req.course3, req.c3alt1, req.c3alt2, req.c3alt3], 
                                  [req.course4, req.c4alt1, req.c4alt2, req.c4alt3], 
                                  [req.course5, req.c5alt1, req.c5alt2, req.c5alt3]])

        return self.schedule

    def assign(self, student, requests):
        self.totalassignments += 5

        # returns a (student, section, preference) triple, or None if no class could be assigned

        allClasses = []

        for request in requests:
            #print('assigning', student.name, end='')
            for alt, course in enumerate(request):
                if course == '': continue
                assigned = False

                # Get all sections of a particular course
                courses = [x for x in self.classes if
                           ClassCode.getClassCodeFromTitle(x.classCode) ==
                           ClassCode.getClassCodeFromTitle(course)]
                random.shuffle(courses)

                for c in courses:
                    if c.slotsRemaining > 0:
                        c.slotsRemaining -= 1
                        if self.getCourseHash(c) not in self.schedule:
                            self.schedule[self.getCourseHash(c)] = []
                            self.hashDict[self.getCourseHash(c)] = c
                            
                        # Create has of course object, excluding any volatile fields
                        self.schedule[self.getCourseHash(c)].append(student)

                        allClasses.append((c, alt))
                        assigned = True
                        break
                
                if assigned: break

        self.fails += len(requests) - len(allClasses)
        return allClasses


def generateSchedule():
    """Main procedure for generating schedules"""
    # Add students

    cap = 18

    engine = create_engine(CONNECT_STRING, module=sqlite, echo=DEBUG)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    students = session1.query(models.Student).all()

    # Load class, student, and request data from database
    students = [pymodels.Student.__import__(x) for x in session1.query(models.Student).all()]
    requests = [pymodels.SimpleRequest.__import__(x) for x in session1.query(models.SimpleRequest).all()]
    classes = [pymodels.Class.__import__(x) for x in session1.query(models.Class).all()]

    for c in classes:
        c.slotsRemaining = cap


    scheduler = BasicScheduler(students, requests, classes, session1)

    # Perform scheduling
    scheduler.generateSchedule()
    scheduler.commit()
    # TODO: Update objects modified in generateSchedule(), then commit
    # Note: Updates are processed automatically when changes to the pymodels are made

    print('fail_rate:', '{}%'.format((scheduler.fails / scheduler.totalassignments) * 100), '({} / {})'.format(scheduler.fails, scheduler.totalassignments))
    print(len(classes))
    print('total cost: {}; avg across courses: {}'.format(scheduler.cost(), scheduler.cost() / len(scheduler.schedule)))

    
    # Commit
    session1.commit()
    session1.close()


if __name__=="__main__":
    generateSchedule()
