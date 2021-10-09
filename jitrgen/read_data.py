import os
import pandas as pd

test_file = os.path.join(os.getenv('HOME'),'Desktop/template.xlsx')

setup_sheet = pd.read_excel(test_file, sheet_name='Setup')
students_sheet = pd.read_excel(test_file, sheet_name='Students')

