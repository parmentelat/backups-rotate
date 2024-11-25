# backups-rotate

You run a website with a database, and you want to backup your database every day, and keep the last 7 days of backups. This script will do that for you.

Contrary to logrotate, where contents is aassumed to be **appended** to files, here we assume all the files are **full backups**; and that each backup is independant from the others. So the job is not to rename files, but to remove the old ones.

## What it does

You can define a policy on several frequency levels, e.g.

- one per year - no matter how far back in time
- and/or, keep one backup for each of the last 3 quarters
- and/or, the last 2 months
- and/or, the last 4 weeks
- and/or, the last 5 days
- and/or, the last 6 hours

## Installation

```bash
pip install backups-rotate
```

## Configuration

The tool comes with 6 predefined "periods": `year`, `quarter`, `month`, `week`, `day`, `hour`.

You define your folder and policy in a YAML file, like e.g (for the policy described above):

```yaml
---
# this defines the area named "database" that can be used
# on the command line to specify what needs to be cleaned up

- name: database
  folder: /usr/lib/backups
  patterns:
    - "mydb*.sql"
    - "mydb*.sql.gz"
  policy:
    year: infinite
    quarter: 3
    month: 2
    week: 4
    day: 5
    hour: 6

# by default the time attaached to each file is its creation time
# optionally, you can specify the format of the timestamp 
# in the file name, like so:
    # datetime_format: "%Y-%m-%d_%H-%M-%S"
# in that case, files that do not match the format will be ignored

# OR, still optionally, you can specify to use the modification time
# instead of the creation time
    # use_modification_time: true

# you define as many areas as you want
- name: builds
  folder: /usr/lib/builds
  patterns:
    - "myapp*"
  # type can be either folder, file or symlink
  # by default all files are considered
  type: folder
  policy:
    month: 4
    week: 3
    day: 4
```

## Usage

Here are a few ways to run the tool

```bash
# run on all areas
backups-rotate

# using a config file (default is /etc/backups-rotate.yaml, and ./backups-rotate.yaml)
backups-rotate --config my_policy.yaml database

# on a specific area
backups-rotate database

# on a specific area; list the files considered
# you can use -l instead of --list
backups-rotate database --list

# same in verbose mode
# you can use -v instead of --verbose
backups-rotate database --list --verbose

# same but only shows what would be deleted
# you can use -d instead of --deleted
backups-rotate database --list --deleted

# not doing anything, just showing what would be done
# you can use -n instead of --dry-run
backups-rotate database --dry-run

# do it (i.e. remove the selected files), and be verbose about it
backups-rotate database --verbose
```

## How policies are implemented

When run on a specific area, the tool will:

- gather all matching files in the specified folder
- then for each frequency present in the policy, starting with the shortest one:
  - split time into bins of that frequency, starting from now and going backwards
  - attach every file to corresponding bin
  - then for the number attached to that frequency (can be infinite), and starting from the most recent bin:
    - take the most recent file and mark it as kept
  - then list (if dry-run) or remove (if not dry-run) all files that are not marked as kept

### Example

Based on `sample2()` in `tests/samples.py`, assume you have one file per hour between
`2024-01-01 00:00` and `2024-11-15 23:00`, then applying the policy above would keep:

```text
2024-06-30 23:00    # for quarter
2024-09-30 23:00    # for quarter
2024-10-27 23:00    # for week
2024-10-31 23:00    # for month
2024-11-03 23:00    # for week
2024-11-10 23:00    # for week
2024-11-11 23:00    # for day
2024-11-12 23:00    # for day
2024-11-13 23:00    # for day
2024-11-14 23:00    # for day
2024-11-15 18:00    # for hour
2024-11-15 19:00    # for hour
2024-11-15 20:00    # for hour
2024-11-15 21:00    # for hour
2024-11-15 22:00    # for hour
2024-11-15 23:00    # for hour day week month quarter year
```

if instead the policy was defined with `month: infinite`, then the policy would also retain

```text
2024-01-31 23:00
2024-02-29 23:00
2024-03-31 23:00
2024-04-30 23:00
2024-05-31 23:00
2024-07-31 23:00
2024-08-31 23:00
```

noting that the following 2 were already kept for quarter:

```text
2024-06-30 23:00
2024-09-30 23:00
```

### Timestamps

By default, time is taken from the file's creation time. If you want to use the
file's modification time instead, you can use the `use-modification-time`
flag in your yaml config.

Also if your files are named with a timestamp, you can use the `datetime-format`
option to specify the format of the timestamp in the file name (using Python's
`datetime` format).

## Tests

```bash
pip install pytest
pytest
```
