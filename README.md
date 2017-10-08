# Schedule-IP

### Notes and Instructions
##### Testing the database
To perform an integrity check on the database, navigate to the directory of the database, and run the `integrity_test.py` script from that directory.

##### Rebuilding the database
To build a fresh copy of the database with the most recent schema, run `rebuild_db.bat`. This will create a new database file (by default it is called `schedule.db` but that can be changed by passing an argument to the script with the desired name).
As of right now, `rebuild_db` requires the `sed` command, a unix utility.

##### Upgrading the database schema
The database schema is reflected in python in the file `src/models.py`.
If a change to this file is made, the database must be updated to reflect these changes.
Run `python make_upgrade.py "message"`, replacing message with a short description of the changes you made to `models.py`. An upgrade script has now been created in the `migrate_repo/versions` directory.

Now, run `python manage.py upgrade`. This will upgrade the database to the latest version.

##### Upgrading `pymodels.py`
More python-friendly versions of the database models exist in `src/pymodels.py`. These are essentially the same as the `models.py` classes but they allow easy comparison for equality and do not use class attributes.
Instead of inputting the changes from `models.py` by hand, simply run `python generate_pymodels.py`.

