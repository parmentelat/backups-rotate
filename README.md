# backups-rotate

You run a website with a database, and you want to backup your database every day, and keep the last 7 days of backups. This script will do that for you.

## WORK IN PROGRESS

***not yet published on pypi***

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

You define your policy in a YAML file, like e.g (for the policy described above):

```yaml
---
# this defines the area named "database" that can be used
# on the command line to specify the area to be inspected / cleaned up

- name: database
  folder: /usr/lib/backups
  patterns:
    - "*.sql"
    - "*.tar.gz"
  policy:
    year: infinite
    quarter: 3
    month: 2
    week: 4
    day: 5
    hour: 6
```

## Usage

Here are a few ways to run the tool

```bash
# run on all areas
backups-rotate

# on a specific area
backups-rotate database

# not doing anything, just showing what would be done
backups-rotate database --dry-run

# using a config file (default is /etc/backups-logrotate.yaml)
backups-rotate --config my_policy.yaml database
```

which will remove, from the specified folder, all backups that are older than the policy you defined.

## Actual behaviour

When run on a specific area, the tool will:

- gather all matching files in the specified folder
- then for each frequency present in the policy, starting with the shortest one:
  - split time into bins of that frequency, starting from now and going backwards
  - attach every file to corresponding bin
  - then for the number attached to that frequency (can be infinite), and starting from the most recent bin:
    - take the most recent file and mark it as kept
  - then list (if dry-run) or remove (if not dry-run) all files that are not marked as kept

## Example

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

## Timestamps

By default, time is taken from the file's creation time. If you want to use the
file's modification time instead, you can use the `--use-modification-time`
option.

Also if your files are named with a timestamp, you can use the
`--datetime-format` option to specify the format of the timestamp in the file
name (using Python's `datetime` format); files that do not match the format will
be ignored - and thus preserved.

## Tests

```bash
pip install pytest
pytest
```
