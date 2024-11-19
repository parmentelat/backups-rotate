# pylint: disable=missing-docstring

PLANETLAB_AREA = {
    'name': 'planetlab',
    # overwritten by the test code
    'folder': '/var/lib/pgsql/backups',
    'patterns': [
        'planetlab5.*.sql',
    ],
    'datetime_format': "%Y-%m-%d-%H-%M-%S",
}

DRUPAL_AREA = {
    'name': 'drupal',
    # overwritten by the test code
    'folder': '/var/lib/pgsql/backups',
    'patterns': [
        'drupal.*.sql',
    ],
    'use_modification_time': True,
}

ALL_FILES = """
drupal.2024-09-19-03-30-08.sql  drupal.2024-10-19-03-30-01.sql  planetlab5.2024-09-19-03-30-08.sql                planetlab5.2024-10-19-03-30-01.sql
drupal.2024-09-20-03-30-07.sql  drupal.2024-10-20-03-30-00.sql  planetlab5.2024-09-20-03-30-07.sql                planetlab5.2024-10-20-03-30-00.sql
drupal.2024-09-21-03-30-01.sql  drupal.2024-10-21-03-30-09.sql  planetlab5.2024-09-21-03-30-01.sql                planetlab5.2024-10-21-03-30-09.sql
drupal.2024-09-22-03-30-05.sql  drupal.2024-10-22-03-30-09.sql  planetlab5.2024-09-22-03-30-05.sql                planetlab5.2024-10-22-03-30-09.sql
drupal.2024-09-23-03-30-04.sql  drupal.2024-10-23-03-30-01.sql  planetlab5.2024-09-23-03-30-04.sql                planetlab5.2024-10-23-03-30-01.sql
drupal.2024-09-24-03-30-05.sql  drupal.2024-10-24-03-30-07.sql  planetlab5.2024-09-24-03-30-05.sql                planetlab5.2024-10-24-03-30-07.sql
drupal.2024-09-25-03-30-01.sql  drupal.2024-10-25-03-30-07.sql  planetlab5.2024-09-25-03-30-01.sql                planetlab5.2024-10-25-03-30-07.sql
drupal.2024-09-26-03-30-06.sql  drupal.2024-10-26-03-30-01.sql  planetlab5.2024-09-26-03-30-06.sql                planetlab5.2024-10-26-03-30-01.sql
drupal.2024-09-27-03-30-00.sql  drupal.2024-10-27-03-30-05.sql  planetlab5.2024-09-27-03-30-00.sql                planetlab5.2024-10-27-03-30-05.sql
drupal.2024-09-27-10-40-11.sql  drupal.2024-10-28-03-30-05.sql  planetlab5.2024-09-27-10-40-11-before-family.sql  planetlab5.2024-10-28-03-30-05.sql
drupal.2024-09-28-03-30-03.sql  drupal.2024-10-29-03-30-04.sql  planetlab5.2024-09-28-03-30-03.sql                planetlab5.2024-10-29-03-30-04.sql
drupal.2024-09-29-03-30-03.sql  drupal.2024-10-30-03-30-03.sql  planetlab5.2024-09-29-03-30-03.sql                planetlab5.2024-10-30-03-30-03.sql
drupal.2024-09-30-03-30-02.sql  drupal.2024-10-31-03-30-02.sql  planetlab5.2024-09-30-03-30-02.sql                planetlab5.2024-10-31-03-30-02.sql
drupal.2024-10-01-03-30-01.sql  drupal.2024-11-01-03-30-02.sql  planetlab5.2024-10-01-03-30-01.sql                planetlab5.2024-11-01-03-30-02.sql
drupal.2024-10-02-03-30-01.sql  drupal.2024-11-02-03-30-02.sql  planetlab5.2024-10-02-03-30-01.sql                planetlab5.2024-11-02-03-30-02.sql
drupal.2024-10-03-03-30-00.sql  drupal.2024-11-03-03-30-01.sql  planetlab5.2024-10-03-03-30-00.sql                planetlab5.2024-11-03-03-30-01.sql
drupal.2024-10-04-03-30-00.sql  drupal.2024-11-04-03-30-05.sql  planetlab5.2024-10-04-03-30-00.sql                planetlab5.2024-11-04-03-30-05.sql
drupal.2024-10-05-03-30-00.sql  drupal.2024-11-05-03-30-04.sql  planetlab5.2024-10-05-03-30-00.sql                planetlab5.2024-11-05-03-30-04.sql
drupal.2024-10-06-03-30-09.sql  drupal.2024-11-06-03-30-05.sql  planetlab5.2024-10-06-03-30-09.sql                planetlab5.2024-11-06-03-30-05.sql
drupal.2024-10-07-03-30-09.sql  drupal.2024-11-07-03-30-03.sql  planetlab5.2024-10-07-03-30-09.sql                planetlab5.2024-11-07-03-30-03.sql
drupal.2024-10-08-03-30-08.sql  drupal.2024-11-08-03-30-03.sql  planetlab5.2024-10-08-03-30-08.sql                planetlab5.2024-11-08-03-30-03.sql
drupal.2024-10-09-03-30-05.sql  drupal.2024-11-09-03-30-03.sql  planetlab5.2024-10-09-03-30-05.sql                planetlab5.2024-11-09-03-30-03.sql
drupal.2024-10-10-03-30-00.sql  drupal.2024-11-10-03-30-02.sql  planetlab5.2024-10-10-03-30-00.sql                planetlab5.2024-11-10-03-30-02.sql
drupal.2024-10-11-03-30-06.sql  drupal.2024-11-11-03-30-02.sql  planetlab5.2024-10-11-03-30-06.sql                planetlab5.2024-11-11-03-30-02.sql
drupal.2024-10-12-03-30-06.sql  drupal.2024-11-12-03-30-02.sql  planetlab5.2024-10-12-03-30-06.sql                planetlab5.2024-11-12-03-30-02.sql
drupal.2024-10-13-03-30-00.sql  drupal.2024-11-13-03-30-00.sql  planetlab5.2024-10-13-03-30-00.sql                planetlab5.2024-11-13-03-30-00.sql
drupal.2024-10-14-03-30-05.sql  drupal.2024-11-14-03-30-01.sql  planetlab5.2024-10-14-03-30-05.sql                planetlab5.2024-11-14-03-30-01.sql
drupal.2024-10-15-03-30-04.sql  drupal.2024-11-15-03-30-03.sql  planetlab5.2024-10-15-03-30-04.sql                planetlab5.2024-11-15-03-30-03.sql
drupal.2024-10-16-03-30-09.sql  drupal.2024-11-16-03-30-00.sql  planetlab5.2024-10-16-03-30-09.sql                planetlab5.2024-11-16-03-30-00.sql
drupal.2024-10-17-03-30-00.sql  drupal.2024-11-17-03-30-02.sql  planetlab5.2024-10-17-03-30-00.sql                planetlab5.2024-11-17-03-30-02.sql
drupal.2024-10-18-03-30-01.sql  drupal.2024-11-18-03-30-01.sql  planetlab5.2024-10-18-03-30-01.sql                planetlab5.2024-11-18-03-30-01.sql
""".split()

BROKEN_AREAS = [
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
]
