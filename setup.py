from setuptools import setup
setup(
  name = 'SuperGLU',
  packages = ['SuperGLU'],
  version = '0.1.4',
  description = 'Base Generalized Learning Utilities (GLU) library for communicating data between different learning technologies and intelligent systems.',
  author = 'Benjamin D. Nye',
  author_email = 'benjamin.nye@gmail.com',
  url = 'https://github.com/GeneralizedLearningUtilities/SuperGLU',
  download_url = 'https://github.com/GeneralizedLearningUtilities/SuperGLU/archive/0.1.tar.gz',
  include_package_data = True,
  keywords = ['ITS', "Adaptive Learning", 'Messaging', 'HTML5', "Websockets", "Service"],
  classifiers = [          
		  "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
		  "Programming Language :: JavaScript",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Science/Research"],
)