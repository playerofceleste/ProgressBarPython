from time import sleep
 
### Global Options ###||
FILLED = '-' #Text that represents the filled section
UNFILLED = ' ' #Text that represents the unfilled section
CURSOR = '>' #Last unit of the filled section, ignored if SHOW_CURSOR is False
SHOW_CURSOR = True #Set to False to remove the cursor
ROUNDING = 2 #How rounded displayed stats should be
DISPLAY_NAME = False #Display the provided bar name (notably not the object's name, but self.name, provided during init)
IGNORE_SIZE_WARNS = False #Allows possible size errors to be ignored. Here be dragons
#######################||
 
#This renders the cursor the same as the rest of the bar
if not SHOW_CURSOR:
    CURSOR = FILLED
 
 
class ProgressBar:
 
    def __init__(self, name: str, width: int, init_value: int):
        self.width = width
        self.init_value = init_value
        self.init_width = width
        self.value = init_value
        self.name = name
        self.update(self.value)
 
    def value_check(self):
        """By default returns True but any fatal errors will change the output to be False"""
        valid = True
 
        if self.value >= 0 and not type(self.value) is int:
            print(f'[{self.name}]: ERR: Invalid value ({self.value})')
            valid = False
        if self.width > 0 and not type(self.width) is int :
            print(f'[{self.name}]: ERR: Invalid width ({self.width})')
            valid = False
        if self.width < 10 and not IGNORE_SIZE_WARNS:
            print(f'[{self.name}]: WARN: Width ({self.width}) should be greater than 10 ')
        if valid and self.width < self.value and not IGNORE_SIZE_WARNS:
            print(f'[{self.name}]: ERR: Width ({self.width}) less than value ({self.value})')
            valid = False
        if valid:
            return True
        else:
            return False
 
    def update(self, value: int):
        """Updates (prints) the progress bar"""
        self.value = value
        if self.value_check():
            rounded_percentage = round((self.value / self.width * 100), ROUNDING)
            unfilled_section = (self.width - self.value) * UNFILLED
            filled_section = ((self.value - 1) * FILLED) + CURSOR
            if DISPLAY_NAME:
                name_affix = self.name + ' '  # To account for the missing space that would normally not be there
            else:
                name_affix = '' #Empty
            print('\r', end = '') #This begins the line overwrite
            print(f'[[{filled_section + unfilled_section}]] {name_affix}[{rounded_percentage}%]', end = '', flush = True)
    def increment(self, by = 1):
        """Increments the value of the bar by a specified amount, defaults to 1"""
        self.update(self.value + by)
     
    def decrement(self, by = 1):
        """Decrements the value of the bar by a specified amount, defaults to 1"""
        self.update(self.value - by)
    
    def invert(self):
        """Inverts the filled section"""
        self.update(self.width - self.value)
     
    def zero(self):
        """Sets the bar's value to zero"""
        self.update(0)
     
    def change_width(self, new_width: int):
        self.width = new_width
        self.update(self.value)
     
    def reset(self):
        """Sets the value to the initially assigned value"""
        self.update(self.init_value)
        self.change_width(self.init_width)
