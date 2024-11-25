"""
an area has a name, and a folder,
and it refers to a set of files defined by some patterns
together with a policy
"""

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from collections.abc import Iterator

import pandas as pd

from .policy import Policy


def extract_date_from_string(filename: str, dateformat: str) -> pd.Timestamp | None:
    """
    Extracts a date from a filename using the provided date format.

    Args:
        filename (str): The filename to search for a date.
        dateformat (str): A strptime-compliant date format to match.

    Returns:
        datetime: The extracted date if found, None otherwise.
    """
    # we need to know how many characters to try and match
    dummy = datetime(2000, 1, 1, 0, 0, 0)
    partial_length = len(dummy.strftime(dateformat))

    for i in range(len(filename) - partial_length + 1):
        substring = filename[i:i + partial_length]
        try:
            # print(substring)
            return pd.Timestamp(datetime.strptime(substring, dateformat))
        except ValueError:
            continue
    return None


def extract_date_from_path(path: Path, dateformat: str) -> pd.Timestamp | None:
    """
    Extracts a date from a path using the provided date format.
    First tries name, then its parent, until one is found.

    Args:
        path (Path): The path to search for a date.
        dateformat (str): A strptime-compliant date format to match.

    Returns:
        datetime: The extracted date if found, None otherwise.
    """
    for f in path.absolute().parts[::-1]:
        if date := extract_date_from_string(f, dateformat):
            return date


@dataclass
class TimedPath:
    """
    a path with a timestamp
    knows how to get the timestamp from the path or a format
    """
    path: Path
    timestamp: pd.Timestamp = None

    def attach_timestamp(self, *, datetime_format: str = None,
                         use_modification_time: bool = False):
        """
        attach a timestamp to the path

        if datetime_format is provided, it is used to parse the timestamp from
        the filename

        otherwise, and if use_modification_time is True, the modification time
        is used - the default is to use the creation time
        """
        # no format
        if datetime_format is None:
            if use_modification_time:
                self.timestamp = pd.Timestamp(self.path.stat().st_mtime, unit='s')
            else:
                self.timestamp = pd.Timestamp(self.path.stat().st_ctime, unit='s')
            return
        # otherwise use the format
        date = extract_date_from_path(self.path, datetime_format)
        if date is None:
            raise ValueError(
                f"Could not extract date from {self.path} using {datetime_format}")
        self.timestamp = date

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class Area:
    """
    an area is a set of files with a policy
    """

    def __init__(self, area_dict: dict):

        # mandatory fields
        try:
            self.name = area_dict['name']
            self.path = Path(area_dict['folder'])
            self.patterns = area_dict['patterns']
            self.policy = Policy(area_dict['policy'])
        except KeyError as e:
            raise ValueError(f"Missing key {e}") from e

        # optional fields
        self.datetime_format = area_dict.get('datetime_format', None)
        if 'use_creation_time' in area_dict and 'use_modification_time' in area_dict:
            raise ValueError(f"area {name}: cannot have both use_creation_time and use_modification_time")
        elif 'use_modification_time' in area_dict:
            self.use_modification_time = area_dict['use_modification_time']
        elif 'use_creation_time' in area_dict:
            self.use_modification_time = not area_dict['use_creation_time']
        else:
            self.use_modification_time = None
        self.type_ = area_dict.get('type', None)

        # for the record
        self.area_dict = area_dict
        # stats
        self.total = 0
        self.deleted = 0
        # list of TimedPath
        self._timed_paths = None
        self._kept = None
        # sanity check
        self._check()

    def __repr__(self):
        return f"Area({self.name} on {self.path} - {self.total} files, {self.deleted} deleted)"

    def _check(self):
        """
        sanity check
        """
        # no need to check for mandatory fields
        # as they are used in the constructor already
        allowed = set("name|folder|patterns|policy|datetime_format"
                      "|use_creation_time|use_modification_time|type".split("|"))
        # any non-supported key ? this can be dangerous
        unsupported = set(self.area_dict.keys()) - allowed
        if unsupported:
            raise ValueError(f"Invalid keys in {self.name} : {unsupported}")

        if not isinstance(self.patterns, list):
            raise ValueError(f"area {self.name}: invalid patterns, should be a list")
        if not isinstance(self.use_modification_time, (bool, type(None))):
            raise ValueError(f"area {self.name}: invalid use_modification_time - should be a boolean")
        if self.datetime_format is not None and not isinstance(self.datetime_format, str):
            raise ValueError(f"area {self.name}: invalid datetime_format in - should be a string")
        if self.use_modification_time is not None and self.datetime_format is not None:
            raise ValueError(f"area {self.name}: cannot have both use_modification_time and datetime_format {self.name}")
        if self.type_ is not None and self.type_ not in ("file", "folder", "symlink"):
            raise ValueError(f"area {self.name}: invalid type {self.type_}")

        # check the folder
        if not self.path.exists():
            raise ValueError(f"Folder {self.path} does not exist")
        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a folder")
        if not self.path.is_absolute():
            raise ValueError(f"{self.path} is not an absolute path")


    def _populate(self):
        """
        read the disk to populate the list of files
        """
        self._timed_paths = []
        for pattern in self.patterns:
            self._timed_paths.extend(self.path.glob(pattern))
        self._timed_paths = [TimedPath(path) for path in self._timed_paths]
        match self.type_:
            case "file":
                self._timed_paths = [tp for tp in self._timed_paths if tp.path.is_file()]
            case "folder":
                self._timed_paths = [tp for tp in self._timed_paths if tp.path.is_dir()]
            case "symlink":
                self._timed_paths = [tp for tp in self._timed_paths if tp.path.is_symlink()]
        self.total = len(self._timed_paths)

    def _attach_timestamp_to_files(self):
        """
        attach a timestamp to each file
        """
        for file in self._timed_paths[::]:
            try:
                file.attach_timestamp(
                    datetime_format=self.datetime_format,
                    use_modification_time=self.use_modification_time)
            except ValueError as e:
                print(f"WARNING: area {self.name} - ignoring file {file.path}: {e}")
                self._timed_paths.remove(file)
        # use TimedPath __lt__ to sort by timestamp
        self._timed_paths.sort()

    def read(self):
        """
        read the disk and computes which files to keep
        """
        self._populate()
        self._attach_timestamp_to_files()
        self._kept = self.policy.keep_timestamps([
            file.timestamp for file in self._timed_paths])
        self.deleted = 0
        for i, file in enumerate(self._timed_paths):
            if not self._kept[i]:
                self.deleted += 1


    def _iterate(self) -> Iterator[tuple[bool, Path, pd.Timestamp]]:
        """
        iterate on tuples (path: Path, kept: bool)
        """
        if self._kept is None:
            print("warning: area not read yet - bailing out")
            return
        for i, file in enumerate(self._timed_paths):
            yield (self._kept[i], file.path, file.timestamp)


    def list(self, *, deleted=True, kept=True, verbose=False):
        """
        shows the files in the area, with an indication of kept/deleted
        """
        if self._timed_paths is None:
            print("warning: area not populated yet")
            return
        if self._kept is None:
            print("warning: area not read yet - showing all files")
            for file in self._timed_paths:
                print(file)
            return
        for kept_file, file, ts in self._iterate():
            # show only selected entries
            if (deleted and not kept_file) or (kept and kept_file):
                status = "KEEP" if kept_file else "DELE"
                if not verbose:
                    print(file)
                else:
                    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                    print(status, ts_str, file)
        if verbose:
            print(f"{self.deleted} files deleted out of {self.total}")

    def delete(self, *, dry_run=True, verbose=False):
        """
        delete the files in the area
        """
        summary = {'kept': 0, 'deleted': 0, 'missing': 0}
        for kept_file, file, _ts in self._iterate():
            if kept_file:
                summary['kept'] += 1
                if dry_run:
                    print("dry-run: would KEEP  ", file)
                continue
            if dry_run:
                print("dry-run: would DELETE", file)
                summary['deleted'] += 1
            elif not file.exists():
                summary['missing'] += 1
                print("MISSING", file)
            else:
                summary['deleted'] += 1
                if verbose:
                    print("DELETING", file)
                file.unlink()
        if verbose:
            def item(k, v): return f"{v} {k} files"
            chunks = [item(k, v) for k, v in summary.items() if v]
            print(" / ".join(chunks))
