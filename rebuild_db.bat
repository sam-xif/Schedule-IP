@echo off
rem Batch script to automatically create and migrate a new database from the current migrate_repo repository
rem Notes: Assumes that manage.py already exists in the current directory
rem        Assumes database files have .db extension
rem Requires sed

set REPO=migrate_repo
set EXT=db
set MANAGE_SCRIPT=manage.py

if "%1"=="" (
    echo missing argument: db_name
    goto :EOF
)

rem Create the empty database file
type nul > %1

rem Put the database under version control
python %MANAGE_SCRIPT% version_control --url=sqlite:///%1

rem update the manage.py script to manage the new database
sed -i "s;sqlite:///.*\.%EXT%;sqlite:///%1;g" %MANAGE_SCRIPT%

rem upgrades to the most recent schema
python %MANAGE_SCRIPT% upgrade

