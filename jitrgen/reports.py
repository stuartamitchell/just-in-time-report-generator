import pandas as pd
from jitrgen.student import Student

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

    def __init__(self, setup_sheet, students_sheet):
        self.questions = None
        self.totals = None
        self.topics = None
        self.topic_totals = None
        self.type_totals = None
        self.students = None
        self.reports = None

        self.__read_data(setup_sheet, students_sheet)
        self.reports = self.__generate_reports()

    def __read_data(self, setup_sheet, students_sheet):
        '''
        read the data from xlsx_file and populate class attributes except for reports

        Parameters
        ----------
        xlsx_file : file
            an xlsx file containing student data and setup information about an assessment item
        '''

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

    def __topic_descriptors(self, percentages):
        '''
        Returns a list of descriptors for the topics given percentages

        Parameters
        ----------
        percentages : list
            the list of percentage scores the student achieved in each topic

        Returns
        -------
        dict
            a dictionary keyed by descriptor, values a list of topics
        '''
        achievement_descriptors = {}

        for i, elem  in enumerate(self.topics):
            descriptor = 'poor'

            if percentages[i] >= 0.4 and percentages[i] < 0.5:
                descriptor = 'limited'
            elif percentages[i] >= 0.5 and percentages[i] < 0.7:
                descriptor = 'satisfactory'
            elif percentages[i] >= 0.7 and percentages[i] < 0.85:
                descriptor = 'advanced'
            elif percentages[i] >= 0.85:
                descriptor = 'exceptional'
            
            if descriptor not in achievement_descriptors.keys():
                achievement_descriptors[descriptor] = [elem]
            else:
                achievement_descriptors[descriptor].append(elem)
        
        return achievement_descriptors

    def __type_descriptors(self, percentages):
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

        for i, type  in enumerate(self.types):
            descriptor = 'limited'

            if percentages[i] >= 0.5 and percentages[i] < 0.7:
                descriptor = 'some'
            elif percentages[i] >= 0.75:
                descriptor = 'high'
            
            achievement_descriptors[type] = descriptor
        
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
            report = '{}, you have demonstrated'.format(student.preferred) 

            percentages_by_topic, percentages_by_type = self.__percentages(student)

            topic_descriptors = self.__topic_descriptors(percentages_by_topic)
            type_descriptors = self.__type_descriptors(percentages_by_type)

            topic_phrase = ''

            for i, descriptor in enumerate(topic_descriptors.keys()):
                if i == len(topic_descriptors.keys()) - 1 and i > 0:
                    topic_phrase += ', and '
                elif i > 0:
                    topic_phrase += ', '
                else:
                    topic_phrase += ' '
                
                if descriptor in ['advanced', 'exceptional']:
                    topic_phrase += 'an {} understanding of '.format(descriptor)
                else:
                    topic_phrase += 'a {} understanding of '.format(descriptor)

                topics = topic_descriptors[descriptor]

                for j, topic in enumerate(topics):
                    if j == 0:
                        topic_phrase += topic
                    elif j == len(topics) - 1 and j > 0:
                        topic_phrase += ', and ' + topic
                    else:
                        topic_phrase += ', ' + topic

            topic_phrase += '.'

            report += topic_phrase

            type_phrase = ' '

            if type_descriptors['r'] == 'limited':
                type_phrase += 'It appears that you have experienced difficulties with the routine problems covered in the unit. Please ensure that you are asking enough questions in class to build your understanding of the procedures and complete sufficient revision.'
            elif type_descriptors['r'] == 'some' and type_descriptors['nr'] in ['limited', 'some']:
                type_phrase += 'You have shown some competancy with the routine problems in the paper. In your homework, focus on building fluency by adding time pressure into your practice. Consider engaging with some of the enrichment materials to strengthen your capacity to apply your knowledge in novel situations.'
            elif type_descriptors['r'] == 'some' and type_descriptors['nr'] == 'high':
                type_phrase += 'You have shown a high capacity to apply your knowledge in novel situations, but have not demonstrated a similar ability in the routine problems. This suggests that you are undertaking insufficient practice of the fundamentals. Ensure that you strengthen your fundamentals before focussing on problem solving.'
            elif type_descriptors['r'] == 'high' and type_descriptors['nr'] in ['limited', 'some']:
                type_phrase += 'You have demonstrated a high capacity to handle the routine problems in the paper, but have not been able to apply your knowledge to novel situations to the same degree. Consider devoting a greater proportion of your practice to problem-solving activities.'
            elif type_descriptors['r'] == 'high' and type_descriptors['nr'] == 'high':
                type_phrase += 'You have shown a high degree of fluency in both the routine and non-routine problems in the paper. Keep up the hard work!'

            report += type_phrase

            report += ' Please read the feedback in your paper carefully for a detailed account of your achievement in this assessment.'

            reports.append(report)
            
        return reports
