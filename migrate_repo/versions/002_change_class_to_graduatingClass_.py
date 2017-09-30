from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
student = Table('student', pre_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('_class', Integer),
    Column('studentId', String),
    Column('sex', String),
)

student = Table('student', post_meta,
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
    pre_meta.tables['student'].columns['_class'].drop()
    post_meta.tables['student'].columns['cluster'].create()
    post_meta.tables['student'].columns['graduatingClass'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['student'].columns['_class'].create()
    post_meta.tables['student'].columns['cluster'].drop()
    post_meta.tables['student'].columns['graduatingClass'].drop()

