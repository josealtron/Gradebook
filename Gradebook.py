# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:29:24 2019

@author: josea
Gradebook for Students Project
"""
# Objects for Grade Categories


from GrCat import *

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
        Returns a copy of the category dictionary.
        """
        return self.Cats.copy()

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


