from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
class_ = Table('class_', pre_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('className', String),
    Column('classCode', String),
    Column('periodCode', Integer),
    Column('section', Integer),
    Column('room', String),
    Column('instructor', String),
)

schedule = Table('schedule', pre_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student', Integer),
    Column('_class', Integer),
)

student = Table('student', pre_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('graduatingClass', Integer),
    Column('studentId', String),
    Column('sex', String),
    Column('cluster', String),
)

classes = Table('classes', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('className', String),
    Column('classCode', String),
    Column('periodCode', Integer),
    Column('section', Integer),
    Column('room', String),
    Column('instructor', String),
)

requests = Table('requests', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student', Integer),
    Column('yearlong1', String),
    Column('yearlong2', String),
    Column('yearlong3', String),
    Column('yearlong4', String),
    Column('engElectiveTop', String),
    Column('engElective1', String),
    Column('engElective2', String),
    Column('engElective3', String),
    Column('engElective4', String),
    Column('engElective5', String),
    Column('termContained1', String),
    Column('cont1alt1', String),
    Column('cont1alt2', String),
    Column('cont1alt3', String),
    Column('cont1alt4', String),
    Column('termContained2', String),
    Column('cont2alt1', String),
    Column('cont2alt2', String),
    Column('cont2alt3', String),
    Column('cont2alt4', String),
    Column('termContained3', String),
    Column('cont3alt1', String),
    Column('cont3alt2', String),
    Column('cont3alt3', String),
    Column('cont3alt4', String),
    Column('termContained4', String),
    Column('cont4alt1', String),
    Column('cont4alt2', String),
    Column('cont4alt3', String),
    Column('cont4alt4', String),
    Column('termContained5', String),
    Column('cont5alt1', String),
    Column('cont5alt2', String),
    Column('cont5alt3', String),
    Column('cont5alt4', String),
    Column('courseLoad', String),
    Column('course6', String),
    Column('topPriority', String),
)

schedules = Table('schedules', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student', Integer),
    Column('_class', Integer),
)

students = Table('students', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('graduatingClass', Integer),
    Column('studentId', String),
    Column('sex', String),
    Column('cluster', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['class_'].drop()
    pre_meta.tables['schedule'].drop()
    pre_meta.tables['student'].drop()
    post_meta.tables['classes'].create()
    post_meta.tables['requests'].create()
    post_meta.tables['schedules'].create()
    post_meta.tables['students'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['class_'].create()
    pre_meta.tables['schedule'].create()
    pre_meta.tables['student'].create()
    post_meta.tables['classes'].drop()
    post_meta.tables['requests'].drop()
    post_meta.tables['schedules'].drop()
    post_meta.tables['students'].drop()

