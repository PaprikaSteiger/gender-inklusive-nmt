from pathlib import Path
import numpy as np
import typing as t
from collections import Counter
import re
from math import floor
from preprocess_corpus import CORPUS_NOISE, DIR

def select_sentences(n: int, file: str):
    clean_lines = []
    with open(file, "r", encoding="utf8") as inn:
        for line in inn:
            # don't add sentences with noise to test set
            if any(line.startswith(ele) or ele in line for ele in CORPUS_NOISE):
                continue
            # block sentences with less than or two tokens
            if len(line.split(" ")) <= 3:
                continue
            clean_lines.append(line)
    length = len(clean_lines)
    # generate n random intengers in range (0, length)
    # TODO: assert no integer appears twice
    # TODO: or replace dupplicated sentences afterwards
    indices = np.random.randint(0, length, n)
    indices_set = set(indices)
    while not len(indices_set) == len(indices):
        breakpoint()
        new_int = np.random.randint(0, length)
        if new_int not in indices_set:
            indices_set.add(new_int)

    for i in indices_set:
        yield clean_lines[i]

def create_validation_set(train_data: str,
                          train_out: str,
                          val_out: str):
    split = 0.1
    split_index = floor(len(train_data) * split)
    train = train_data[:split_index]
    validation = train_data[split_index:]
    lines = open(train_data, "r", encoding="utf8").readlines()
    length = len(lines)
    # generate n random integers in range (0, length)
    n = floor(length * split)
    indices = np.random.randint(0, length, n)
    indices_set = set(indices)
    while not len(indices_set) == len(indices):
        new_int = np.random.randint(0, length)
        if new_int not in indices_set:
            indices_set.add(new_int)
    with open(train_out, "w", encoding="utf8") as train:
        for i, line in enumerate(lines, start=0):
            if i in indices_set:
                continue
            else:
                train.write(line)
    with open(val_out, "w", encoding="utf8") as val:
        for i in indices_set:
            val.write(lines[i])
    return train, validation

if __name__ == "__main__":
    create_validation_set(
        train_data=str(DIR/"fr_train.txt"),
        train_out=str(DIR/"train.fr"),
        val_out=str(DIR/"validation.fr"))






