# pylint: disable=missing-docstring, wildcard-import

# from unittest import TestCase
from pathlib import Path

import pandas as pd
import pytest

from backups_rotate.area import extract_date_from_filename, TimedPath, Area

from tests.areas import *
from tests.policies import *


TEST_FOLDER = Path("/tmp/test-backups-rotate")
if not TEST_FOLDER.exists():
    TEST_FOLDER.mkdir()


def test_broken_area0():
    with pytest.raises(ValueError):
        Area(BROKEN_AREAS[0])
def test_broken_area1():
    with pytest.raises(ValueError):
        Area(BROKEN_AREAS[1])
def test_broken_area2():
    with pytest.raises(ValueError):
        Area(BROKEN_AREAS[2])


def test_datetime_format():
    path = Path("database-2024-01-01-something.sql")
    datetime_format = "%Y-%m-%d"
    ts = extract_date_from_filename(path, datetime_format)
    assert ts == pd.Timestamp("2024-01-01")

def test_attach_timestamp1():
    path = Path("database-2024-01-01-something.sql")
    tp = TimedPath(path)
    tp.attach_timestamp(datetime_format="%Y-%m-%d")
    assert tp.timestamp == pd.Timestamp("2024-01-01")

def test_attach_timestamp2():
    path = TEST_FOLDER / "--some-test-file--"
    if path.exists():
        path.unlink()
    now = pd.Timestamp.now()
    path.touch()
    tp = TimedPath(path)
    tp.attach_timestamp()
    assert (tp.timestamp - now) < pd.Timedelta(milliseconds=50)

def test_attach_timestamp3():
    files = ALL_FILES
    folder = TEST_FOLDER / "planetlab"
    if not folder.exists():
        folder.mkdir()
    for file in folder.glob("*"):
        file.unlink()
    for file in files:
        path = folder / file
        path.touch()

    area_dict = PLANETLAB_AREA
    area_dict['folder'] = str(folder)
    area_dict['policy'] = POLICY10
    area = Area(area_dict)
    area.clean()
