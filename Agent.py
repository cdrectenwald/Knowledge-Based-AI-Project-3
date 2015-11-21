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
        self.figure_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '1', '2', '3', '4', '5', '6', '7', '8']
        self.figure_pixel_matrix = {}
        self.figure_similarity = {}

    def initialize(self, problem: RavensProblem):
        print(problem.name)
        folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
        for figure_name in self.figure_names:
            self.figure_pixel_matrix[figure_name] = self.open_image_return_pixels(Image.open('{}{}.png'.format(folder_name, figure_name)).convert('1'))
        for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H'], ['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6']]:
            self.figure_similarity[combination[0]+combination[1]] = self.calculate_image_pixel_similarity(self.figure_pixel_matrix[combination[0]], self.figure_pixel_matrix[combination[1]])

    def calculate_image_pixel_similarity(self, pixel_matrix_a, pixel_matrix_b):
        intersection = 0
        union = 0
        for a_row, b_row in zip(pixel_matrix_a, pixel_matrix_b):
            for a_row_column, b_row_column in zip(a_row, b_row):
                if (a_row_column | b_row_column) != 0:
                    union += 1
                if a_row_column == b_row_column and a_row_column != 0:
                    intersection += 1
        return intersection / union * 100

    def open_image_return_pixels(self, image: Image.Image):
        pixels = list(image.getdata())
        width, height = image.size
        return [pixels[i * width:(i + 1) * width] for i in range(height)]

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        self.initialize(problem)
        return -1

