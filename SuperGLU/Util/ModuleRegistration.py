# -*- coding: utf-8 -*-
import importlib
import os
import pkgutil
import sys
import SuperGLU.Util.ErrorHandling
UTIL_PACKAGE_NAME = "SuperGLU.Util"

PENDING_IMPORTS = []

def importAllInDirectory(fileName):
    """
    Import everything in the same directory as the given file
    """
    import SuperGLU.Util.Paths
    dirName = os.path.dirname(fileName)
    moduleName = SuperGLU.Util.Paths.findCanonicalPackage(dirName)
    return importAllInPackage(moduleName, fileName)

def importAllInPackage(packageName=UTIL_PACKAGE_NAME, fileName=None):
    """
    Automatic Module Discovery in Current Directory
    The Util package is special because it needs to be able
    to specifically plant the Util name, to prevent
    any circular refs.
    """
    global PENDING_IMPORTS
    if fileName is None:
        fileName = __file__
    dirName = os.path.dirname(fileName)
    packages = ['.'.join(packageName.split('.') + [mod])
                  for imp, mod, isPackage in pkgutil.iter_modules([dirName])
                 if ' ' not in mod and isPackage]
    modules = ['.'.join(packageName.split('.') + [mod])
                  for imp, mod, isPackage in pkgutil.iter_modules([dirName])
                 if ' ' not in mod and not isPackage]
    packages.sort(key=lambda x: x.count('.'))
    modules.sort(key=lambda x: x.count('.'))
    libraries = packages + modules
    for library in libraries:
        try:
            #print " "*(len(PENDING_IMPORTS)*3), "IMPORTING: ", library
            if library not in sys.modules and library not in PENDING_IMPORTS:
                PENDING_IMPORTS.append(library)
                importlib.import_module(library)
                PENDING_IMPORTS.remove(library)
        except ImportError as err:
            #Util.ErrorHandling.errorHandler(sys.exc_info(), 1)
            pass
    return libraries
