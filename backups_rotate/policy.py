"""
the Policy class is in charge of spotting the timestamps that are to be kept
"""


import numpy as np
import pandas as pd


# the periods are hard-coded for now
PERIODS = {
    'year': '1YE',
    'quarter': '1QE',
    'month': '1ME',
    'week': '1W',
    'day': '1D',
    'hour': '1h',
}


class Policy:

    """
    A policy is a set of rules that determine which timestamps are kept
    and which are discarded.
    It is definded by a dictionary that may have the following keys:
    'year', 'quarter', 'month', 'week', 'day', 'hour'
    with values that are either integers or the string 'infinite'.
    """

    def __init__(self, period_dict: dict):
        self.period_dict = period_dict
        for k in period_dict.keys():
            if k not in PERIODS:
                raise ValueError(f"Invalid period: {k}")

    def __repr__(self):
        return f"Policy({self.period_dict})"


    def count_validating_periods_for_timestamps(
            self, timestamps: list[pd.Timestamp]) -> np.ndarray:

        """
        Apply the policy to a list of timestamps
        returns a ndarray of size len(timestamps) and of type uint8
        that indicates which timestamps are to be kept

        specifically, the value indicates for how many period types
        the timestamp qualifies to be kept
        """

        total = len(timestamps)
        kept = np.zeros(total, dtype=np.uint8)

        index = pd.DatetimeIndex(timestamps)
        rank = range(total)
        df = pd.DataFrame(rank, index=index, columns=['rank'])

        df.sort_index(inplace=True)

        for period, value in self.period_dict.items():

            # isolate the last item per period
            last_per_period = df.resample(PERIODS[period]).last()
            # skip periods without any item
            last_per_period.dropna(inplace=True)
            # keep only the last <value> items if not infinite
            if value != 'infinite':
                if value < 1:
                    raise ValueError(
                        f"Invalid value for {period}: {value} - should be >= 1")
                last_per_period = last_per_period.iloc[-value:]
            last_per_period = last_per_period.astype(int)
            # print("===", period)
            # for rank in last_per_period['rank']:
            #     print(rank, timestamps[rank])
            # mark the items to be kept
            kept[last_per_period['rank']] += 1

        return kept

    def keep_timestamps(self, timestamps: list[pd.Timestamp]) -> np.ndarray:
        """
        a wrapper around count_validating_periods_for_timestamps
        that returns a boolean array instead
        """
        return self.count_validating_periods_for_timestamps(timestamps) > 0

    def indices_of_timestamps_to_keep(self, timestamps: list[pd.Timestamp]) -> list[int]:
        """
        return the indices of the timestamps to keep
        """
        return np.nonzero(self.keep_timestamps(timestamps))[0].tolist()
