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

        print(self.reports)


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

        # set up with duplicates for early set up
        self.topics = setup_sheet['Topic']
        self.types = setup_sheet['Type']
        
        self.questions = setup_sheet['Question']
        self.totals = setup_sheet['Total']

        self.students = self.__create_students(students_sheet.itertuples())

        self.topic_totals = self.__create_totals(self.topics, self.totals)
        self.type_totals = self.__create_totals(self.types, self.totals)

        # remove duplicates now that we don't need them
        self.topics = list(set(self.topics))
        self.topics.sort()
        self.types = list(set(self.types))
        self.types.sort()

        print(self.topics)
        print(self.types)

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
            totals.append(total)

        return totals

    def __percentages(self, student):
        '''
        Get percentage totals topic and type of question as arrays

        Returns
        -------
        tuple of lists
            the lists of percentage totals for each student 
        '''
        student_topic_totals = [t[1] for t in student.by_topic()]
        student_type_totals = [t[1] for t in student.by_type()]

        percentages_by_topic = []
        percentages_by_type = []
        
        for i in range(0, len(self.topic_totals)):
            percentages_by_topic.append(student_topic_totals[i] / self.topic_totals[i])

        for i in range(0, len(self.type_totals)):
            percentages_by_type.append(student_type_totals[i] / self.type_totals[i])
        
        return percentages_by_topic, percentages_by_type

    def __descriptors(self, category, percentages):
        '''
        Returns a list of descriptors for the types given percentages

        Parameters
        ----------
        percentages : list
            the list of percentage scores the student achieved in the category

        Returns
        -------
        dict
            a dictionary keyed by descriptor values a list of category elements
        '''

        achievement_descriptors = {}

        for i, elem  in enumerate(category):
            descriptor = 'poor'

            if percentages[i] >= 0.5 and percentages[i] < 0.75:
                descriptor = 'satisfactory'
            elif percentages[i] >= 0.75:
                descriptor = 'strong'
            
            if descriptor not in achievement_descriptors.keys():
                achievement_descriptors[descriptor] = [elem]
            else:
                achievement_descriptors[descriptor].append(elem)
        
        return achievement_descriptors
    
    def __generate_reports(self):
        '''
        Generates a report comment for each student


        Returns
        -------
        list
            a list of student reports
        '''
        
        reports = []

        for student in self.students:
            report = '{}, you have demonstrated '.format(student.preferred) 

            percentages_by_topic, percentages_by_type = self.__percentages(student)

            topic_descriptors = self.__descriptors(self.topics, percentages_by_topic)
            type_descriptors = self.__descriptors(self.types, percentages_by_type)

            print(student.preferred, percentages_by_topic, topic_descriptors, percentages_by_type, type_descriptors)

            reports.append(report)
            
        return reports

if __name__ == '__main__':
    test_file = os.path.join(os.getenv('HOME'),'Desktop/test_data.xlsx')
    reports = Reports(test_file)
