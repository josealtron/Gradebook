from Gradebook import *

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
            print('GrCat __init__: invalid input')

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
        Returns a copy of the grade dictionary.
        """
        return self.grades.copy()
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
