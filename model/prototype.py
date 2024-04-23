from abc import ABC, abstractclassmethod

'''Allows for cloning of user-defined objects'''
class Prototype(ABC):
    """
    An abstract base class that specifies the Prototype design pattern. This pattern is used to create duplicate objects 
    while keeping performance in mind. It is particularly useful when object creation is costly, and you need a similar object
    multiple times.

    Classes that inherit from this should implement the `clone` method, which is used to make a deep copy of the object.
    """    
    
    # Returns a deep copy of this object 
    @abstractclassmethod
    def clone(self):
        """
        Creates a deep copy of the object that implements this method. This method should be overridden to return 
        a deep copy of the instance it is called on.

        Returns:
        Prototype: A new object that is a deep copy of the instance.
        """        
        pass
