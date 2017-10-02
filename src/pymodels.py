import models

class PyModelBase:
    """ PyModelBase interface"""
    
    @staticmethod
    def __import__(data):
        """ Imports data from an ORM model into a standard python class object """
        raise NotImplementedError
        
    def __export__(self):
        """ Exports the data of the class to the corresponding ORM model """
        raise NotImplementedError
    
    """ Methods for comparing equality between two objects"""
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __cmp__(self, other):
        return self.__dict__ == other.__dict__


class Student(PyModelBase):
    """
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    graduatingClass = Column(Integer)
    studentId = Column(String)
    sex = Column(String)
    cluster = Column(String)
    """

    def __init__(self, ID, name, graduatingClass, sex, cluster):
        self.ID = ID
        self.name = name
        self.graduatingClass = graduatingClass
        self.sex = sex
        self.cluster = cluster
    
    @staticmethod
    def __import__(data):
        if type(data) is not models.Student or data is None:
            raise Exception("Invalid argument to __import__")

        return Student(data.ID, data.name, data.graduatingClass, data.sex, data.cluster)

    def __export__(self):
        return models.Student(ID=self.ID, name=self.name, graduatingClass=self.graduatingClass, sex=self.sex, cluster=self.cluster)


class Class(PyModelBase):
    """
    ID = Column(Integer, primary_key=True)
    className = Column(String)
    classCode = Column(String)
    periodCode = Column(Integer)
    section = Column(Integer)
    room = Column(String)
    instructor = Column(String)
    """

    def __init__(self, ID, className, classCode, periodCode, section, room, instructor):
        self.ID = ID
        self.className = className
        self.classCode = classCode
        self.periodCode = periodCode
        self.section = section
        self.room = room
        self.instructor = instructor

    @staticmethod
    def __import__(data):
        if type(data) is not models.Class or data is None:
            raise Exception("Invalid argument to __import__")

        return Class(data.ID, data.className, data.classCode, data.periodCode, data.section, data.room, instructor)

    def __export__(self):
        return models.Class(ID=self.ID, className=self.className, classCode=self.classCode, periodCode=self.periodCode, section=self.section, room=self.room, instructor=self.instructor)

class Schedule(PyModelBase):
    """
    ID = Column(Integer, primary_key=True)
    student = Column(Integer)
    _class = Column(Integer)
    """

    def __init__(self, ID, student, _class):
        self.ID = ID
        self.student = student
        self._class = _class

    @staticmethod
    def __import__(data):
        if type(data) is not models.Schedule or data is None:
            raise Exception("Invalid argument to __import__")

        return Schedule(data.ID, data.student, data._class)

    def __export__(self):
        return models.Schedule(ID=self.ID, student=self.student, _class=self._class)