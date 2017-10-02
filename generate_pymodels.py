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
INFIELDS=2

indent_level=0
indent_sequence=''

def generateClass(variables):
    template="""
class ${NAME:&}(PyModelBase):
    def __init__(self, ${FIELDS:&:, }):
        ${FIELDS:self.&=&:\\n        }
        
    @staticmethod
    def __import__(data):
        if type(data) is not models.${NAME:&} or data is None:
            raise Exception("Invalid argument to __import__")

        return ${NAME:&}(${FIELDS:data.&:, })
        
    def __export__(self):
        return models.${NAME:&}(${FIELDS:&=self.&:, })
    """
    
    for var in variables:
        pattern = r'\$\{{({0}.*?)\}}'.format(var)
        match = re.search(pattern, template)
        while match:
            fields = match.group(1).split(':')
            if type(variables[var]) is tuple:
                subst = ast.literal_eval("'" + fields[2] + "'").join([re.sub(r'(?<!\\)&', x, ast.literal_eval("'" + fields[1] + "'")) for x in variables[var]])
                template = template[0:match.start()] + subst + template[match.end():]
            elif type(variables[var]) is str:
                subst = re.sub(r'(?<!\\)&', variables[var], ast.literal_eval("'" + fields[1] + "'"))
                template = template[0:match.start()] + subst + template[match.end():]
            else:
                raise Exception("Invalid variable type")
            match = re.search(pattern, template)
            
    return template

if __name__=="__main__":
    with open(INPUT, 'r') as infile:
        infileText = infile.readlines()
    state = START
    with open(OUTPUT, 'w+') as outfile:
        variables = {}
        for line in infileText:
            if line.startswith('class'):
                variables["NAME"] = line.split(' ')[1].split('(')[0].strip()
                if state == START:
                    state = INCLASS
                
                variables["NAME"] = line.split(' ')[1].split('(')[0].strip()
            elif state == INCLASS:
                if line.strip() != '':
                    
                    
                
                
        generateClass({'NAME': 'Student', 'FIELDS': ('graduatingClass', 'two', 'three')})