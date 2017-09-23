import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite

from models import *

DEBUG=True

e = create_engine('sqlite+pysqlite:///schedule.db', module=sqlite, echo=DEBUG)

if __name__=="__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'create-tables':
        create_tables(e)
    elif len(sys.argv) > 1 and sys.argv[1] == 'update':
        Teacher.update_table(e)
    else:
        Session = sessionmaker(bind=e)
        session1 = Session()
        stu = Student(name="Samm Xifaras", _class=2017, studentId="101010", sex="male")
		
		# This addition is considered 'pending.' It's changes will not be reflected in the database until a query is executed, which will first flush all pending changes.        
        session1.add(stu) 

        # Execute query to flush
        stu_query = session1.query(Student).filter_by(name="Samm Xifaras").first()

        # Commit changes to database
        session1.commit()
        
        print(repr(stu_query))
		