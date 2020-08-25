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
    Given a .gb file, returns a list with 2 elements. Element 1 is the
    Gradebook attribute data, in the form of a list
    containing data attributes. Element 2 is a list containing strings of 
    Cat data. Element 2 will be of length n, where n is the number of cats.
    :param gbfile - string containing path to .gb file
    :returns list containing gradebook and cat data
    """
    f = open(gbfile)
    text = f.read()
    data = text.split("****")
    gb_data = data[0]
    if len(data) > 1:
        cat_data = data[1:]
        for i, cat in enumerate(cat_data):
            cat_data[i] = cat.split('\n')
            while cat_data[i][-1] == '':
                cat_data[i].pop()
            while cat_data[i][0] == '':
                cat_data[i].pop(0)
    gb_data = data[0].split('\n')
    while gb_data[-1] == '':
        gb_data.pop()
    
    if len(data) > 1:
        return [gb_data, cat_data]
    else: #no cats in the file
        return [gb_data, []] 

def initGB(gb_data) -> Gradebook:
    """
    Given a string containing gb attribute data (section 1 of the .gb file),
    initialize a Gradebook object with the given data.
    :param gbfile: string containing section 1 of .gb file
    :returns Gradebook object
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


print(dataSplit('example.gb'))