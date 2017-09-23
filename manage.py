#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='migrate-repo', debug='False', url='sqlite:///schedule.db')
