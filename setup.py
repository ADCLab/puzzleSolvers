import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "puzzleSolvers",
    version = "0.0.1",
    author = "Adan E Vela",
    author_email = "adan.vela@ucf.edu",
    description = ("Simple module to optimize ordering of moving puzzle pieces using TSP"),
    license = "Apache License 2.0",
    keywords = "optimize puzzle solving",
    url = "https://github.com/ADCLab/puzzleSolver",
    packages=['puzzleSolver', 'testing'],
    install_requires=['collections', 'scipy', 'numpy','python_tsp'], #external packages as dependencies
    long_description=read('README.md'),
)
