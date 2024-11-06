'''
Introduction:
    The @classmethod decorator in Python is used to define a method that is bound to the class and not the 
    instance of the class. This means that the method can be called on the class itself rather than on instances
    of the class. 

    When a method is defined using the @classmethod decorator, the method receives the class (cls) as 
    its first argument, rather than an instance (self).

Class Method vs Static Method:
    The main differences between class methods and static methods are:
        Class Method: Takes cls as the first parameter and can access or modify class state. 
        Static Method: Does not take any specific parameters and cannot access or modify class state. 

Factory Method:
    Factory methods are methods that return an instance of the class, often using different input parameters
'''

class Geeks:
    course = "DSA"
    list_of_instances = []

    def __init__(self, name):
        self.name = name
        Geeks.list_of_instances.append(self)

    @classmethod
    def get_course(cls):
        return f"Course: {cls.course}"

    @classmethod
    def get_instance_count(cls):
        return f"Number of instances: {len(cls.list_of_instances)}"

    @staticmethod
    def welcome_message():
        return "Welcome to Geeks for Geeks!"


# Creating instances
g1 = Geeks("Alice")
g2 = Geeks("Bob")

# Calling class methods
print(Geeks.get_course())
print(Geeks.get_instance_count())

# Calling static method
print(Geeks.welcome_message())

# Output:
# Course: DSA
# Number of instances: 2
# Welcome to Geeks for Geeks!

######################################################
'''Common Use Case: Factory Method'''

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_string):
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)

# Creating an instance using the factory method
date = Date.from_string('2023-07-16')
print(date.year, date.month, date.day)

# Output:
# 2023 7 16