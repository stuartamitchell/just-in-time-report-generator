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
    get_results_by_topic()
        Returns the student results topic
    '''

    def __init__(self, surname, firstname, results):
        '''
        
        '''

        self.fullname = surname + ', ' + firstname

        if '(' in firstname:
            preferred = firstname.split(' ')
            self.preferred = preferred[1][1:-1]

        else:
            self.preferred = firstname

        self.results = results
    
    def get_results_by_topic(self):
        '''
        Returns a list of the student's results by topic
        '''

        topics = list(set([t[1] for t in self.results]))

        results_by_topic = []

        for topic in topics:
            topic_result = sum([t[2] for t in self.results if t[1] == topic])
            results_by_topic.append((topic, topic_result))

        return results_by_topic

    