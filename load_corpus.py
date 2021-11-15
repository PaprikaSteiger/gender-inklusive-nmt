"""
Loading the Europarl Corpus en-de and en-fr from huggingface
"""
from pathlib import Path
import requests
import tarfile

DIR: Path = (Path(__file__).parent / "data").mkdir(exist_ok=True) or Path(__file__).parent / "data"


# TODO: Seemingly, the hugging face interface throws an error
# europarl-mono at https://huggingface.co/datasets/mulcyber/europarl-mono/blob/main/europarl-mono.py
# def load_europarl_en_de():
#     dataset = load_dataset("mulcyber/europarl-mono", "europarl-de")
#     return dataset
# # TODO: Seemingly, the hugging face interface throws an error
# def load_europarl_en_fr():
#     dataset = load_dataset("europarl_bilingual", lang1="en", lang2="fr")
#     return dataset


def write_dataset_to_file(dirname: str, url: str):
    response = requests.get(url, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=dirname)

# we could also use the single language corpus
# it contains more data
# but we'd have to construct it ourselves given all the source files...
#     response = requests.get(r"https://www.statmt.org/europarl/v7/europarl.tgz", stream=True)
#     file = tarfile.open(fileobj=response.raw, mode="r|gz")
#     for member in file.getmembers():
        # just select files from required language


if __name__ == "__main__":
    write_dataset_to_file(dirname=DIR, url=r"https://www.statmt.org/europarl/v7/de-en.tgz")
    write_dataset_to_file(dirname=DIR, url=r"https://www.statmt.org/europarl/v7/fr-en.tgz")
    for file in DIR.iterdir():
        if str(file).endswith(".en"):
            file.unlink()


