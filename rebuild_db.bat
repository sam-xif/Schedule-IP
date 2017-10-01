@echo off
rem Batch script to automatically create and migrate a new database from the current migrate_repo repository
rem Notes: Assumes that manage.py already exists in the current directory
rem        Assumes database files have .db extension
rem Requires sed
rem TODO: Remove requirement for sed by using the migrate command to generate a new management script

rem Change any of these variables to reflect your environment
set REPO=migrate_repo
set EXT=db
set MANAGE_SCRIPT=manage.py
set DB_NAME=schedule.%EXT%

if not "%1"=="" (
    set DB_NAME=%1
)

rem Create the empty database file
type nul > %DB_NAME%

rem Put the database under version control
python %MANAGE_SCRIPT% version_control --url=sqlite:///%DB_NAME%

rem update the manage.py script to manage the new database
sed -i "s;sqlite:///.*\.%EXT%;sqlite:///%DB_NAME%;g" %MANAGE_SCRIPT%

rem upgrades to the most recent schema
python %MANAGE_SCRIPT% upgrade

