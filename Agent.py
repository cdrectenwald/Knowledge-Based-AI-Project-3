from PIL import Image
import itertools
import collections
from RavensProblem import RavensProblem
from RavensFigure import RavensFigure
from RavensObject import RavensObject
import pprint
import os


class Agent:
    def __init__(self):
        self.log_file = None

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        print(problem.name)
        return -1
