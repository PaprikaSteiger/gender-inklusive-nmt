"""
Loading the Europarl Corpus en-de and en-fr from huggingface
"""
from pathlib import Path

from datasets import load_dataset

def load_europarl_en_de():
    return load_dataset("europarl_bilingual", lang1="en", lang2="de")

def load_europarl_en_fr():
    return load_dataset("europarl_bilingual", lang1="en", lang2="fr")