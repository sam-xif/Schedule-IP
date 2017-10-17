import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
import random

import pymodels

# Import random student generator from the integrity test module
from integrity_test import generateStudentObject

DEBUG=True

engine = create_engine('sqlite+pysqlite:///schedule.db', module=sqlite, echo=DEBUG)

MASTER_SCHED = 'src/F17-Master-Schedule-Sept27_CS.csv'

allStudents = []

allRequests = []

def parseStudentInfo():
    """
    NOTE: This code currently does not work
    The course requests should not be stored in the Student object, but the data from the csv should instead be used to map Request objects to Students that already exist in the students table

    For this test, students should be added from the csv first, then Request objects should be created, then the two should be linked to each other.
    """

    ifile  = open('src/Contact Information.csv', "rt")
    read = csv.reader(ifile)
    Session = sessionmaker(bind=engine)
    session1 = Session()
    first = True
    for row in read:
        if (first):
            first = False
        else:
            stu = Student(name=row[2], graduatingClass=row[3], studentId=row[4], sex=row[5],
                cluster=row[6])
            requests = Request(yearlong1=row[7], yearlong2=row[8], yearlong3=row[9], yearlong4=row[10],
                engElectiveTop=row[11], engElective1=row[12], engElective2=row[13], engElective3=row[14],
                engElective4=row[15], engElective5=row[16], termContained1=row[17], cont1alt1=row[18],
                cont1alt2=row[19], cont1alt3=row[20], cont1alt4=row[21], termContained2=row[22],
                cont2alt1=row[23], cont2alt2=row[24], cont2alt3=row[25], cont2alt4=row[26], termContained3=row[27],
                cont3alt1=row[28], cont3alt2=row[29], cont3alt3=row[30], cont3alt4=row[31], termContained4=row[32],
                cont4alt1=row[33], cont4alt2=row[34], cont4alt3=row[35], cont4alt4=row[36], termContained5=row[37],
                cont5alt1=row[38], cont5alt2=row[39], cont5alt3=row[40], cont5alt4=row[41], courseLoad=row[42],
                course6=row[43], topPriority=row[44])
            allStudents.append(stu)
            allRequests.append(requests)

    for x in range(len(allStudents)):
        session1.add(allStudents[x])
        session1.add(allRequests[x])
    
    session1.commit()

def addClassesToDB():
    """Add classes from master schedule csv to database"""
    print("Opening master schedule file...")
    courses = open(MASTER_SCHED, "rt")
    
    print("Preparing to add courses...")
    readCourses = csv.reader(courses)
    Session = sessionmaker(bind=engine)
    session1 = Session()

    # Format Course,Period,Teacher,Section,Room,Days

    classObjects = []
    first = True
    for row in readCourses:
        if first: 
            first = False
            continue

        if row[0] == '': continue

        cap = 16

        courseCode = row[0].split(':')[0].strip()
        courseName = row[0].split(':')[1].strip()
        period = row[1].strip()
        teacher = row[2].strip()
        section = int(row[3].strip())
        room = row[4].strip()
        days = row[5].strip()

        print("Add course", courseCode)
        
        classObjects.append(pymodels.Class(None, courseName, courseCode, period, days, section, room, teacher, cap, cap, cap))

    for c in classObjects:
        session1.add(c.__export_new__())

    print("Committing...")
    session1.commit()
    session1.close()
    courses.close()

def prret(obj, formatStr, *args):
    """
    Utility printing function.

    TODO: Remove this once no longer needed
    """
    print(formatStr.format(obj, *args))
    return obj

def generateClassSet(classes, numAlternates):
    """Helper function for generateData"""
    return [prret(classes[x], 'cl: {}')[0] for x in random.sample(range(0, len(classes)), numAlternates if numAlternates <= len(classes) else len(classes))]

def generateRequests(allStudents):
    courses = open(MASTER_SCHED, "rt")
    readCourses = csv.reader(courses)
    Session = sessionmaker(bind=engine)
    session1 = Session()
    first = True



    arabic = [] #ARA
    art = [] #ART
    biology = [] #BIO
    chinese = [] #CHI
    chemistry = [] #CHM
    classics = [] #CLA
    empathy = [] #EBI
    english = [] #ENG
    french = [] #FRE
    german = [] #GER
    history = [] #HSS
    japanese = [] #JPN
    latin = [] #LTN
    math = [] #MTH
    music = [] #MUS
    phd = [] #PHD
    relphil = [] #PHR
    physics = [] #PHY
    russian = [] #RUS
    science = [] #SCI
    spanish = [] #SPA
    theater = [] #THD

    languages = []
    languages.extend([arabic, chinese, classics, french, german, japanese, latin, russian, spanish])

    sciences = []
    sciences.extend([biology, chemistry, physics, science])

    sixth = []
    sixth.extend([art, music, theater, phd, empathy])

    others = []
    others.extend([history, relphil])

    for row in readCourses:
        if (first):
            first = False
        else:
            course = row[0].split(',')[0][:3]
            if (course == "ARA"):
                arabic.append(row)
            elif (course == "ART"):
                art.append(row)
            elif (course == "BIO"):
                biology.append(row)
            elif (course == "CHI"):
                chinese.append(row)
            elif (course == "CHM"):
                chemistry.append(row)
            elif (course == "CLA"):
                classics.append(row)
            elif (course == "EBI"):
                empathy.append(row)
            elif (course == "ENG"):
                english.append(row)
            elif (course == "FRE"):
                french.append(row)
            elif (course == "GER"):
                german.append(row)
            elif (course == "HSS"):
                history.append(row)
            elif (course == "JPN"):
                japanese.append(row)
            elif (course == "LTN"):
                latin.append(row)
            elif (course == "MTH"):
                math.append(row)
            elif (course == "MUS"):
                music.append(row)
            elif (course == "PHD"):
                phd.append(row)
            elif (course == "PHR"):
                relphil.append(row)
            elif (course == "PHY"):
                physics.append(row)
            elif (course == "RUS"):
                russian.append(row)
            elif (course == "SCI"):
                science.append(row)
            elif (course == "SPA"):
                spanish.append(row)
            elif (course == "THD"):
                theater.append(row)
            # CSC is not included 
            else:
                print("The course code: " + course + " could not be evaluated")

    requestsObjects = []
    for r in allStudents: #THIS CREATES A RANDOM SET OF CLASSES


        classReq = [] # array of courses to be allocated to a student
        # rquirements vary depending on class of student
        # 30% chance that they take 6 classes and 70 that they take 5

        # For some reason, half of the courses in the course list got cut out of the csv

        six = (random.randint(0,10) > 7)
        # print("Do they take 6 classes? ", six)

        # math
        classReq.append(generateClassSet(math, 4))

        # language
        language = random.randint(0, len(languages) - 1)
        classReq.append(generateClassSet(languages[language], 4))

        #english
        classReq.append(generateClassSet(english, 4))
        
        # science
        sciClass = random.randint(0, len(sciences) - 1)
        classReq.append(generateClassSet(sciences[sciClass], 4))

        # other
        otherClass = random.randint(0, len(others) - 1)
        classReq.append(generateClassSet(others[otherClass], 4))

        if (six):
            sixthClass = random.randint(0, len(sixth) - 1)
            classReq.append(generateClassSet(sixth[sixthClass], 4))
        else:
            classReq.append(['','','',''])


        requestsObjects.append(pymodels.SimpleRequest(None, r.ID, r, 6 if six else 5, *classReq))

        print(classReq)

    session1.commit()
    courses.close()

if __name__=="__main__":

    if sys.argv[1] == '--add-courses':
        addClassesToDB()
    else:
        generateRequests([1])