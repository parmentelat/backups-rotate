# pylint: disable=missing-docstring

POLICY1 = {
    'hour': 'infinite',
}
# wrt sample1 we expect 44 entries
POLICY1_SAMPLE1 = 44
# all entries are kept with sample 2
POLICY1_SAMPLE2 = 7680

POLICY2 = {
    'year': 1,
}
POLICY2_SAMPLE1 = 1
POLICY2_SAMPLE2 = 1

POLICY3 = {
    'year': 'infinite',
}
POLICY3_SAMPLE1 = 4
POLICY3_SAMPLE2 = 1

POLICY4 = {
    'quarter': 3,
}
POLICY4_SAMPLE1 = 3
POLICY4_SAMPLE2 = 3


POLICY10 = {
    'year': 'infinite',
    'quarter': 3,
    'month': 2,
    'week': 4,
    'day': 5,
    'hour': 6,
}

# wrt sample1 we expect a maximum of
# - 4 years, 3 quarters, 2 months, 4 weeks, 5 days, 6 hours
# i.e. 24
# except that the latest event (#3) appears 6 times - so -5
# the last event of year 2023 (#23) appears for year and quarter so -1
# event #8 (2024-03-31) appears for quarter, month, week and day, so -3
# event #29 (2024-02-03) appears for week and day, so -1
# so bottom line is 24 - 5 - 1 - 3 - 1 = 14
POLICY10_SAMPLE1 = 14

# wrt sample2 we have one entry every hour between jan 1 and nov 17 2024
# so we expect 3+2+4+5+6+1 = 21, minus:
# very last event is present 6 times, so -5
# all other dimensions are orthogonal, so that's it
# 21 - 5 = 16
POLICY10_SAMPLE2 = 16


POLICY11 = POLICY10.copy()
POLICY11['month'] = 'infinite'

# one additional result for january to september
# but june and march were already picked for quarter
POLICY11_SAMPLE2 = POLICY10_SAMPLE2 + 9 - 2
