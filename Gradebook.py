# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:29:24 2019

@author: josea
Gradebook for Students Project
"""
# Objects for Grade Categories


class GrCat(object):
    # --------------------------------------------------------------------------
    # initialization and overloaded operators
    
    def __init__(self, name, avg=None, parent=None, w=0):
        """
        Initializes Grade Category object. Gr_Cat instances have the following
        data attributes:
            
            name - Name of the category, taken as a string parameter on initialization.
            
            avg - the grade average of the category, set to None by default, 
            int or float greater than or equal to 0 otherwise. An average can 
            be manually inputted, or the average can be automatically calculated 
            from given grades.
            
            grades - Dictionary, empty on initialization. Can be filled with 
            assignments/grades, and average can be computed using it. Keys are 
            assignment names, values are tuples(grade and assignment date)
            
            parent - a Gradebook object that the Gr_Category object is a part of.
            
            manual_avg - A flag, indicating whether avg has been manually set 
            or computed by the grades dictionary.
            
        Arguments:
            name - a string, the name of the category.
            avg - optional parameter, the current class average. If a parameter
            is given, the function will automatically set the manual_avg flag 
            to True.
            parent - optional parameter, a Gradebook object. Set to None by default.
            w - an optional parameter; the weight that the category gets in the parent
            gradebook. Will only be used if a parent is assigned. Set to 0 by
            default.
        """   
        try:
            assert type(name) == str and (is_num(avg) or avg is None)
            if avg is not None:
                assert avg >= 0
            self.name = name
            self.avg = avg
            self.grades = {}
            self.parent = parent
            if avg is None:
                self.manual_avg = False
            else:
                self.manual_avg = True
            if parent: 
                parent.add_cat(self, w)

        except AssertionError:
            print ('GrCat __init__: invalid input')
    
    def __str__(self):
        """
        When print is called, a Gr_Category instance will print its name and its average.
        """
        return "Category Name: " + self.name + "\n" + "Average: " + str(self.avg)
    # --------------------------------------------------------------------------
    # Getters

    def get_name(self):
        """
        Returns the name of the category.
        """
        return self.name
    
    def get_avg(self):
        """
        Returns the current grade average of the category.
        """
        return self.avg
    
    def get_grades(self):
        """
        Returns a deep copy of the grade dictionary.
        """
        import copy
        return copy.deepcopy(self.grades)
    
    def print_assignment_info(self, name):
        """
        Given an assignment in the student's gradebook, prints the assignment's 
        name, grade, and date.
        Arguments:
            name - a string, name of the assignment
        """
        try:
            print("Name: " + name)
            print("Grade: " + str(self.grades[name][0]))
            print("Date: " + str(self.grades[name][1]))
        except KeyError:
            print("Assignment not found.")
            
    def print_all_assignments(self):
        """Calls the print assignment info method on all assignments, separating
        them with a line in between.
        """
        for grade in self.grades:
            self.print_assignment_info(grade)
            print()

    # --------------------------------------------------------------------------
    # Adjust data attributes
    def rename(self, new_name):
        """
        Changes the category's name to the given new name.
        Arguments:
            new_name - a string
        """
        try:
            assert type(new_name) == str
            self.name = new_name
        except AssertionError:
            print('new_name: Invalid input.')
        
    def force_avg(self, new_avg):
        """
        Manually changes the category's grade average to a given average. Average
        cannot be lower than 0. If average is higher than 100, the function 
        will run but the user will be alerted.
        
        Arguments:
            new_average - a float or int greater than or equal to 0
        """
        try:
            assert new_avg >= 0 and (is_num(new_avg))
            self.avg = new_avg
            self.manual_avg = True
            if new_avg > 100:
                print('Warning: Average has been set to a number greater than 100.')
            if self.parent:
                self.parent.add_cat(self)
        except AssertionError:
            print('Please input a number higher than 0.')
            
    def auto_avg(self):
        """If manual_avg is set to True, changes it to False, and auto-updates 
        the category's grade.
        """
        self.manual_avg = False
        self.update_avg()

    def add_grade(self, name, grade, date=None):
        """
        Adds an assignment to the Category's grade dictionary.
        Arguments:
            name - a string, name of the assignment
            grade - a float or int higher than or equal to 0
            date - optional parameter, a tuple containing month, day, year (all 
            ints). Month must be between 1 and 12, day must be between 0 and 31.
            TODO: What happens if the grade is already there?
        """
        try:
            # Check for valid inputs
            assert type(name) == str
            assert is_num(grade)
            assert grade >= 0
            assert (type(date) == tuple or date is None)
            if type(date) == tuple:
                assert len(date) == 3
                for hopefully_i in date:
                    assert type(hopefully_i) == int
                assert in_range(date[0], 1, 12)
                assert in_range(date[1], 1, 31)
                assert date[2] > 0
            
            # adds the grade if all is good
            self.grades[name] = (grade, date)
            self.update_avg()

        except AssertionError:
            print('add_grade: invalid input.')
            
    def remove_grade(self, name):
        """
        Removes an assignment from the Category's grade dictionary, if the assignment exists.
        Arguments:
            name - a string, name of the assignment to be deleted
        """
        try:
            del self.grades[name]
            self.update_avg()
        except KeyError:
            print("Assignment not found in this category.")
            
    # --------------------------------------------------------------------------
    # Other operations
    
    def update_avg(self):
        """
        Updates the category's grade average, based on the student's grades.
        If the manual flag is set to False, this function will execute automatically
        when grades are added or removed. If there are no assignments in the 
        grade dictionary, sets the average to "None".
        
        Does nothing if manual flag is set to True.
        """
        try:
            if self.manual_avg is False:
                dividend = 0
                divisor = len(self.grades)
                for assign_data in self.grades.values():
                    dividend += assign_data[0]
                self.avg = round(dividend / divisor, 2)
                if self.parent:
                    self.parent.add_cat(self)
        except ZeroDivisionError:
            self.avg = None
            
# ------------------------------------------------------------------------------


class Gradebook(object):
    # ----------------------------------------------------------------------
    # Initialization and overloaded operators
    def __init__(self, Gr_sys = False):
        """
        Initialized Gradebook object. Gradebook objects have the following
        data attributes:

        Cats - dictionary containing category names as keys and
        tuples as values. The tuples contain a Gr_Category object, the object's
        current average, and the weight the category gets in the overall grade.

        Class_avg - a float greater than or equal to 0. Current class average.
        Computed automatically using given category data.

        valid_weight - a boolean flag, set to true if all the given category
        weights add up to 100, false otherwise. Set to false on initialization.

        Gr_sys - A dictionary that maps letters as keys and the grade
        averages that represent them as values. Values are tuples, with
        both element of the tuples being ints or floats. The first element
        is the minimum grade for that letter grade, and the second element
        is the maximum for that letter grade.
        Initialized by default with a standard abcdf grading scale.

        This function has an optional parameter:
            Gr_sys: a boolean. If set to True, Gradebook will be initialized
            with an empty dictionary for Gr_sys for easier modification.
        """
        self.Cats = {}
        self.Class_avg = None
        self.valid_weight = False
        if Gr_sys is True:
            self.Gr_sys = {}
        else:
            self.Gr_sys = {"A":(90, 100), "B":(80, 89.99), "C":(75, 79.99),
                           "D":(70, 74.99), "F":(0, 69.99)}

    def __str__(self):
        cats = self.Cats.keys()
        return ("Current Categories: " + str(cats) + "\n" +
                "Current Average: " + str(self.Class_avg))

    # ----------------------------------------------------------------------
    # Getters and printers

    def get_letter_grade(self):
        if self.Gr_sys:
            for letter in self.Gr_sys:
                if in_range(self.Class_avg, self.Gr_sys[letter][0], self.Gr_sys[letter][1]):
                    return letter

    def get_cats(self):
        """
        Returns a deep copy of the category dictionary.
        """
        import copy
        return copy.deepcopy(self.Cats)

    def get_class_avg(self):
        """
        Returns the class average.
        """
        return self.Class_avg

    def get_gr_sys(self):
        """
        Returns a deep copy of the grade system dictionary.
        """
        import copy
        return copy.deepcopy(self.Gr_sys)

    def print_all_avg(self):
        """
        Prints all category averages and the final class average.
        """
        for cat in self.Cats.values():
            print("Category " + cat[0].name + ", Avg: " + str(cat[1]))
        print ("Class avg: " + str(self.Class_avg))

    # ----------------------------------------------------------------------
    # Adjust data attributes

    def add_cat(self, cat, weight=0):
        """
        Adds a category to the Cats dictionary. Also assigns its average and
        weight. This method is also called to update categories when they are
        modified.

        Arguments:
            cat: A Gr_category object

            weight: Int or Float (usually int), The percentage of the final grade that
            this category's grades get. Must be between 0 and 100.
            Note: if all the category weights in the gradebook sum up to over
            or less than 100, the weights must be edited in order to make the
            sum less than 100. Otherwise, a class average cannot be calculated.

        Will return an error if a category of the same name already exists
        in the cat dictionary.
        """
        try:
            assert is_num(weight)
            assert in_range(weight, 0, 100)
            name = cat.get_name()
            # if the name already exists, we're updating an existing category.
            # reuse the same weight.
            if weight == 0 and name in self.Cats:
                weight = self.Cats[name][2]
            self.Cats[name] = (cat, cat.get_avg(), weight)
            cat.parent = self
            self.weight_check()
            self.update_avg()
        except AssertionError:
            print("Gradebook.add_cat: invalid input.")

    def update_avg(self):
        """Updates the class average, based on the given category averages
        and weights. If the weight_check flag is set to false, notifies the
        user and sets the class average to None.

        For categories with no averages, an average of 100% is put as a placeholder
        to give students an accurate depiction of their current average.
        """
        total = 0
        if self.valid_weight is False:
            print("Current category weights do not add up to 100.")
            self.Class_avg = None
            return

        if self.Cats:
            for val in self.Cats.values():
                if val[1]:
                    total += ((val[1]/100)*val[2])
                else:
                    total += val[2]
        self.Class_avg = round(total, 2)

    def weight_check(self):
        """Checks that all of the weights add up to 100, and adjusts flag
        as necessary.
        """
        total = 0
        if self.Cats:
            for vals in self.Cats.values():
                total += vals[2]

        if total == 100:
            self.valid_weight = True
        else:
            self.valid_weight = False

    def project(self, Cat, assignment = None):
        """
        Given a category contained within the gradebook's category dictionary,
        projects the maximum and minimum class average after a future assignment is
        added to the category.
        Arguments:
            Cat - category that the projected assignment will fall under
            Assignment - parameter to allow for projection of a specific grade's impact on the class average.
        """
        try:
            name = Cat.get_name()
            assert name in self.Cats
            # get the weight of the category
            w = self.Cats[name][2]

            for i in (0, 100, assignment):
                if i is None:
                    continue
                Cat.add_grade('temp', i)
                self.add_cat(Cat, w)
                if i == 0:
                    print("Minimum possible new class average:" + str(self.Class_avg))
                elif i == 100:
                    print("Maximum possible new class average:" + str(self.Class_avg))
                else:
                    print("Average after an entry with grade " + str(i) + ":" + str(self.Class_avg))
                Cat.remove_grade('temp')
            self.add_cat(Cat, w)
        except AssertionError:
            print('Gradebook.project: Cat not in gradebook.')

            
# ------------------------------------------------------------------------------
# other functions
def is_num(test):
    """Returns True if given value is an int or float, false otherwise.
    
    Arguments:
        test: any value
    """
    if type(test) == int or type(test) == float:
        return True
    return False


def in_range(test, minimum, maximum):
    """
    Returns True if given test number is within the minimum and maximum range
    (inclusive). Returns False in all other cases, including invalid input. 
    User is alerted if input is invalid.
    Arguments:
        test: an int or float
        minimum: an int or float less than or equal to the maximum
        maximum: an int or float greater than or equal to the minimum
    """
    # check for bad input
    for i in (test, minimum, maximum):
        if not is_num(i):
            print ("in_range: parameter not a number")
            return False
    if maximum < minimum:
        print("in_range: min must be less than or equal to max.")
        return False
    
    if test <= maximum:
        if test >= minimum:
            return True
    return False

# example Gbook
gbook = Gradebook()
hw = GrCat('HW', parent=gbook, w=20)
quiz = GrCat('Quiz', parent=gbook, w=30)
test = GrCat('Test', parent=gbook, w=50)

for s in ("HW1", "HW2"):
    hw.add_grade(s, 100)
for s in ("Quiz 1", "Quiz 2"):
    quiz.add_grade(s, 100)
for s in ("Test 1", "Test 2"):
    test.add_grade(s, 100)


