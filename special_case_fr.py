import typing as t
import spacy

# general noun suffix
noun_lemma_endings = [
    "eau", "el", "elle",
    "teur", "trice", "teuse",
    "deur", "drice", #"deuse",
    "eur", "euse", "eure",
    "oux", "ouse", "ousse", "ouce",
    "eux", "euse",
    "s", "se", #"sse",
    "tre", "tresse",
    "en", "enne",
    "ien", "ienne",
    "er", "ère",
    "ier", "ière",
    "nt", "nte",
    "nd", "nde",
    "t", "te",
    "on", "onne",
    "u", "ue",
    "é", "ée",
    "i", "ie",
    "al", "ale",
    "ef", "effe",
    "tif", "tive"
    #"iste",
    #"in", "ine",
    #"e", "esse"
]

# personal nouns that should not be change
noun_no_replacement = [
    "Monsieur", "M.", "roi",
    "Madame", "Mme", "dame", "reine",
    "héro", "gars", "type", "mec",
    "homme", "femme", "mari", "mâle", "femelle",
    "fils","fille","garçon", "bébé", "enfant", "adulte",
    "grand-père", "grand-mère", "père", "mère", "papa", "maman",
    "parrain", "marraine", "soeur", "frère", "filleul", "filleule",
    "oncle", "tante", "neveu", "nièce",
    "personne", "individu", "humain", "gens", "monde", "peuple", "ancêtre",
    "moine", "moniale"
]

# identical feminine and masculine personal nouns that should not be change
noun_same_no_replacement = [
    "artiste",
    "bénévole",
    "capitaine",
    "diplomate",
    "fonctionnaire",
    "gendarme",
    "guide",
    "interprète",
    "juriste",
    "maire",
    "membre",
    "propriétaire",
    "scientifique",
    "secrétaire"
]

# general adj suffix
adj_lemma_endings = [
    "eau", "el", "elle",
    "teur", "trice", "teuse",
    "deur", "drice",  #"deuse",
    "eur", "euse", "eure",
    "oux", "ouse", "ousse", "ouce",
    "eux", "euse",
    "s", "se", #"sse",
    "tre", "tresse",
    "en", "enne",
    "ien", "ienne",
    "er", "ère",
    "ier", "ière",
    "nt", "nte",
    "nd", "nde",
    "t", "te",
    "on", "onne",
    "u", "ue",
    "é", "ée",
    "i", "ie",
    "al", "ale",
    "ef", "effe",
    "tif", "tive"
    #"iste",
    # "in", "ine",
    # "e", "esse",
    # #"ai", "aie",
    #"il", "elle",
    #"ul", "ulle"
    #"et", "ette", "ète",
    #"gu", "güe",
    #"ou", "olle",
    #"f", "ve",
    #"g", "gue"
]