from PIL import Image
import itertools
import collections
from RavensProblem import RavensProblem
from RavensFigure import RavensFigure
from RavensObject import RavensObject
import pprint
import os
from NumberOfIslands import Islands
import functools
import statistics


# noinspection PyMethodMayBeStatic
class Agent:
    def __init__(self):
        self.problem_name = None
        self.log_file = None
        self.figure_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', '1', '2', '3', '4', '5', '6', '7', '8']
        self.figure_pixel_matrix = {}
        self.figure_similarity = {}
        self.figure_number_of_objects = {}
        self.islands = Islands()

    def initialize(self, problem: RavensProblem):
        print(problem.name)
        self.problem_name = problem.name
        folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
        for figure_name in self.figure_names:
            self.figure_pixel_matrix[figure_name] = self.open_image_return_pixels(Image.open('{}{}.png'.format(folder_name, figure_name)).convert('1'))
            self.figure_number_of_objects[figure_name] = self.islands.get_number_of_islands(self.figure_pixel_matrix[figure_name])
        for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H'], ['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8']]:
            self.figure_similarity[combination[0] + combination[1]] = self.calculate_figure_pixel_similarity(self.figure_pixel_matrix[combination[0]], self.figure_pixel_matrix[combination[1]])
        # print(self.figure_number_of_objects)

    def calculate_figure_pixel_similarity(self, pixel_matrix_a, pixel_matrix_b):
        intersection = functools.reduce(lambda x, y: x + y, self.figure_pixel_matrix_white_intersection(pixel_matrix_a, pixel_matrix_b)).count(255)
        union = functools.reduce(lambda x, y: x + y, self.figure_pixel_matrix_white_union(pixel_matrix_a, pixel_matrix_b)).count(255)
        return intersection / union * 100

    def figure_pixel_matrix_white_union(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if (a_row_column | b_row_column) != 0:
                    return_matrix[row][column] = 255
                else:
                    return_matrix[row][column] = 0
        return return_matrix

    def figure_pixel_matrix_black_union(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if a_row_column == 0 or b_row_column == 0:
                    return_matrix[row][column] = 0
                else:
                    return_matrix[row][column] = 255
        return return_matrix

    def figure_pixel_matrix_black_intersection(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if a_row_column == 0 and b_row_column == 0:
                    return_matrix[row][column] = 0
                else:
                    return_matrix[row][column] = 255
        return return_matrix

    def figure_pixel_matrix_white_intersection(self, pixel_matrix_a, pixel_matrix_b):
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

    def method_unchanged(self):
        flag = 1
        best_answer = -1
        similarity_maximum = 0
        for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H']]:
            if self.figure_similarity[combination[0] + combination[1]] < 95:
                flag = 0
        if flag == 1:
            for combination in [['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8']]:
                this_similarity = self.figure_similarity[combination[0] + combination[1]]
                if this_similarity > similarity_maximum:
                    best_answer = combination[1]
                    similarity_maximum = this_similarity
        return best_answer

    def method_merge_row(self):
        best_answer = -1
        similarity_maximum = 0
        if self.calculate_figure_pixel_similarity(
                self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix['A'], self.figure_pixel_matrix['B']), self.figure_pixel_matrix['C']),
                self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix['D'], self.figure_pixel_matrix['E']), self.figure_pixel_matrix['F'])) > 95:
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                this_similarity = self.calculate_figure_pixel_similarity(
                    self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix['A'], self.figure_pixel_matrix['B']), self.figure_pixel_matrix['C']),
                    self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix_white_intersection(self.figure_pixel_matrix['G'], self.figure_pixel_matrix['H']), self.figure_pixel_matrix[possible_answer]))
                if this_similarity > similarity_maximum:
                    best_answer = possible_answer
                    similarity_maximum = this_similarity
        return best_answer

    def method_simple_iterate(self):
        possible_combinations = self.permutations(['A', 'B', 'C'], ['D', 'E', 'F'])
        flag = 0
        best_answer = -1
        similarity_maximum = 0
        for combination in possible_combinations:
            overall_similarity = []
            for key, value in combination.items():
                overall_similarity.append(self.calculate_figure_pixel_similarity(self.figure_pixel_matrix[key], self.figure_pixel_matrix[value]))
            if statistics.mean(overall_similarity) > 95:
                flag = 1
        if flag == 1:
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                possible_combinations = self.permutations(['A', 'B', 'C'], ['G', 'H', possible_answer])
                for combination in possible_combinations:
                    overall_similarity = []
                    for key, value in combination.items():
                        overall_similarity.append(self.calculate_figure_pixel_similarity(self.figure_pixel_matrix[key], self.figure_pixel_matrix[value]))
                    if statistics.mean(overall_similarity) > similarity_maximum and statistics.mean(overall_similarity) > 95:
                        best_answer = possible_answer
                        similarity_maximum = statistics.mean(overall_similarity)
        return best_answer

    def method_merge_two_to_get_third(self):
        best_answer = -1
        similarity_maximum = 0
        possible_combinations = list(itertools.permutations('012', 3))
        imitation = ['A', 'B', 'C']
        for combination in possible_combinations:
            if self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_union(self.figure_pixel_matrix[imitation[int(combination[0])]], self.figure_pixel_matrix[imitation[int(combination[1])]]), self.figure_pixel_matrix[imitation[int(combination[2])]]) > 95:
                for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    reproduce = ['G', 'H', possible_answer]
                    this_similarity = self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_union(self.figure_pixel_matrix[reproduce[int(combination[0])]], self.figure_pixel_matrix[reproduce[int(combination[1])]]), self.figure_pixel_matrix[reproduce[int(combination[2])]])
                    if this_similarity > similarity_maximum:
                        best_answer = possible_answer
                        similarity_maximum = this_similarity
        return best_answer

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        self.initialize(problem)
        for possible_method in [self.method_unchanged, self.method_merge_two_to_get_third, self.method_simple_iterate, self.method_merge_row]:
            possible_answer = possible_method()
            if possible_answer != -1:
                print(possible_method.__name__)
                return possible_answer
        return -1

    def permutations(self, former_objects, later_objects):
        return [dict(zip(a, later_objects)) for a in itertools.permutations(former_objects, len(later_objects))] if \
            len(former_objects) > len(later_objects) else \
            [dict(zip(former_objects, b)) for b in itertools.permutations(later_objects, len(former_objects))]