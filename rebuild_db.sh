# Draft of BASH version of rebuild_db.bat

DBNAME=schedule.db
MANAGE_SCRIPT=manage.py
EXT=db

rm $DBNAME
touch $DBNAME

python $MANAGE_SCRIPT version_control --url=sqlite:///$DBNAME

sed -i "s;sqlite:///.*\.${EXT};sqlite:///${DBNAME};g" $MANAGE_SCRIPT

python $MANAGE_SCRIPT upgrade

