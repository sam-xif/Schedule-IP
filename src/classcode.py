"""
Provides a utility for parsing class codes
"""

import re

class ClassCode:
    def __init__(self, dept, level):
        self.dept = dept
        self.level = level

    def __eq__(self, other):
        return self.dept == other.dept and self.level == other.level

    @staticmethod
    def getClassCodeFromTitle(title):
        pattern = r'\s*([a-zA-Z]{3,})-?([0-9]{2,3}[a-zA-Z]*)\s*'
        match = re.match(pattern, title)
        if match is None:
            return None

        dept = match.group(1)
        level = match.group(2)

        return ClassCode(dept, level)
    
