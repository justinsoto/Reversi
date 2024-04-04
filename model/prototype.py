from abc import ABC, abstractclassmethod

'''Allows for cloning of user-defined objects'''
class Prototype(ABC):
    
    # Returns a deep copy of this object 
    @abstractclassmethod
    def clone(self):
        pass
