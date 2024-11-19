# pylint: disable=missing-docstring, wildcard-import, multiple-statements

# from unittest import TestCase

from backups_rotate import Policy

from tests.samples import *
from tests.policies import *


# the generic method is to compare the output of the policy
# with the expected output
def _test_policy_from_constants(sample_index, policy_index):
    policy_dict = globals()[f'POLICY{policy_index}']
    sample = globals()[f'sample{sample_index}']()
    kept = Policy(policy_dict).keep_timestamps(sample)
    expected = globals()[f'POLICY{policy_index}_SAMPLE{sample_index}']
    assert kept.sum() == expected

def test_policy_1_1(): _test_policy_from_constants(1, 1)
def test_policy_2_1(): _test_policy_from_constants(2, 1)
def test_policy_1_2(): _test_policy_from_constants(1, 2)
def test_policy_2_2(): _test_policy_from_constants(2, 2)
def test_policy_1_3(): _test_policy_from_constants(1, 3)
def test_policy_2_3(): _test_policy_from_constants(2, 3)
def test_policy_1_4(): _test_policy_from_constants(1, 4)
def test_policy_2_4(): _test_policy_from_constants(2, 4)
def test_policy_1_10(): _test_policy_from_constants(1, 10)
def test_policy_2_10(): _test_policy_from_constants(2, 10)

def test_policy_2_11(): _test_policy_from_constants(2, 11)
