from collections import Counter
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import csv

from load_corpus import DIR

TOKENIZED = DIR / "tokenized_normalized_truecased.de"


def count_words(in_file: Path):
    c = Counter()
    with open(in_file, "r", encoding="utf8") as inn:
        for line in inn:
            line = line.split(" ")
            c.update(line)
    return c


def histogram_of_frequencies(data: list):
    array = np.array(data)
    bins = len(set(array))
    sn.histplot(array, stat="count", bins=bins, )
    plt.show()

# use https://github.com/rsennrich/ParZu for parsing
# write small bash script

if __name__ == "__main__":
    counter = count_words(in_file=(DIR / "tokenized_normalized_truecased.de"))
    histogram_of_frequencies(data=list(counter.values()))
    # write counts to file
    with (DIR / "word_count.csv").open("w", encoding="utf8", newline="") as out:
        dict_writer = csv.writer(out)
        for k, v in counter.items():
            dict_writer.writerow([k, v])
    # show n least frequent words
    n = 100
    for ele in counter.most_common()[:n-1:-1]:
        print(ele)