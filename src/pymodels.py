# This file was auto-generated by generate_pymodels.py

from src import models

class PyModelBase:
    @staticmethod
    def __import__(data):
        raise NotImplementedError
        
    def __export_new__(self):
        raise NotImplementedError

    def __export__(self):
        raise NotImplementedError
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        # Standard hash function
        hashes = [self.__dict__[x].__hash__() for x in self.__dict__ if x is not None]
        hashSum = 0
        for hash in hashes:
            hashSum = 31 * hashSum + hash
        return hashSum
    


class Class(PyModelBase):
    def __init__(self, ID, className, classCode, period, days, section, room, instructor, slotsRemaining, targetCapacity, maxCapacity, wrapped_object=None):
        self.ID=ID
        self.className=className
        self.classCode=classCode
        self.period=period
        self.days=days
        self.section=section
        self.room=room
        self.instructor=instructor
        self.slotsRemaining=slotsRemaining
        self.targetCapacity=targetCapacity
        self.maxCapacity=maxCapacity
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.Class or data is None:
            raise Exception("Invalid argument to __import__")

        return Class(data.ID, data.className, data.classCode, data.period, data.days, data.section, data.room, data.instructor, data.slotsRemaining, data.targetCapacity, data.maxCapacity, wrapped_object=data)
        
    def __export_new__(self):
        return models.Class(ID=self.ID, className=self.className, classCode=self.classCode, period=self.period, days=self.days, section=self.section, room=self.room, instructor=self.instructor, slotsRemaining=self.slotsRemaining, targetCapacity=self.targetCapacity, maxCapacity=self.maxCapacity)

    def __export__(self):
        self.wrapped_object.ID=self.ID
        self.wrapped_object.className=self.className
        self.wrapped_object.classCode=self.classCode
        self.wrapped_object.period=self.period
        self.wrapped_object.days=self.days
        self.wrapped_object.section=self.section
        self.wrapped_object.room=self.room
        self.wrapped_object.instructor=self.instructor
        self.wrapped_object.slotsRemaining=self.slotsRemaining
        self.wrapped_object.targetCapacity=self.targetCapacity
        self.wrapped_object.maxCapacity=self.maxCapacity
        return self.wrapped_object
        
    def __repr__(self):
        return "Class<ID={}, className={}, classCode={}, period={}, days={}, section={}, room={}, instructor={}, slotsRemaining={}, targetCapacity={}, maxCapacity={}".format(self.ID, self.className, self.classCode, self.period, self.days, self.section, self.room, self.instructor, self.slotsRemaining, self.targetCapacity, self.maxCapacity)


class Student(PyModelBase):
    def __init__(self, ID, name, graduatingClass, studentId, sex, cluster, priority, wrapped_object=None):
        self.ID=ID
        self.name=name
        self.graduatingClass=graduatingClass
        self.studentId=studentId
        self.sex=sex
        self.cluster=cluster
        self.priority=priority
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.Student or data is None:
            raise Exception("Invalid argument to __import__")

        return Student(data.ID, data.name, data.graduatingClass, data.studentId, data.sex, data.cluster, data.priority, wrapped_object=data)
        
    def __export_new__(self):
        return models.Student(ID=self.ID, name=self.name, graduatingClass=self.graduatingClass, studentId=self.studentId, sex=self.sex, cluster=self.cluster, priority=self.priority)

    def __export__(self):
        self.wrapped_object.ID=self.ID
        self.wrapped_object.name=self.name
        self.wrapped_object.graduatingClass=self.graduatingClass
        self.wrapped_object.studentId=self.studentId
        self.wrapped_object.sex=self.sex
        self.wrapped_object.cluster=self.cluster
        self.wrapped_object.priority=self.priority
        return self.wrapped_object
        
    def __repr__(self):
        return "Student<ID={}, name={}, graduatingClass={}, studentId={}, sex={}, cluster={}, priority={}".format(self.ID, self.name, self.graduatingClass, self.studentId, self.sex, self.cluster, self.priority)


class Schedule(PyModelBase):
    def __init__(self, ID, student_id, student, _class_id, _class, wrapped_object=None):
        self.ID=ID
        self.student_id=student_id
        self.student=student
        self._class_id=_class_id
        self._class=_class
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.Schedule or data is None:
            raise Exception("Invalid argument to __import__")

        return Schedule(data.ID, data.student_id, data.student, data._class_id, data._class, wrapped_object=data)
        
    def __export_new__(self):
        return models.Schedule(ID=self.ID, student_id=self.student_id, student=self.student, _class_id=self._class_id, _class=self._class)

    def __export__(self):
        self.wrapped_object.ID=self.ID
        self.wrapped_object.student_id=self.student_id
        self.wrapped_object.student=self.student
        self.wrapped_object._class_id=self._class_id
        self.wrapped_object._class=self._class
        return self.wrapped_object
        
    def __repr__(self):
        return "Schedule<ID={}, student_id={}, student={}, _class_id={}, _class={}".format(self.ID, self.student_id, self.student, self._class_id, self._class)


class SimpleRequest(PyModelBase):
    def __init__(self, ID, student_id, student, courseload, course1, c1alt1, c1alt2, c1alt3, course2, c2alt1, c2alt2, c2alt3, course3, c3alt1, c3alt2, c3alt3, course4, c4alt1, c4alt2, c4alt3, course5, c5alt1, c5alt2, c5alt3, course6, c6alt1, c6alt2, c6alt3, wrapped_object=None):
        self.ID=ID
        self.student_id=student_id
        self.student=student
        self.courseload=courseload
        self.course1=course1
        self.c1alt1=c1alt1
        self.c1alt2=c1alt2
        self.c1alt3=c1alt3
        self.course2=course2
        self.c2alt1=c2alt1
        self.c2alt2=c2alt2
        self.c2alt3=c2alt3
        self.course3=course3
        self.c3alt1=c3alt1
        self.c3alt2=c3alt2
        self.c3alt3=c3alt3
        self.course4=course4
        self.c4alt1=c4alt1
        self.c4alt2=c4alt2
        self.c4alt3=c4alt3
        self.course5=course5
        self.c5alt1=c5alt1
        self.c5alt2=c5alt2
        self.c5alt3=c5alt3
        self.course6=course6
        self.c6alt1=c6alt1
        self.c6alt2=c6alt2
        self.c6alt3=c6alt3
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.SimpleRequest or data is None:
            raise Exception("Invalid argument to __import__")

        return SimpleRequest(data.ID, data.student_id, data.student, data.courseload, data.course1, data.c1alt1, data.c1alt2, data.c1alt3, data.course2, data.c2alt1, data.c2alt2, data.c2alt3, data.course3, data.c3alt1, data.c3alt2, data.c3alt3, data.course4, data.c4alt1, data.c4alt2, data.c4alt3, data.course5, data.c5alt1, data.c5alt2, data.c5alt3, data.course6, data.c6alt1, data.c6alt2, data.c6alt3, wrapped_object=data)
        
    def __export_new__(self):
        return models.SimpleRequest(ID=self.ID, student_id=self.student_id, student=self.student, courseload=self.courseload, course1=self.course1, c1alt1=self.c1alt1, c1alt2=self.c1alt2, c1alt3=self.c1alt3, course2=self.course2, c2alt1=self.c2alt1, c2alt2=self.c2alt2, c2alt3=self.c2alt3, course3=self.course3, c3alt1=self.c3alt1, c3alt2=self.c3alt2, c3alt3=self.c3alt3, course4=self.course4, c4alt1=self.c4alt1, c4alt2=self.c4alt2, c4alt3=self.c4alt3, course5=self.course5, c5alt1=self.c5alt1, c5alt2=self.c5alt2, c5alt3=self.c5alt3, course6=self.course6, c6alt1=self.c6alt1, c6alt2=self.c6alt2, c6alt3=self.c6alt3)

    def __export__(self):
        self.wrapped_object.ID=self.ID
        self.wrapped_object.student_id=self.student_id
        self.wrapped_object.student=self.student
        self.wrapped_object.courseload=self.courseload
        self.wrapped_object.course1=self.course1
        self.wrapped_object.c1alt1=self.c1alt1
        self.wrapped_object.c1alt2=self.c1alt2
        self.wrapped_object.c1alt3=self.c1alt3
        self.wrapped_object.course2=self.course2
        self.wrapped_object.c2alt1=self.c2alt1
        self.wrapped_object.c2alt2=self.c2alt2
        self.wrapped_object.c2alt3=self.c2alt3
        self.wrapped_object.course3=self.course3
        self.wrapped_object.c3alt1=self.c3alt1
        self.wrapped_object.c3alt2=self.c3alt2
        self.wrapped_object.c3alt3=self.c3alt3
        self.wrapped_object.course4=self.course4
        self.wrapped_object.c4alt1=self.c4alt1
        self.wrapped_object.c4alt2=self.c4alt2
        self.wrapped_object.c4alt3=self.c4alt3
        self.wrapped_object.course5=self.course5
        self.wrapped_object.c5alt1=self.c5alt1
        self.wrapped_object.c5alt2=self.c5alt2
        self.wrapped_object.c5alt3=self.c5alt3
        self.wrapped_object.course6=self.course6
        self.wrapped_object.c6alt1=self.c6alt1
        self.wrapped_object.c6alt2=self.c6alt2
        self.wrapped_object.c6alt3=self.c6alt3
        return self.wrapped_object
        
    def __repr__(self):
        return "SimpleRequest<ID={}, student_id={}, student={}, courseload={}, course1={}, c1alt1={}, c1alt2={}, c1alt3={}, course2={}, c2alt1={}, c2alt2={}, c2alt3={}, course3={}, c3alt1={}, c3alt2={}, c3alt3={}, course4={}, c4alt1={}, c4alt2={}, c4alt3={}, course5={}, c5alt1={}, c5alt2={}, c5alt3={}, course6={}, c6alt1={}, c6alt2={}, c6alt3={}".format(self.ID, self.student_id, self.student, self.courseload, self.course1, self.c1alt1, self.c1alt2, self.c1alt3, self.course2, self.c2alt1, self.c2alt2, self.c2alt3, self.course3, self.c3alt1, self.c3alt2, self.c3alt3, self.course4, self.c4alt1, self.c4alt2, self.c4alt3, self.course5, self.c5alt1, self.c5alt2, self.c5alt3, self.course6, self.c6alt1, self.c6alt2, self.c6alt3)


class Request(PyModelBase):
    def __init__(self, ID, student_id, student, yearlong1, yearlong2, yearlong3, yearlong4, engElectiveTop, engElective1, engElective2, engElective3, engElective4, engElective5, termContained1, cont1alt1, cont1alt2, cont1alt3, cont1alt4, termContained2, cont2alt1, cont2alt2, cont2alt3, cont2alt4, termContained3, cont3alt1, cont3alt2, cont3alt3, cont3alt4, termContained4, cont4alt1, cont4alt2, cont4alt3, cont4alt4, termContained5, cont5alt1, cont5alt2, cont5alt3, cont5alt4, courseLoad, course6, topPriority, wrapped_object=None):
        self.ID=ID
        self.student_id=student_id
        self.student=student
        self.yearlong1=yearlong1
        self.yearlong2=yearlong2
        self.yearlong3=yearlong3
        self.yearlong4=yearlong4
        self.engElectiveTop=engElectiveTop
        self.engElective1=engElective1
        self.engElective2=engElective2
        self.engElective3=engElective3
        self.engElective4=engElective4
        self.engElective5=engElective5
        self.termContained1=termContained1
        self.cont1alt1=cont1alt1
        self.cont1alt2=cont1alt2
        self.cont1alt3=cont1alt3
        self.cont1alt4=cont1alt4
        self.termContained2=termContained2
        self.cont2alt1=cont2alt1
        self.cont2alt2=cont2alt2
        self.cont2alt3=cont2alt3
        self.cont2alt4=cont2alt4
        self.termContained3=termContained3
        self.cont3alt1=cont3alt1
        self.cont3alt2=cont3alt2
        self.cont3alt3=cont3alt3
        self.cont3alt4=cont3alt4
        self.termContained4=termContained4
        self.cont4alt1=cont4alt1
        self.cont4alt2=cont4alt2
        self.cont4alt3=cont4alt3
        self.cont4alt4=cont4alt4
        self.termContained5=termContained5
        self.cont5alt1=cont5alt1
        self.cont5alt2=cont5alt2
        self.cont5alt3=cont5alt3
        self.cont5alt4=cont5alt4
        self.courseLoad=courseLoad
        self.course6=course6
        self.topPriority=topPriority
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.Request or data is None:
            raise Exception("Invalid argument to __import__")

        return Request(data.ID, data.student_id, data.student, data.yearlong1, data.yearlong2, data.yearlong3, data.yearlong4, data.engElectiveTop, data.engElective1, data.engElective2, data.engElective3, data.engElective4, data.engElective5, data.termContained1, data.cont1alt1, data.cont1alt2, data.cont1alt3, data.cont1alt4, data.termContained2, data.cont2alt1, data.cont2alt2, data.cont2alt3, data.cont2alt4, data.termContained3, data.cont3alt1, data.cont3alt2, data.cont3alt3, data.cont3alt4, data.termContained4, data.cont4alt1, data.cont4alt2, data.cont4alt3, data.cont4alt4, data.termContained5, data.cont5alt1, data.cont5alt2, data.cont5alt3, data.cont5alt4, data.courseLoad, data.course6, data.topPriority, wrapped_object=data)
        
    def __export_new__(self):
        return models.Request(ID=self.ID, student_id=self.student_id, student=self.student, yearlong1=self.yearlong1, yearlong2=self.yearlong2, yearlong3=self.yearlong3, yearlong4=self.yearlong4, engElectiveTop=self.engElectiveTop, engElective1=self.engElective1, engElective2=self.engElective2, engElective3=self.engElective3, engElective4=self.engElective4, engElective5=self.engElective5, termContained1=self.termContained1, cont1alt1=self.cont1alt1, cont1alt2=self.cont1alt2, cont1alt3=self.cont1alt3, cont1alt4=self.cont1alt4, termContained2=self.termContained2, cont2alt1=self.cont2alt1, cont2alt2=self.cont2alt2, cont2alt3=self.cont2alt3, cont2alt4=self.cont2alt4, termContained3=self.termContained3, cont3alt1=self.cont3alt1, cont3alt2=self.cont3alt2, cont3alt3=self.cont3alt3, cont3alt4=self.cont3alt4, termContained4=self.termContained4, cont4alt1=self.cont4alt1, cont4alt2=self.cont4alt2, cont4alt3=self.cont4alt3, cont4alt4=self.cont4alt4, termContained5=self.termContained5, cont5alt1=self.cont5alt1, cont5alt2=self.cont5alt2, cont5alt3=self.cont5alt3, cont5alt4=self.cont5alt4, courseLoad=self.courseLoad, course6=self.course6, topPriority=self.topPriority)

    def __export__(self):
        self.wrapped_object.ID=self.ID
        self.wrapped_object.student_id=self.student_id
        self.wrapped_object.student=self.student
        self.wrapped_object.yearlong1=self.yearlong1
        self.wrapped_object.yearlong2=self.yearlong2
        self.wrapped_object.yearlong3=self.yearlong3
        self.wrapped_object.yearlong4=self.yearlong4
        self.wrapped_object.engElectiveTop=self.engElectiveTop
        self.wrapped_object.engElective1=self.engElective1
        self.wrapped_object.engElective2=self.engElective2
        self.wrapped_object.engElective3=self.engElective3
        self.wrapped_object.engElective4=self.engElective4
        self.wrapped_object.engElective5=self.engElective5
        self.wrapped_object.termContained1=self.termContained1
        self.wrapped_object.cont1alt1=self.cont1alt1
        self.wrapped_object.cont1alt2=self.cont1alt2
        self.wrapped_object.cont1alt3=self.cont1alt3
        self.wrapped_object.cont1alt4=self.cont1alt4
        self.wrapped_object.termContained2=self.termContained2
        self.wrapped_object.cont2alt1=self.cont2alt1
        self.wrapped_object.cont2alt2=self.cont2alt2
        self.wrapped_object.cont2alt3=self.cont2alt3
        self.wrapped_object.cont2alt4=self.cont2alt4
        self.wrapped_object.termContained3=self.termContained3
        self.wrapped_object.cont3alt1=self.cont3alt1
        self.wrapped_object.cont3alt2=self.cont3alt2
        self.wrapped_object.cont3alt3=self.cont3alt3
        self.wrapped_object.cont3alt4=self.cont3alt4
        self.wrapped_object.termContained4=self.termContained4
        self.wrapped_object.cont4alt1=self.cont4alt1
        self.wrapped_object.cont4alt2=self.cont4alt2
        self.wrapped_object.cont4alt3=self.cont4alt3
        self.wrapped_object.cont4alt4=self.cont4alt4
        self.wrapped_object.termContained5=self.termContained5
        self.wrapped_object.cont5alt1=self.cont5alt1
        self.wrapped_object.cont5alt2=self.cont5alt2
        self.wrapped_object.cont5alt3=self.cont5alt3
        self.wrapped_object.cont5alt4=self.cont5alt4
        self.wrapped_object.courseLoad=self.courseLoad
        self.wrapped_object.course6=self.course6
        self.wrapped_object.topPriority=self.topPriority
        return self.wrapped_object
        
    def __repr__(self):
        return "Request<ID={}, student_id={}, student={}, yearlong1={}, yearlong2={}, yearlong3={}, yearlong4={}, engElectiveTop={}, engElective1={}, engElective2={}, engElective3={}, engElective4={}, engElective5={}, termContained1={}, cont1alt1={}, cont1alt2={}, cont1alt3={}, cont1alt4={}, termContained2={}, cont2alt1={}, cont2alt2={}, cont2alt3={}, cont2alt4={}, termContained3={}, cont3alt1={}, cont3alt2={}, cont3alt3={}, cont3alt4={}, termContained4={}, cont4alt1={}, cont4alt2={}, cont4alt3={}, cont4alt4={}, termContained5={}, cont5alt1={}, cont5alt2={}, cont5alt3={}, cont5alt4={}, courseLoad={}, course6={}, topPriority={}".format(self.ID, self.student_id, self.student, self.yearlong1, self.yearlong2, self.yearlong3, self.yearlong4, self.engElectiveTop, self.engElective1, self.engElective2, self.engElective3, self.engElective4, self.engElective5, self.termContained1, self.cont1alt1, self.cont1alt2, self.cont1alt3, self.cont1alt4, self.termContained2, self.cont2alt1, self.cont2alt2, self.cont2alt3, self.cont2alt4, self.termContained3, self.cont3alt1, self.cont3alt2, self.cont3alt3, self.cont3alt4, self.termContained4, self.cont4alt1, self.cont4alt2, self.cont4alt3, self.cont4alt4, self.termContained5, self.cont5alt1, self.cont5alt2, self.cont5alt3, self.cont5alt4, self.courseLoad, self.course6, self.topPriority)

