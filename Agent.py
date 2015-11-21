from PIL import Image
import itertools
import collections
from RavensProblem import RavensProblem
from RavensFigure import RavensFigure
from RavensObject import RavensObject
import pprint
import os


# noinspection PyMethodMayBeStatic
class Agent:
    def __init__(self):
        self.log_file = None

    def initialize(self, problem: RavensProblem):
        print(problem.name)
        folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
        image = Image.open('{}{}.png'.format(folder_name, problem.name)).convert('1')
        pixels = list(image.getdata())
        width, height = image.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        pass

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        self.initialize(problem)
        return -1

