# Schedule-IP

### Notes and Instructions
* To perform an integrity check on the database, navigate to the directory of the database, and run the `integrity_test.py` script from that directory.
* To build a fresh copy of the database with the most recent schema, run `rebuild_db.bat`. This will create a new database file (by default it is called `schedule.db` but that can be changed by passing an argument to the script with the desired name)
  As of right now, `rebuild_db` requires the `sed` command, a unix utility.