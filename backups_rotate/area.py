"""
an area has a name, it refers to a set of files together with a policy
"""

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from .policy import Policy

def extract_date_from_filename(path: Path, dateformat) -> pd.Timestamp | None:
    """
    Extracts a date from a filename using the provided date format.

    Args:
        filename (str): The filename to search for a date.
        dateformat (str): A strptime-compliant date format to match.

    Returns:
        datetime: The extracted date if found, None otherwise.
    """
    filename = path.name
    # we need to know how many characters to try and match
    dummy = datetime(2000, 1, 1, 0, 0, 0)
    partial_length = len(dummy.strftime(dateformat))

    for i in range(len(filename) - partial_length + 1):
        substring = filename[i:i + partial_length]
        try:
            print(substring)
            return pd.Timestamp(datetime.strptime(substring, dateformat))
        except ValueError:
            continue
    return None


@dataclass
class TimedPath:
    path: Path
    timestamp: pd.Timestamp = None

    def attach_timestamp(self, *, file_format: str = None, use_modification_time: bool = False):
        """
        attach a timestamp to the path
        if file_format is provided, it is used to parse the timestamp from the filename
        otherwise, and if use_modification_time is True, the modification time is used
        the default is to use the creation time
        """
        # no format
        if file_format is None:
            if use_modification_time:
                self.timestamp = pd.Timestamp(self.path.stat().st_mtime)
            else:
                self.timestamp = pd.Timestamp(self.path.stat().st_ctime)
            return
        # otherwise use the format
        date = extract_date_from_filename(self.path, file_format)
        if date is None:
            raise ValueError(f"Could not extract date from {self.path} using {file_format}")
        self.timestamp = date


class Area:

        def __init__(self, area_dict: dict):
            self.name = area_dict['name']
            self.path = Path(area_dict['folder'])
            self.patterns = area_dict['files']
            self.policy = Policy(area_dict['policy'])

        def check(self):
            if not self.path.exists():
                raise ValueError(f"Folder {self.path} does not exist")
            if not self.path.is_dir():
                raise ValueError(f"{self.path} is not a folder")
            if not self.path.is_absolute():
                raise ValueError(f"{self.path} is not an absolute path")

        def populate():
            pass