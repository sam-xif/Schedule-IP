from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
schedules = Table('schedules', pre_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student', Integer),
    Column('_class', Integer),
)

schedules = Table('schedules', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student_id', Integer),
    Column('_class_id', Integer),
)

requests = Table('requests', pre_meta,
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

requests = Table('requests', post_meta,
    Column('ID', Integer, primary_key=True, nullable=False),
    Column('student_id', Integer),
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['schedules'].columns['_class'].drop()
    pre_meta.tables['schedules'].columns['student'].drop()
    post_meta.tables['schedules'].columns['_class_id'].create()
    post_meta.tables['schedules'].columns['student_id'].create()
    pre_meta.tables['requests'].columns['student'].drop()
    post_meta.tables['requests'].columns['student_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['schedules'].columns['_class'].create()
    pre_meta.tables['schedules'].columns['student'].create()
    post_meta.tables['schedules'].columns['_class_id'].drop()
    post_meta.tables['schedules'].columns['student_id'].drop()
    pre_meta.tables['requests'].columns['student'].create()
    post_meta.tables['requests'].columns['student_id'].drop()

