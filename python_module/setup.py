from setuptools import setup, find_packages
# Note: Manifest.in not really used for anything (possibly being deprecated)
setup(
  name = 'SuperGLU',
  packages = find_packages(),
  version = '0.1.7',
  description = 'Base Generalized Learning Utilities (GLU) library for communicating data between different learning technologies and intelligent systems.',
  author = 'Benjamin D. Nye',
  author_email = 'benjamin.nye@gmail.com',
  url = 'https://github.com/GeneralizedLearningUtilities/SuperGLU',
  download_url = 'https://github.com/GeneralizedLearningUtilities/SuperGLU/archive/0.1.tar.gz',
  include_package_data = True,
  exclude_package_data = {'': ['.gitignore', '.travis.yml', 'requirements.txt']},
  keywords = ['ITS', "Adaptive Learning", 'Messaging', 'HTML5', "Websockets", "Service"],
  classifiers = [          
		  "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
		  "Programming Language :: JavaScript",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Science/Research"],
   setup_requires = [ "setuptools_git >= 0.3", ]
)