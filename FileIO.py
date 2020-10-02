import os
import numpy as np
from numpy import genfromtxt


def getFileExtension(fileName):
    return os.path.splitext(fileName)[1]


def getFileNameWithoutExtension(fileName):
    return os.path.splitext(fileName)[0]


def openFile(filePath, skipHeader=1):
    """
    ***MAKE HEADER WIDGET***
    Given a filepath, this function will traverse the file and return
    an x-coordinate array amd w y-coordinate array.

    :param filePath: a path to a supported csv or txt file
    :return: 2 Coordinate data arrays
    """
    inputArray = genfromtxt(filePath, delimiter=',', skip_header=skipHeader)
    return inputArray[:, 0], inputArray[:, 1]
