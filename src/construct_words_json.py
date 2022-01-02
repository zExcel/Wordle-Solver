import os, json

def insert_into_dict(my_dict: dict, word: str):
    length = len(word)
    if length in my_dict:
        if word.lower() not in my_dict[length]:
            my_dict[length].append(word)
    else:
        my_dict[length] = [word.lower()]


def construct_json_file(file_name: str = '../resources/all_words.txt'):
    words_by_count = {}
    file = open(file_name)
    lines = file.read().splitlines()
    result = list(map(lambda word: insert_into_dict(words_by_count, word), lines))
    file.close()

    output = open(file_name.replace('.txt', '.json'), 'w')
    json.dump(words_by_count, output)
    output.close()


def construct_popular_json():
    construct_json_file('../resources/popular_words.txt')


def get_dict_from_file(file_name: str = '../resources/all_words.json'):
    file = open(file_name, 'r')
    result = json.load(file)
    file.close()
    return result

def get_dict_from_all_file():
    return get_dict_from_file()

def get_dict_from_popular_file():
    return get_dict_from_file('../resources/popular_words.json')