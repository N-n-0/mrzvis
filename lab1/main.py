#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#// Лабораторная работа №1 по дисциплине Модели решения задач в интеллектуальных системах
#// Выполнена студентами группы 121701 БГУИР Пашиным Никитой Александровичем, Селицким Богданом
#// Программа выполняет вычисление попарного произведения компонентов двух векторов чисел.
#// https://studfile.net/preview/8921792/page:5/
#// 21.04.2024

import re


class Data:
    def __init__(self, m, first_vector, second_vector):
        self.m = m
        self.first_vector = first_vector
        self.second_vector = second_vector
        self.partial_multiply, self.zero = [0,0,0,0], [0,0,0,0]
        self.current_step = 1
        self.index = -1
        self.first_multiplier, self.second_multiplier, self.result = [], [], []


def input_data(string, m):
    if is_correct_input(m, string, '10 '):
        values = [x for x in string.split(' ')]
        result = []
        for el in values:
            result.append(translate_to_array(el))
        return result
    else:
        raise ValueError("Некорректный ввод")


def translate_to_decimal(number):
    result = 0
    for i in range(len(number)-1, -1, -1):
        result += pow(2, len(number)-i-1) * number[i]
    return result


def translate_to_array(number):
    values = []
    for el in number:
        values.append(int(el))
    if len(values) < 4:
        while len(values) != 4:
            values.insert(0, 0)
    return values


def is_correct_input(m, string, allowed_chars):
    pattern = f'^[{re.escape(allowed_chars)}]+$'
    check = (re.match(pattern, string) is not None and check_space_and_length(m, string))
    return check


def check_space_and_length(m, string):
    for i, char in enumerate(string):
        if (i + 1) % 5 == 0 and char != ' ':
            return False
    return True and len(string) == m*4 + m-1


def multi(data):
    if data.index > -1:
        data.result.append(data.partial_multiply)
        print(f'Произведение: {data.partial_multiply} ({translate_to_decimal(data.partial_multiply)})\n')
    data.index += 1
    if data.index < data.m:
        data.current_step = 1
        data.partial_multiply, data.zero = [0,0,0,0], [0,0,0,0]
        data.first_multiplier = data.first_vector[data.index]
        data.second_multiplier = data.second_vector[data.index]
        print(f'Множимое: {data.first_multiplier} ({translate_to_decimal(data.first_multiplier)})\t'
              f'Множитель: {data.second_multiplier} ({translate_to_decimal(data.second_multiplier)})\n')
    else:
        print(f'Результирующий вектор: {data.result}')
    return data


def for_one(data):
    while len(data.partial_multiply) != len(data.first_multiplier):
        data.first_multiplier.append(0)
    print(f'Шаг {data.current_step}')
    temp = 0
    if data.second_multiplier[len(data.second_multiplier)-data.current_step] == 1:
        print(f'\nПервое слагаемое: {data.partial_multiply} ({translate_to_decimal(data.partial_multiply)})\t'
            f'Второе слагаемое: {data.first_multiplier} ({translate_to_decimal(data.first_multiplier)})')
        for i in range(len(data.partial_multiply) - 1, -1, -1):
            if data.partial_multiply[i] + data.first_multiplier[i] + temp <= 1:
                data.partial_multiply[i] = data.partial_multiply[i] + data.first_multiplier[i] + temp
                temp = 0
            else:
                data.partial_multiply[i] = (data.partial_multiply[i] + data.first_multiplier[i] + temp) % 2
                temp = 1
        data.partial_multiply.insert(0, temp)
    else:
        print(f'\nПервое слагаемое: {data.partial_multiply} ({translate_to_decimal(data.partial_multiply)})\t'
            f'Второе слагаемое: {data.zero} ({translate_to_decimal(data.zero)})')
        data.partial_multiply.insert(0, 0)
    data.zero.insert(0, 0)
    data.first_multiplier.append(0)
    print(f'Частичная сумма: {data.partial_multiply} ({translate_to_decimal(data.partial_multiply)})\n')
    data.current_step += 1
    return data


def pipeline(func_list):
    def decorator(func):
        def wrapper(input_data):
            result = input_data
            for process_func in func_list:
                result = process_func(result)
            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    m = int(input('m= '))
    #if m <3
    first_vector = input('Множимые числа: ')
    first_vector = input_data(first_vector, m)
    second_vector = input('Множители: ')
    second_vector = input_data(second_vector, m)
    print(first_vector, second_vector)
    data = Data(m, first_vector, second_vector)

    process_list = [multi if i % 5 == 0 else for_one for i in range(5*m+1)]

    @pipeline(process_list)
    def process_data(data):
        return data

    output_data = process_data(data)