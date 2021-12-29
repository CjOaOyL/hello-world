'''
Created on Jan 16, 2021

@author: jaqua
'''

class Skill(object):
    '''
    classdocs
    '''


    def __init__(self, skillname, modality, competency):
        '''
        Constructor
        '''
        self.name = skillname
        self.modality = modality
        self.competency = competency
        
        
        self.experience = [" "]
        
        
    def addExperience(self,experience):
        self.experience = [self.getExperience(self),experience]
        
    def getExperience(self):
        return self.experience
    
    
        
        