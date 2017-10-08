"""
Utilities for parsing and generating period codes, which contain various data about classes

period code:

first digit: whether the class is required
second digit: the number of times the class meets (usually 3 or 4, but some other classes may meet fewer times)
third digit: day on which the red dot occurs, if class does not meet 4 times a week (0 if no red dot)
fourth digit: period on which the class meets

Example:
1326 means that this is a required class which meets 3 times a week and has a red dot on Tuesday. The class meets 6th period
"""

class PeriodCode:
    def __init_(self, required, numMeetings, reddot, period):
        self.required = required
        self.numMeetings = numMeetings
        self.reddot = reddot
        self.period = period

    @classmethod
    def parse(cls, number):
        string = str(number)
        
        required = bool(int(string[0]))
        numMeetings = int(string[1])
        reddot = int(string[2])
        period = int(string[3])

        return PeriodCode(required, numMeetings, reddot, period)

