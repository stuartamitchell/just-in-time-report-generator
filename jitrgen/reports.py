import os
import pandas as pd
from student import Student

class Reports:
    '''
    A class to represent of a set of student reports for an assessment

    ...
    Attributes
    ----------
    students : list
        A list of Student objects

    reports : list
        A list of report comments

    Methods
    -------
    read_data(self, xlsx_file)
        reads the data from the xlsx file and populates several attributes

    create_students(self, rows)
        creates a list of Student objects with the data in xlsx_file

    create_topc_totals(self)
        creates a list of totals per topic in the assessment
    '''

    def __init__(self, xlsx_file):
        self.questions = None
        self.totals = None
        self.topics = None
        self.topic_totals = None
        self.students = None
        self.reports = None

        self.read_data(xlsx_file)

    def read_data(self, xlsx_file):
        '''
        '''
        setup_sheet = pd.read_excel(xlsx_file, sheet_name='Setup')
        students_sheet = pd.read_excel(xlsx_file, sheet_name='Students')

        self.questions = setup_sheet['Question']
        self.totals = setup_sheet['Total']
        self.topics = setup_sheet['Topic']

        self.students = self.create_students(students_sheet.itertuples())

        self.topic_totals = self.create_topic_totals()

    def create_students(self, rows):
        '''
        '''

        students = []

        for row in rows:
            student = row[1:]
            
            surname = student[0]
            firstname = student[1]
            
            scores = student[2:]
            results = list(zip(self.questions, self.topics, scores))

            students.append(Student(surname, firstname, results))

        return students

    def create_topic_totals(self):
        topic_totals = []
        
        topics = list(set(self.topics))

        for topic in topics:
            topic_total = sum([t[1] for t in list(zip(self.topics, self.totals)) if t[0] == topic])
            topic_totals.append((topic, topic_total))

        return topic_totals

if __name__ == '__main__':
    test_file = os.path.join(os.getenv('HOME'),'Desktop/test_data.xlsx')
    reports = Reports(test_file)

    print(list(zip(reports.questions, reports.totals, reports.topics)))
    print(reports.topic_totals)
