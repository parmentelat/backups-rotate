# pylint: disable=missing-docstring, wildcard-import

# from unittest import TestCase
from pathlib import Path

import pandas as pd
import pytest

from backups_rotate.area import extract_date_from_filename, TimedPath, Area

from tests.areas import *
from tests.policies import *


def test_broken_areas():
    for area_dict in BROKEN_AREAS:
        with pytest.raises(ValueError):
            Area(area_dict)


def test_datetime_format():
    path = Path("database-2024-01-01-something.sql")
    datetime_format = "%Y-%m-%d"
    ts = extract_date_from_filename(path, datetime_format)
    assert ts == pd.Timestamp("2024-01-01")


def test_attach_timestamp_by_format():
    path = Path("database-2024-01-01-something.sql")
    tp = TimedPath(path)
    tp.attach_timestamp(datetime_format="%Y-%m-%d")
    assert tp.timestamp == pd.Timestamp("2024-01-01")


def test_attach_timestamp_by_ctime():
    path = TEST_FOLDER / "--some-test-file--"
    if path.exists():
        path.unlink()
    now = pd.Timestamp.now()
    path.touch()
    tp = TimedPath(path)
    tp.attach_timestamp()
    assert (tp.timestamp - now) < pd.Timedelta(milliseconds=50)


def test_attach_timestamp_mydb_area():
    files = ALL_FILES
    area_dict = MYDB_AREA
    folder = Path(area_dict['folder'])
    if not folder.exists():
        folder.mkdir()
    for file in folder.glob("*"):
        file.unlink()
    for file in files:
        path = folder / file
        path.touch()

    area = Area(area_dict)
    area.read()
    assert area.deleted == 53


def test_attach_timestamp_another_area():
    files = ALL_FILES
    area_dict = ANOTHER_AREA
    folder = Path(area_dict['folder'])
    if not folder.exists():
        folder.mkdir()
    for file in folder.glob("*"):
        file.unlink()
    for file in files:
        path = folder / file
        path.touch()

    area = Area(area_dict)
    area.read()
    # because this area uses modification time, only one file
    # survives in this test
    assert area.deleted == 61
