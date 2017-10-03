from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
classes = Table('classes', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('className', String),
    Column('classCode', String),
    Column('periodCode', Integer),
    Column('section', Integer),
    Column('room', String),
    Column('instructor', String),
    Column('slotsRemaining', Integer),
)

students = Table('students', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('graduatingClass', Integer),
    Column('studentId', String),
    Column('sex', String),
    Column('cluster', String),
    Column('priority', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['classes'].columns['slotsRemaining'].create()
    post_meta.tables['students'].columns['priority'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['classes'].columns['slotsRemaining'].drop()
    post_meta.tables['students'].columns['priority'].drop()

