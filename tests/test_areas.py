from unittest import TestCase
from pathlib import Path

import pandas as pd

from backups_rotate.area import extract_date_from_filename, TimedPath

def test_file_format():
    path = Path("database-2024-01-01-something.sql")
    format = "%Y-%m-%d"
    ts = extract_date_from_filename(path, format)
    assert ts == pd.Timestamp("2024-01-01")

def test_attach_timestamp1():
    path = Path("database-2024-01-01-something.sql")
    tp = TimedPath(path)
    tp.attach_timestamp(file_format="%Y-%m-%d")
    assert tp.timestamp == pd.Timestamp("2024-01-01")

def test_attach_timestamp2():
    path = Path("/tmp/--some-test-file--")
    if path.exists():
        path.unlink()
    now = pd.Timestamp.now()
    path.touch()
    tp = TimedPath(path)
    tp.attach_timestamp()
    assert (tp.timestamp - now) < pd.Timedelta(milliseconds=50)
