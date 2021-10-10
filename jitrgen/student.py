class Student:
    '''
    A class used to represent student achievement in an assessment

    ...
    Attributes
    ----------
    fullname : str
        the student's full name

    preferred : str
        the student's preferred name

    results : list
        a list of tuples of student results (question, topic, score)

    Methods
    -------
    by_question()
        Returns the student results by question

    by_topic()
        Returns the student results by topic

    by_type()
        Returns the student results by type
    '''

    def __init__(self, surname, firstname, results):
        self.fullname = surname + ', ' + firstname

        if '(' in firstname:
            preferred = firstname.split(' ')
            self.preferred = preferred[1][1:-1]

        else:
            self.preferred = firstname

        self.questions = [t[0] for t in results]
        self.topics = [t[1] for t in results]
        self.types = [t[2] for t in results]
        self.totals = [t[3] for t in results]

    def __label_totals(self, labels):
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
        label_totals = list(zip(labels, self.totals))

        totals = []

        for label in set_labels:
            total = sum([t[1] for t in label_totals if t[0] == label])
            totals.append((label, total))

        totals.sort()

        return totals
    
    def by_question(self):
        '''
        Returns a list of the student's results by question
        '''

        return self.__label_totals(self.questions)

    def by_topic(self):
        '''
        Returns a list of the student's results by topic
        '''

        return self.__label_totals(self.topics)

    def by_type(self):
        '''
        Returns a list of the student's results by type
        '''

        return self.__label_totals(self.types)

    