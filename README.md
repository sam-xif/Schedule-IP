# Schedule-IP

### External Dependencies
* `tqdm` (`pip install tqdm`)
* `sqlalchemy` (`pip install sqlalchemy`)
* `sqlalchemy-migrate` (`pip install sqlalchemy-migrate`)
* `sqlite3`

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

### Project Final Report
In this project, our goal was to write a scheduling algorithm capable of assigning students to courses. We began by setting up a database to hold the necessary information, scraped some of PA's master schedule data to use, and began building an algorithm.
We ended up implementing the Hungarian Algorithm as the algorithm of choice, as the scheduling problem could be interpreted nicely as finding the optimal matching of a bipartite graph.
Unfortunately, we did not have enough time to develop this into a full-scale scheduler, but we did get it working with simple scheduling scenarios.

To run a simple scenario, use the command `python simplescenario.py`. This will run a scheduling scenario with 10 students and 5 spots in each section. The output at the end will show student names (which are random character strings) mapped to courses.

A big issue we ran into while developing this algorithm was incredibly long runtimes. Those have mostly been eliminated due to various optimizations.
To circumvent this, we made changes to the algorithm in order to improve speed, but it may have introduced unexpected consequences with regards to finding a perfect matching.
In the future, the algorithm could likely be expanded by running a second pass over the output and correcting any errors that the algorithm may have made.