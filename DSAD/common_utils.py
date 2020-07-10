import json
import datetime
from os import path, makedirs


def get_abs_path(*paths):
    return path.abspath(path.join(*paths))


def get_data_dir(file_name):
    return get_abs_path(__file__, "../"+file_name)

def get_output_dir():
    return get_abs_path(__file__, "../")

def get_content_from_file(file_path):
    with open(file_path, 'r') as file:
        newlines = []
        for line in file.readlines():
            newlines.append(line)
        return newlines
