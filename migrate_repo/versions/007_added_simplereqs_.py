from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
simplereqs = Table('simplereqs', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student_id', Integer),
    Column('courseload', Integer),
    Column('course1', Integer),
    Column('c1alt1', Integer),
    Column('c1alt2', Integer),
    Column('c1alt3', Integer),
    Column('course2', Integer),
    Column('c2alt1', Integer),
    Column('c2alt2', Integer),
    Column('c2alt3', Integer),
    Column('course3', Integer),
    Column('c3alt1', Integer),
    Column('c3alt2', Integer),
    Column('c3alt3', Integer),
    Column('course4', Integer),
    Column('c4alt1', Integer),
    Column('c4alt2', Integer),
    Column('c4alt3', Integer),
    Column('course5', Integer),
    Column('c5alt1', Integer),
    Column('c5alt2', Integer),
    Column('c5alt3', Integer),
    Column('course6', Integer),
    Column('c6alt1', Integer),
    Column('c6alt2', Integer),
    Column('c6alt3', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['simplereqs'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['simplereqs'].drop()

