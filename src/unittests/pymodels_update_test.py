import unittest

from src import models
from src import pymodels

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

CONNECT_STRING='sqlite+pysqlite:///schedule.db'


class Test_pymodels_update_test(unittest.TestCase):
    def test_A(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
