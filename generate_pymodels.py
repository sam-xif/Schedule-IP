"""
Script that reads in models.py and generates pymodels.py
"""


import re
import ast
import string

INPUT='src/models.py'
OUTPUT='src/pymodels.py'

# Parser states
START=0
INCLASS=1
OUTOFCLASS=2

indent_level=0
indent_sequence=''

pymodelbase = """# This file was auto-generated by generate_pymodels.py

from src import models

class PyModelBase:
    @staticmethod
    def __import__(data):
        raise NotImplementedError
        
    def __export_new__(self):
        raise NotImplementedError

    def __export__(self):
        raise NotImplementedError
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        # Standard hash function
        hashes = [self.__dict__[x].__hash__() for x in self.__dict__ if x is not None]
        hashSum = 0
        for hash in hashes:
            hashSum = 31 * hashSum + hash
        return hashSum
    

"""

def unescape_expansion(exp):
    """
    Unescapes closing curly braces because they interfere with the regexes
    """
    return re.sub(r'\\}', '}', exp)

def generateClass(variables):
    template="""
class ${NAME:&}(PyModelBase):
    def __init__(self, ${FIELDS:&:, }, wrapped_object=None):
        ${FIELDS:self.&=&:\\n        }
        self.wrapped_object = wrapped_object
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.${NAME:&} or data is None:
            raise Exception("Invalid argument to __import__")

        return ${NAME:&}(${FIELDS:data.&:, }, wrapped_object=data)
        
    def __export_new__(self):
        return models.${NAME:&}(${FIELDS:&=self.&:, })

    def __export__(self):
        ${FIELDS:self.wrapped_object.&=self.&:\\n        }
        return self.wrapped_object
        
    def __repr__(self):
        return "${NAME:&}<${FIELDS:&={\\}:, }".format(${FIELDS:self.&:, })

"""
    
    for var in variables:
        # Dynamically generated regex pattern for each variable
        pattern = r'\$\{{({0}.*?)(?<!\\)\}}'.format(var)
        
        # Gets first occurence of pattern
        match = re.search(pattern, template)
        while match: # Loops until match is None
            # Perform expansion of the variables
            fields = match.group(1).split(':')
            if type(variables[var]) is list:
                subst = ast.literal_eval("'" + fields[2] + "'").join([re.sub(r'(?<!\\)&', x, ast.literal_eval("'" + unescape_expansion(fields[1]) + "'")) for x in variables[var]])
                template = template[0:match.start()] + subst + template[match.end():]
            elif type(variables[var]) is str:
                subst = re.sub(r'(?<!\\)&', variables[var], ast.literal_eval("'" + unescape_expansion(fields[1]) + "'"))
                template = template[0:match.start()] + subst + template[match.end():]
            else:
                raise Exception("Invalid variable type")
                
            # Loads in the next occurence
            match = re.search(pattern, template)
            
    return template

if __name__=="__main__":
    with open(INPUT, 'r') as infile:
        infileText = infile.readlines()
    state = START
    with open(OUTPUT, 'w+') as outfile:
        # Write the base class to the file
        outfile.write(pymodelbase)
        
        variables = {}
        variables["FIELDS"] = []
        for line in infileText:
            # Check if line starts with class, if so, we are in a class
            if line.startswith('class'):
                if state == INCLASS:
                    # Finish the class if we encounter a new class while already in a class
                    outfile.write(generateClass(variables))
                    variables = {}
                    variables["FIELDS"] = []
                variables["NAME"] = line.split(' ')[1].split('(')[0].strip()
                if state == START or state == OUTOFCLASS:
                    state = INCLASS
            elif state == INCLASS:
                if line.strip() != '':
                    # If the line is not blank, assume it is an attribute
                    # Check if the line is not a comment
                    if re.match(r'\s+', line) is not None:
                        if re.match(r'\s*#', line) is None:
                            attrib = line.strip().split('=')[0].strip()
                            if not attrib.startswith('__'):
                                variables["FIELDS"].append(attrib)
                    else:
                        # This else clause handles output of the last class in the sequence
                        state = OUTOFCLASS
                        outfile.write(generateClass(variables))
                        variables = {}
                        variables["FIELDS"] = []