# -*- coding: utf-8 -*-
import os
import sys
import pkgutil
import importlib

def getFileDir(filesrc):
    """Get the directory of the given file spec
    @param filesrc A file path (possibly relative)
    @return Absolute path of the directory containing the file
    """
    return os.path.dirname(os.path.abspath(filesrc))

def getBasePath():
    """
    Get the base path for the project root
    @return: Base path
    @rtype: str
    """
    try:
        #return os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
        this_dir = getFileDir(__file__)
        return os.sep.join( this_dir.split(os.sep)[:-1] )
    except NameError:
        return ""

def getShortestString(strings, default=None):
    """
    Gets the shortest string out of a list
    @param strings: A collection of strings
    @type strings: list of str
    @param default: A default value to use if strings is empty
    @type default: str or None
    @return: The shortest string in the list, or the default
    @rtype: str
    """
    if len(strings) == 0:
        return default
    else:
        return min(strings, key=len)

def findCanonicalPackage(dirName, resolver=getShortestString):
    """
    Finds a canonical package name for the given directory,
    based on the paths that are loaded
    @param dirName: A directory name to find a canonical package name for
    @type dirName: str
    @param resolver: Function to use if multiple paths are valid, in form f(paths, default)
    @type resolver: callable
    @return: Canonical module name in form Package.SubPackage
    @rtype: str
    """
    validPaths = [path for path in sys.path if dirName.find(path) == 0]
    canonicalPath = resolver(validPaths, "")
    modName = dirName[len(canonicalPath)+1:]
    modName = modName.replace(os.sep, ".")
    return modName

