# This module contains the methods for reading from a .gb file.
from Gradebook import *
from GrCat import *
def loadGB(gbfile: str) -> Gradebook:
    """
    Given a string containing the path to a .gb file, loads Gradebook data from the file.
    :param gbfile: string containing path to .gb file
    :return Gradebook object with all data from the .gb file
    """
    data = dataSplit(gbfile)
    gb_data = data[0]
    cat_data = data[1]
    gb = initGB(gb_data)
    if cat_data:
        initAllCats(cat_data, gb)
    return gb


def dataSplit(gbfile:str) -> list:
    """
    Given a .gb file, returns a list with two elements. Element 0 is the string containing
    the Gradebook attributes (section 1 of the .gb file). Element 1 is a list of strings containing individual
    cat data (section 2 of the .gb file).
    :param gbfile - string containing path to .gb file
    :returns list containing gradebook and cat data
    """
    # TODO


def initGB(gb_data) -> Gradebook:
    """
    Given a string containing gb attribute data (section 1 of the .gb file),
    initialize a Gradebook object with the given data.
    :param gbfile: string containing section 1 of .gb file
    :returns Gradbeook object
    """
    # TODO


def initcat(catdata:str, gb:Gradebook):
    """
    Given a Gradebook object and data from a .gb file containing cat information, initialize a cat and add it to the
    Gradebook.
    :param catdata: string from .gb file containing data for a cat
    :param gb: Gradebook object to add the cat to
    :modifies gb
    :returns None
    """
    # TODO

def initAllCats(cat_data:list, gb:Gradebook):
    """
    Given a Gradebook object and a list containing strings of cat data,
    creates cat data and adds it to the given gb.

    :param cat_data: list of strings. Each strings corresponds to data for a particular cat
    :param gb: Gradebook object to add cats to
    :modifies gb
    :returns None
    """
    # TODO