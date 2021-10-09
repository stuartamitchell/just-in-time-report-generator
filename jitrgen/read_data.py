import os
import pandas as pd
from student import Student

test_file = os.path.join(os.getenv('HOME'),'Desktop/test_data.xlsx')

setup_sheet = pd.read_excel(test_file, sheet_name='Setup')
students_sheet = pd.read_excel(test_file, sheet_name='Students')

print(setup_sheet)

questions = setup_sheet['Question']
topics = setup_sheet['Topic']

tq_list = list(zip(topics, questions))

topics = list(set(setup_sheet['Topic']))

topics_with_questions = []

for topic in topics:
    questions = [q for t,q in tq_list if t == topic]
    topics_with_questions.append((topic, questions))
