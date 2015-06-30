#Put this in sitecustomize.py in Python27\
# import os
# import sys
## In the empty list, put the directory path where this is stored
# sys.path.append(os.sep.join([] + ["um_iis"]))

import SuperGLU.Util.ModuleRegistration
SuperGLU.Util.ModuleRegistration.importAllInDirectory(__file__)
