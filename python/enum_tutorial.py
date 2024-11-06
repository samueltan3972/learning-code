from enum import Enum

# https://docs.python.org/3/library/enum.html

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    @classmethod
    def all_option(cls):
        return [mode.name for mode in list(Color)]

print(Color.RED) # Output: Color.RED
print(Color.RED.name) # Output: RED
print(Color.RED.value) # Output: 1
print(Color(1)) # Output: Color.RED
print(Color['RED']) # Output: Color.RED

