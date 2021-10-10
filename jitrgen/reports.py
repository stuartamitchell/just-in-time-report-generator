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
    '''

    def __init__(self, xlsx_file):
        self.questions = None
        self.totals = None
        self.topics = None
        self.topic_totals = None
        self.type_totals = None
        self.students = None
        self.reports = None

        self.__read_data(xlsx_file)
        self.reports = self.__generate_reports()


    def __read_data(self, xlsx_file):
        '''
        read the data from xlsx_file and populate class attributes except for reports

        Parameters
        ----------
        xlsx_file : file
            an xlsx file containing student data and setup information about an assessment item
        '''
        setup_sheet = pd.read_excel(xlsx_file, sheet_name='Setup')
        students_sheet = pd.read_excel(xlsx_file, sheet_name='Students')

        self.questions = setup_sheet['Question']
        self.totals = setup_sheet['Total']
        self.topics = setup_sheet['Topic']
        self.types = setup_sheet['Type']

        self.students = self.__create_students(students_sheet.itertuples())

        self.topic_totals = self.__create_totals(self.topics, self.totals)
        self.type_totals = self.__create_totals(self.types, self.totals)

    def __create_students(self, rows):
        '''
        creates the list of student objects

        Parameters
        ----------
        rows : list
            a list of student data from an excel spreadsheet

        Returns
        -------
        list
            a list of Student objets
        '''

        students = []

        for row in rows:
            student = row[1:]
            
            surname = student[0]
            firstname = student[1]
            
            scores = student[2:]
            results = list(zip(self.questions, self.topics, self.types, scores))

            students.append(Student(surname, firstname, results))

        return students

    def __create_totals(self, labels, totals):
        '''
        creates a list of tuples (label, total)

        Parameters
        ----------
        labels : list
            a list of labels for the tuple

        totals : list
            a list of totals for the tuple

        Returns
        -------
        list
            a list of tuples of the form (label, total)
        '''
        set_labels = list(set(labels))
        set_labels.sort()
        label_totals = list(zip(labels, totals))

        totals = []

        for label in set_labels:
            total = sum([t[1] for t in label_totals if t[0] == label])
            totals.append((label, total))

        return totals

    def __get_percentages(self, student):
        '''
        Get percentage totals topic and type of question as arrays

        Returns
        -------
        tuple of lists
            the lists of percentage totals for each student 
        '''
        student_topic_totals = [t[1] for t in student.by_topic()]
        student_type_totals = [t[1] for t in student.by_type()]

        topic_totals = [t[1] for t in self.topic_totals]
        type_totals = [t[1] for t in self.type_totals]

        percentages_by_topic = []
        percentages_by_type = []
        
        for i in range(0, len(topic_totals)):
            percentages_by_topic.append(student_topic_totals[i] / topic_totals[i])

        for i in range(0, len(type_totals)):
            percentages_by_type.append(student_type_totals[i] / type_totals[i])
        
        return percentages_by_topic, percentages_by_type
    
    def __generate_reports(self):
        '''
        Generates a report comment for each student


        Returns
        -------
        list
            a list of student reports
        '''
        descriptors = ['very limited', 'limited', 'satisfactory', 'proficient', 'advanced']

        thresholds = [
                        (0, 0.4, 'very limited'),
                        (0.4, 0.5, 'limited'),
                        (0.5, 0.7, 'satisfactory'),
                        (0.7, 0.85, 'proficient'),
                        (0.85,1, 'advanced')
                    ]
        
        reports = []

        for student in self.students:
            percentages_by_topic, percentages_by_type = self.__get_percentages()

            topic_achievement_descriptors = []

            topics = list(set(self.topics))
            topics.sort()

            for topic in topics:
                ''''''

        return reports

if __name__ == '__main__':
    test_file = os.path.join(os.getenv('HOME'),'Desktop/test_data.xlsx')
    reports = Reports(test_file)
