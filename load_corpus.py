"""
Loading the datasets locally
"""
from pathlib import Path
import tarfile
import requests

#TODO clean this file, actual data used found here:
#ted 2020: https://opus.nlpl.eu/TED2020.php
#ted 2013: https://opus.nlpl.eu/TED2013.php
#europarl: MISSING

DIR: Path = (Path(__file__).parent / "data").mkdir(exist_ok=True) or Path(__file__).parent / "data"


def write_dataset_to_file(dirname: str, url: str):
    response = requests.get(url, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=dirname)


if __name__ == "__main__":
    # write_dataset_to_file(dirname=DIR, url=r"https://www.statmt.org/europarl/v7/de-en.tgz")
    # write_dataset_to_file(dirname=DIR, url=r"https://www.statmt.org/europarl/v7/fr-en.tgz")
    pass


