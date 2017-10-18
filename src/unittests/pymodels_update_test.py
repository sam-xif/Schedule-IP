import unittest
import sys
import os

if __name__=="__main__":
    sys.path.append(os.path.realpath('../'))

from src import models
from src import pymodels

from src.integrity_test import randomString

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

CONNECT_STRING='sqlite+pysqlite:///../schedule.db'


class Test_pymodels_update_test(unittest.TestCase):
    def test_A(self):

        name = randomString(10)

        engine = create_engine(CONNECT_STRING, module=sqlite)
        Session = sessionmaker(bind=engine)
        session1 = Session()

        stu = models.Student(name=name, graduatingClass=2018, studentId='101010', sex='male', cluster='wqn', priority='10')
        session1.add(stu)
        session1.commit()
        session1.close()

        session2 = Session()
        stu = pymodels.Student.__import__(session2.query(models.Student).filter_by(name=name).first())
        stu.graduatingClass = stu.graduatingClass - 1 # 2018 - 1 = 2017

        stu.__export__() # Write the changes to the object

        session2.commit()
        session2.close()

        session3 = Session()
        stu = session3.query(models.Student).filter_by(name=name).first()
        self.assertTrue(stu.graduatingClass == 2017)

        session3.delete(stu)

        session3.commit()
        session3.close()


if __name__ == '__main__':
    unittest.main()
