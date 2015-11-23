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
        self.figure_objects = {}
        self.islands = Islands()

    def initialize(self, problem: RavensProblem):
        self.figure_objects = {}
        print(problem.name)
        self.problem_name = problem.name
        folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
        for figure_name in self.figure_names:
            self.figure_pixel_matrix[figure_name] = self.open_image_return_pixels(Image.open('{}{}.png'.format(folder_name, figure_name)).convert('1'))
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

    def figure_pixel_matrix_black_xor(self, pixel_matrix_a, pixel_matrix_b):
        return_matrix = [[0 for i in range(len(pixel_matrix_a[0]))] for j in range(len(pixel_matrix_a))]
        for row, (a_row, b_row) in enumerate(zip(pixel_matrix_a, pixel_matrix_b)):
            for column, (a_row_column, b_row_column) in enumerate(zip(a_row, b_row)):
                if a_row_column != b_row_column:
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

    def parse_objects_in_figures(self):
        for figure_name in self.figure_names:
            self.figure_objects[figure_name] = self.islands.get_number_of_islands(self.figure_pixel_matrix[figure_name])
        return -1

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

    def method_and_two_to_get_third(self):
        best_answer = -1
        similarity_maximum = 0
        if self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_intersection(self.figure_pixel_matrix['A'], self.figure_pixel_matrix['B']), self.figure_pixel_matrix['C']) > 97 \
                and self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_intersection(self.figure_pixel_matrix['D'], self.figure_pixel_matrix['E']), self.figure_pixel_matrix['F']) > 97:
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    this_similarity = self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_intersection(self.figure_pixel_matrix['G'], self.figure_pixel_matrix['H']), self.figure_pixel_matrix[possible_answer])
                    if this_similarity > similarity_maximum:
                        best_answer = possible_answer
                        similarity_maximum = this_similarity
        return best_answer

    def method_xor_two_to_get_third(self):
        best_answer = -1
        similarity_maximum = 0
        if len(self.figure_objects['A']) + len(self.figure_objects['B']) == len(self.figure_objects['C']) and len(self.figure_objects['D']) + len(self.figure_objects['E']) == len(self.figure_objects['F']):
            return -1
        if self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_xor(self.figure_pixel_matrix['A'], self.figure_pixel_matrix['B']), self.figure_pixel_matrix['C']) > 97 \
                and self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_xor(self.figure_pixel_matrix['D'], self.figure_pixel_matrix['E']), self.figure_pixel_matrix['F']) > 97:
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    this_similarity = self.calculate_figure_pixel_similarity(self.figure_pixel_matrix_black_xor(self.figure_pixel_matrix['G'], self.figure_pixel_matrix['H']), self.figure_pixel_matrix[possible_answer])
                    if this_similarity > similarity_maximum:
                        best_answer = possible_answer
                        similarity_maximum = this_similarity
        return best_answer

    def method_change_of_area_to_get_third(self):
        best_answer = -1
        similarity_maximum = 0
        first_row = ['A', 'B', 'C']
        second_row = ['D', 'E', 'F']
        possible_combinations = self.permutations(first_row, second_row)
        similarity_of_combination = {}
        for combination in possible_combinations:
            area_difference = []
            correspondence = list(combination.items())
            area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[0][0]) - self.calculate_sum_of_area_in_figure(correspondence[1][0]),
                                                                 self.calculate_sum_of_area_in_figure(correspondence[0][1]) - self.calculate_sum_of_area_in_figure(correspondence[1][1])))
            area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[1][0]) - self.calculate_sum_of_area_in_figure(correspondence[2][0]),
                                                                 self.calculate_sum_of_area_in_figure(correspondence[1][1]) - self.calculate_sum_of_area_in_figure(correspondence[2][1])))
            area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[0][0]) - self.calculate_sum_of_area_in_figure(correspondence[2][0]),
                                                                 self.calculate_sum_of_area_in_figure(correspondence[0][1]) - self.calculate_sum_of_area_in_figure(correspondence[2][1])))
            similarity_of_combination[frozenset(combination.items())] = statistics.mean(area_difference)
        most_likely = min(similarity_of_combination.items(), key=lambda x: x[1])
        if most_likely[1] < 0.2:
            similarity_of_combination = {}
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                if ('A', 'D') in most_likely[0] and ('B', 'E') in most_likely[0] and ('C', 'F') in most_likely[0]:
                    combination = {'A': 'G', 'B': 'H', 'C': possible_answer}
                elif ('A', 'E') in most_likely[0] and ('B', 'F') in most_likely[0] and ('C', 'D') in most_likely[0]:
                    combination = {'A': possible_answer, 'B': 'G', 'C': 'H'}
                else:
                    return -1
                area_difference = []
                correspondence = list(combination.items())
                area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[0][0]) - self.calculate_sum_of_area_in_figure(correspondence[1][0]),
                                                                     self.calculate_sum_of_area_in_figure(correspondence[0][1]) - self.calculate_sum_of_area_in_figure(correspondence[1][1])))
                area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[1][0]) - self.calculate_sum_of_area_in_figure(correspondence[2][0]),
                                                                     self.calculate_sum_of_area_in_figure(correspondence[1][1]) - self.calculate_sum_of_area_in_figure(correspondence[2][1])))
                area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure(correspondence[0][0]) - self.calculate_sum_of_area_in_figure(correspondence[2][0]),
                                                                     self.calculate_sum_of_area_in_figure(correspondence[0][1]) - self.calculate_sum_of_area_in_figure(correspondence[2][1])))
                similarity_of_combination[possible_answer] = statistics.mean(area_difference)
            return min(similarity_of_combination.items(), key=lambda x: x[1])[0]
        return -1

    def method_simpler_change_of_area_to_get_third(self):
        area_difference = []
        area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('A') - self.calculate_sum_of_area_in_figure('B'), self.calculate_sum_of_area_in_figure('C')))
        area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('D') - self.calculate_sum_of_area_in_figure('E'), self.calculate_sum_of_area_in_figure('F')))
        similarity_of_answer = {}
        if statistics.mean(area_difference) < 0.1:
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                similarity_of_answer[possible_answer] = self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('G') - self.calculate_sum_of_area_in_figure('H'), self.calculate_sum_of_area_in_figure(possible_answer))
            if min(similarity_of_answer.items(), key=lambda x: x[1])[1] < 0.1:
                return min(similarity_of_answer.items(), key=lambda x: x[1])[0]
        return -1

    def similarity_of_two_number(self, number_1, number_2):
        number_1 = abs(number_1)
        number_2 = abs(number_2)
        return abs(number_1 - number_2) / ((number_1 + number_2) / 2)

    def calculate_sum_of_area_in_figure(self, figure_name):
        sum_of_area = 0
        for index, figure_object in self.figure_objects[figure_name].items():
            sum_of_area += figure_object['area']
        return sum_of_area

    def method_special_case_in_change_of_area(self):
        best_answer = -1
        if self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('A') - self.calculate_sum_of_area_in_figure('E'),
                                         self.calculate_sum_of_area_in_figure('F') - self.calculate_sum_of_area_in_figure('G')) < 0.15:
            similarity_of_combination = {}
            for possible_answer in ['1', '2', '3', '4', '5', '6', '7', '8']:
                area_difference = []
                area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('E') - self.calculate_sum_of_area_in_figure(possible_answer),
                                                                     self.calculate_sum_of_area_in_figure('G') - self.calculate_sum_of_area_in_figure('B')))
                area_difference.append(self.similarity_of_two_number(self.calculate_sum_of_area_in_figure('A') - self.calculate_sum_of_area_in_figure(possible_answer),
                                                                     self.calculate_sum_of_area_in_figure('F') - self.calculate_sum_of_area_in_figure('B')))
                similarity_of_combination[possible_answer] = statistics.mean(area_difference)
            filtered_similarity_of_combination = {k: v for (k, v) in similarity_of_combination.items() if v < 0.1}
            if len(filtered_similarity_of_combination) != 0:
                if len(self.figure_objects['A']) == len(self.figure_objects['E']):
                    similar_number_of_objects_filtered_of_combination = {k: v for (k, v) in filtered_similarity_of_combination.items() if len(self.figure_objects[k]) == len(self.figure_objects['E'])}
                    if len(similar_number_of_objects_filtered_of_combination) == 1:
                        key, value = similar_number_of_objects_filtered_of_combination.popitem()
                        best_answer = key
        return best_answer

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        self.initialize(problem)
        for possible_method in [self.method_unchanged, self.parse_objects_in_figures, self.method_xor_two_to_get_third, self.method_and_two_to_get_third, self.method_merge_two_to_get_third, self.method_simple_iterate, self.method_merge_row, self.method_change_of_area_to_get_third, self.method_simpler_change_of_area_to_get_third, self.method_special_case_in_change_of_area]:
            possible_answer = possible_method()
            if possible_answer != -1:
                print(possible_method.__name__)
                return possible_answer
        return -1

    def permutations(self, former_objects, later_objects):
        return [dict(zip(a, later_objects)) for a in itertools.permutations(former_objects, len(later_objects))] if \
            len(former_objects) > len(later_objects) else \
            [dict(zip(former_objects, b)) for b in itertools.permutations(later_objects, len(former_objects))]
