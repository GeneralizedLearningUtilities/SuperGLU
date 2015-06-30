# -*- coding: utf-8 -*-
import SuperGLU.Util.ModuleRegistration

# Check if file name is available
try:
    __file__
    fileDefined = True
except NameError:
    fileDefined = False

# Populate canonical file-named __all__ first, then duplicate
if fileDefined:
    __all__ = SuperGLU.Util.ModuleRegistration.importAllInPackage("SuperGLU.Util", __file__)
else:
    __all__ = SuperGLU.Util.__all__
    
# Cleanup
del fileDefined
