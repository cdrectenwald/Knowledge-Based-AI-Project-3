from PIL import Image
import itertools
import collections
from RavensProblem import RavensProblem
from RavensFigure import RavensFigure
from RavensObject import RavensObject
import pprint
import os
import functools


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
        for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H'], ['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8']]:
            self.figure_similarity[combination[0]+combination[1]] = self.calculate_figure_pixel_similarity(self.figure_pixel_matrix[combination[0]], self.figure_pixel_matrix[combination[1]])
        pass

    def calculate_figure_pixel_similarity(self, pixel_matrix_a, pixel_matrix_b):
        intersection = functools.reduce(lambda x, y: x+y, self.figure_pixel_matrix_intersection(pixel_matrix_a, pixel_matrix_b)).count(255)
        union = functools.reduce(lambda x, y: x+y, self.figure_pixel_matrix_union(pixel_matrix_a, pixel_matrix_b)).count(255)
        return intersection / union * 100

    def figure_pixel_matrix_union(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if (a_row_column | b_row_column) != 0:
                    return_matrix[row][column] = 255
                else:
                    return_matrix[row][column] = 0
        return return_matrix

    def figure_pixel_matrix_intersection(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if a_row_column == b_row_column and a_row_column != 0:
                    return_matrix[row][column] = 255
                else:
                    return_matrix[row][column] = 0
        return return_matrix

    def open_image_return_pixels(self, image: Image.Image):
        pixels = list(image.getdata())
        width, height = image.size
        return [pixels[i * width:(i + 1) * width] for i in range(height)]

    def unchanged(self):
        unchanged_flag = 1
        for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H']]:
            if self.figure_similarity[combination[0]+combination[1]] < 95:
                unchanged_flag = 0
        best_answer = -1
        similarity_maximum = 0
        if unchanged_flag == 1:
            for combination in [['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8']]:
                if self.figure_similarity[combination[0]+combination[1]] > similarity_maximum:
                    best_answer = combination[1]
                    similarity_maximum = self.figure_similarity[combination[0]+combination[1]]
        return best_answer

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        self.initialize(problem)
        possible_answer = self.unchanged()
        if possible_answer != -1:
            return possible_answer
        return -1

