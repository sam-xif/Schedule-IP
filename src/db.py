import sys
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
from random import randint

from models import *

DEBUG=True

engine = create_engine('sqlite+pysqlite:///schedule.db', module=sqlite, echo=DEBUG)
print(engine)

allStudents = []

allRequests = []

if __name__=="__main__":

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

    courses = open('src/F17 Master Schedule Sept27_CS.csv', "rt")
    readCourses = csv.reader(courses)
    session2 = Session()
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
    languages.extend(arabic, chinese, classics, french, german, japanese, latin, russian, spanish)

    sciences = []
    sciences.extend(biology, chemistry, physics, science)

    sixth = []
    sixth.extend(art, music, theater, phd, empathy)

    others = []
    others.extend(history, relphil)

    for row in readCourses:
        if (first):
            first = False
        else:
            course = str(row).split(',')[0][:3]
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
            else:
                print("The course code: " + course + " could not be evaluated")

    for r in allStudents: #THIS CREATES A RANDOM SET OF CLASSES
        classReq = [] # array of courses to be allocated to a student
        # rquirements vary depending on class of student
        # 30% chance that they take 6 classes and 70 that they take 5

        # For some reason, half of the courses in the course list got cut out of the csv

        six = (randint(1,10) > 7)
        print("Do they take 6 classes? " + six)
        class1 = math[randint(1,len(math))].split(',')[0] #this is their math class
        classReq.append(class1)

        language = randint(1,len(languages))
        class2 = languages[language][randint(1,len(languages[language]))].split(',')[0] #This is their language class
        classReq.append(class2)

        class3 = english[randint(1,len(english))].split(',')[0] #this is their english class
        classReq.append(class3)

        sciClass = randint(1,len(sciences))
        class4 = sciences[sciClass][randint(1,len(sciences[sciClass]))].split(',')[0] #this is their science class
        classReq.append(class4)

        otherClass = randint(1,len(others))
        class5 = others[otherClass][randint(1,len(others[otherClass]))].split(',')[0] #other class (history or relphil)
        classReq.append(class5)

        if (six):
            sixthClass = randint(1,len(sixth))
            class6 = sixth[sixthClass][randint(1,len(sixth[sixthClass]))].split(',')[0] #assuming 6th class is a theater/art
            classReq.append(class6)
