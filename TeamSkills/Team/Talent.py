'''
Created on Jan 15, 2021

@author: jaqua
'''

class Talent(object):
    '''
    classdocs
    '''


    def __init__(self, firstName, lastName, title, level, skillset):
        '''
        Constructor
        '''
        self.firstname = firstName
        self.lastname = lastName
        self.title = title
        self.level = level
        
        
        def fullName(self):
            return '{}'+'{}'.format(self.firstname,self.lastname)
        
        
        
#myTalent = Talent("Thandi", "Levons", "AssocDir", "EG104","none")