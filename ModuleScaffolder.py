"""
Module responsible for collating all source files into a single file.
This is a utility in order to upload the source code to Kaggle's Kernel
as a single file, since the competition does not allow custom module beyond
what is in the Kernel editor. 
"""

import random
import os
import regex


PATH = './notebooks/library/'
DOTTED_LINE = '# ---------------------------------------------------------------\n' 
SEPARATOR = '\n\n' +\
              '# ----------------- SECTION AUTO ASSEMBLED ----------------------\n' + DOTTED_LINE

def build(output_module_name = None, local_model_name = None):
    """
    Compiles a single file containing all source codes.

    Parameters
    --------------

    output_module_name: (optional) the name of the file being outputed
    local_model_name: (required) the name of the model orchestrator file
    """

    def read_file(file):
        f = open(file, "r")
        c = f.read()
        f.close()
        return c

    def replace_imports(content):
        return regex.sub(r'from library\.[^\n]+', '', content)

    def load_model(content):
        if local_model_name is not None:
            m = read_file(local_model_name)
            m = m.split('# AUTO-REMOVE-ABOVE')[1]
            content += SEPARATOR + m
        return content

    if output_module_name is None:
        output_module_name = 'modelbuild' + str(random.randint(1, 100000)) + '.py'

    files = os.listdir(PATH)
    
    content = ''

    content += read_file('./settings/kaggle.py')

    for file in files:
        if(not file.endswith('.py')):
            continue
        content +=  SEPARATOR + read_file(PATH + file)


    content += SEPARATOR + DOTTED_LINE + DOTTED_LINE + DOTTED_LINE

    content = load_model(content)

    content = replace_imports(content)

    out = open(output_module_name, 'w')
    out.write(content)
    out.close()


    return output_module_name

