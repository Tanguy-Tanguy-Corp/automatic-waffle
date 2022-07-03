from fileinput import filename
from os import listdir
import csv
import re


def getAvailLangs(dirPath='./static/dictionaries/'):
    """
    Return all implemented languages
    """
    dictFileNames = listdir(dirPath)
    langs = []
    for name in dictFileNames:
        for pos, letter in enumerate(name):
            if letter.isupper():
                firstCapIndex = pos
                break
        langs.append(name[:firstCapIndex])
    return langs


def get_path(lang, dirPath):
    """
    Return the path of the file in directory for the requested language
    """
    filenames = listdir(dirPath)
    for name in filenames:
        if name[:len(lang)] == lang:
            return(dirPath + name)

def createDictionary(lang='fr', dirPath='./static/dictionaries/'):
    """
    Create and return the dictionary in the requested language
        Parameters:
            lang (string): identifier for chosen language
            dirPath (string): path of the directory where dictionaries are stored
        Returns:
            words (list): the list of words contained into the dictionary
    """
    with open(get_path(lang, dirPath)) as dictTxt:
        lines = dictTxt.readlines()
        words = [line[:-1] for line in lines]

    return words



def word_with_n_chars(n, lang='fr'):
    """
    Return all words of n characters in the required dictionnary
    """
    word_dict = createDictionary(lang)
    return [word for word in word_dict if len(word) == n]


def word_with_n_chars_with_regex(n, lang='fr'):
    regex = '\n\w{n}\n'
    return []


def createDistribution(lang='fr', format='list', dirPath='./static/letterDistributions/'):
    """
    Create and return the letter distribution in the requested language
        Parameters:
            lang (string): identifier for chosen language
            format (0 or 1): 0 is for list format, 1 is for dict format
            dirPath (string): path of the directory where letter distributions are stored
        Returns:
            distribution (list|dict)
                format='list' : a list representing the letter distribution [letter, count, value]
                format='dict' : a dict representing the letter distribution {letter: {value: value, count: count}}
    """
    with open(get_path(lang, dirPath)) as distCsv:
        csvReader = csv.reader(distCsv)
        header = next(csvReader)
        if format == 'list':
            distribution = [[row[0].strip(), int(row[2].strip()), int(
                row[1].strip())] for row in csvReader]
        elif format == 'dict':
            distribution = {row[0].strip(): {header[1].strip(): int(row[1].strip()),
                                             header[2].strip(): int(row[2].strip())} for row in csvReader}
        else:
            raise ValueError('2 formats are available: list or dict')

    return distribution
