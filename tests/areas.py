# pylint: disable=missing-docstring

from pathlib import Path

TEST_FOLDER = Path("/tmp/test-backups-rotate")
if not TEST_FOLDER.exists():
    TEST_FOLDER.mkdir()



MYDB_AREA = {
    'name': 'mydb',
    'folder': str(TEST_FOLDER / "mydb"),
    'patterns': [
        'mydb.*.sql',
    ],
    'datetime_format': "%Y-%m-%d-%H-%M-%S",
    'policy': {
        'day': 5,
        'week': 4,
        'month': 'infinite',
    }
}

ANOTHER_AREA = {
    'name': 'another',
    'folder': str(TEST_FOLDER / "mydb"),
    'patterns': [
        'another.*.sql',
    ],
    'policy': {
        'day': 10,
        'month': 'infinite',
    },
    'use_modification_time': True,
}

ALL_FILES = """
another.2024-09-19-03-30-08.sql  another.2024-10-19-03-30-01.sql  mydb.2024-09-19-03-30-08.sql                mydb.2024-10-19-03-30-01.sql
another.2024-09-20-03-30-07.sql  another.2024-10-20-03-30-00.sql  mydb.2024-09-20-03-30-07.sql                mydb.2024-10-20-03-30-00.sql
another.2024-09-21-03-30-01.sql  another.2024-10-21-03-30-09.sql  mydb.2024-09-21-03-30-01.sql                mydb.2024-10-21-03-30-09.sql
another.2024-09-22-03-30-05.sql  another.2024-10-22-03-30-09.sql  mydb.2024-09-22-03-30-05.sql                mydb.2024-10-22-03-30-09.sql
another.2024-09-23-03-30-04.sql  another.2024-10-23-03-30-01.sql  mydb.2024-09-23-03-30-04.sql                mydb.2024-10-23-03-30-01.sql
another.2024-09-24-03-30-05.sql  another.2024-10-24-03-30-07.sql  mydb.2024-09-24-03-30-05.sql                mydb.2024-10-24-03-30-07.sql
another.2024-09-25-03-30-01.sql  another.2024-10-25-03-30-07.sql  mydb.2024-09-25-03-30-01.sql                mydb.2024-10-25-03-30-07.sql
another.2024-09-26-03-30-06.sql  another.2024-10-26-03-30-01.sql  mydb.2024-09-26-03-30-06.sql                mydb.2024-10-26-03-30-01.sql
another.2024-09-27-03-30-00.sql  another.2024-10-27-03-30-05.sql  mydb.2024-09-27-03-30-00.sql                mydb.2024-10-27-03-30-05.sql
another.2024-09-27-10-40-11.sql  another.2024-10-28-03-30-05.sql  mydb.2024-09-27-10-40-11.sql                mydb.2024-10-28-03-30-05.sql
another.2024-09-28-03-30-03.sql  another.2024-10-29-03-30-04.sql  mydb.2024-09-28-03-30-03.sql                mydb.2024-10-29-03-30-04.sql
another.2024-09-29-03-30-03.sql  another.2024-10-30-03-30-03.sql  mydb.2024-09-29-03-30-03.sql                mydb.2024-10-30-03-30-03.sql
another.2024-09-30-03-30-02.sql  another.2024-10-31-03-30-02.sql  mydb.2024-09-30-03-30-02.sql                mydb.2024-10-31-03-30-02.sql
another.2024-10-01-03-30-01.sql  another.2024-11-01-03-30-02.sql  mydb.2024-10-01-03-30-01.sql                mydb.2024-11-01-03-30-02.sql
another.2024-10-02-03-30-01.sql  another.2024-11-02-03-30-02.sql  mydb.2024-10-02-03-30-01.sql                mydb.2024-11-02-03-30-02.sql
another.2024-10-03-03-30-00.sql  another.2024-11-03-03-30-01.sql  mydb.2024-10-03-03-30-00.sql                mydb.2024-11-03-03-30-01.sql
another.2024-10-04-03-30-00.sql  another.2024-11-04-03-30-05.sql  mydb.2024-10-04-03-30-00.sql                mydb.2024-11-04-03-30-05.sql
another.2024-10-05-03-30-00.sql  another.2024-11-05-03-30-04.sql  mydb.2024-10-05-03-30-00.sql                mydb.2024-11-05-03-30-04.sql
another.2024-10-06-03-30-09.sql  another.2024-11-06-03-30-05.sql  mydb.2024-10-06-03-30-09.sql                mydb.2024-11-06-03-30-05.sql
another.2024-10-07-03-30-09.sql  another.2024-11-07-03-30-03.sql  mydb.2024-10-07-03-30-09.sql                mydb.2024-11-07-03-30-03.sql
another.2024-10-08-03-30-08.sql  another.2024-11-08-03-30-03.sql  mydb.2024-10-08-03-30-08.sql                mydb.2024-11-08-03-30-03.sql
another.2024-10-09-03-30-05.sql  another.2024-11-09-03-30-03.sql  mydb.2024-10-09-03-30-05.sql                mydb.2024-11-09-03-30-03.sql
another.2024-10-10-03-30-00.sql  another.2024-11-10-03-30-02.sql  mydb.2024-10-10-03-30-00.sql                mydb.2024-11-10-03-30-02.sql
another.2024-10-11-03-30-06.sql  another.2024-11-11-03-30-02.sql  mydb.2024-10-11-03-30-06.sql                mydb.2024-11-11-03-30-02.sql
another.2024-10-12-03-30-06.sql  another.2024-11-12-03-30-02.sql  mydb.2024-10-12-03-30-06.sql                mydb.2024-11-12-03-30-02.sql
another.2024-10-13-03-30-00.sql  another.2024-11-13-03-30-00.sql  mydb.2024-10-13-03-30-00.sql                mydb.2024-11-13-03-30-00.sql
another.2024-10-14-03-30-05.sql  another.2024-11-14-03-30-01.sql  mydb.2024-10-14-03-30-05.sql                mydb.2024-11-14-03-30-01.sql
another.2024-10-15-03-30-04.sql  another.2024-11-15-03-30-03.sql  mydb.2024-10-15-03-30-04.sql                mydb.2024-11-15-03-30-03.sql
another.2024-10-16-03-30-09.sql  another.2024-11-16-03-30-00.sql  mydb.2024-10-16-03-30-09.sql                mydb.2024-11-16-03-30-00.sql
another.2024-10-17-03-30-00.sql  another.2024-11-17-03-30-02.sql  mydb.2024-10-17-03-30-00.sql                mydb.2024-11-17-03-30-02.sql
another.2024-10-18-03-30-01.sql  another.2024-11-18-03-30-01.sql  mydb.2024-10-18-03-30-01.sql                mydb.2024-11-18-03-30-01.sql
""".split()

BROKEN_AREAS = [
    {
        # missing a lot of stuff
    },
    {
        'name': 'broken0',
        'folder': '/var/lib/pgsql/backups',
        # should be patterns
        'files': ['foo*.sql'],
        'policy': {'year': 'infinite'},
    },
    {
        'name': 'broken1',
        'folder': '/var/lib/pgsql/backups',
        # should be a list
        'patterns': 'foo*.sql',
    },
    {
        'name': 'broken2',
        'folder': '/var/lib/pgsql/backups',
        'patterns': ['foo*.sql'],
        # cannot have it both ways
        'datetime_format': "%Y-%m-%d-%H-%M-%S",
        'use_modification_time': True,
    },
    # a broken policy
    {
        'name': 'broken3',
        'folder': '/var/lib/pgsql/backups',
        'patterns': ['foo*.sql'],
        'policy': {'year': 'infinite', 'quarter': 5, 'unknown': 3},
    },
]
