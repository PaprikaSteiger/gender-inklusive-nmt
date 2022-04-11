import typing as t

import spacy

gendered_no_replacement = [
    "Mann",
    "Herr",
    "Frau",
]
# tokens where gender inclusive shall not be used
no_replacment = [
    "Mutter",
    "Vater",
    "Computer",
    "Roboter",
    "Eimer", #And komposita
    "Fühler",
    "Körper",
    "Gottesanbeterin",
    "Völker", # shouldn't happen anyway as the lemma is volk
    "Fehler",
    "Hunger",
    "20er", #TODO: in general numbers+er
    "Zweiter",
    "Dritter", # ...
    "Leiter", # only if die Leiter
    "Butter",
    "Papier",
    "Scanner",
    "Fieber",
    "Gelächter",
    "Acker",
    #"Wikinger", TODO: ask an expert? For me it's referring to a population/culture not just the male ones
    #"Bürger", TODO: ask an expert?
    #"Boomer", TODO: ask an expert?
    #"Barde", TODO: ask an expert?
    "Meter",
    "Kilometer",
    "Wasser",
    "Muster",
    "Opfer",
    "Lager",
    "Charakter",
    "September",
    "Oktober",
    "November",
    "Dezember",
    "Sommer",
    "Winter",
    "Mauer",
    "Wasser",
    "Gletscher",
    "Wunder",
    "Fenster",
    "Gelder",
    "Gelächter",
    "Becher",
    "Manier",

    # - ending in
    "Medizin",
    "Benzin",

    # - ending ent
    "Moment",

    # - ending or
    "Traktor",


]

# important noun endings
noun_lemma_endings = {
    ("er", "in"): 1, # sg ers:in, just dative: ern:innen
    ("ent", "entin"): 3, # nom sg ent:in, sonst sg alles enten:in, plural enten:innen
    ("at", "atin"): 3, # wie ent
    ("te", "tin"): 3, # wie ent
    ("or", "orin"): 2, # just genitive ors:in, plural always en:innen
    ("eur", "euse"): 4, #Coiffeur
    ("eur","eurin"): 4,
    ("tekt", "tektin"): 3, # wie ent
    #("ender", "enderin"): 1, # wie (t)or
    #"se", "sin" # Virtuose, are there other words with ending e - in?
    # TODO: what to do with ein KriminelleR, but der KriminellE, it follows the strong, mixed, weak declination pattern
    # TODO: adjectives/pronouns used as noun follow adjective declination e.g. Kriminelle / Dritte vs. ein KriminellEr
    # TODO: for all adjectives used as noun, e.g. also ein ErwachseneR der Erwachsene
}


    # der freund die freundin
    # den freund die freundin
    # dem freund der freundin
    # des freundes der freundin
    #
    # die freunde die freundinnen
    # die freunde die freundinnen
    # den freunden den freundinnen
    # der freunde der freundinnen

def replace_freund(noun: spacy.tokens.Token, gender_token=":"):
    morph = noun.morph
    text = noun.text
    ending_masc = "nd"
    ending_fem = "in"
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit(f"{ending_masc}en", 1))
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(text.rsplit(f"{ending_masc}e", 1))
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit(f"{ending_masc}es", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit("innen", 1))
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(text.rsplit("innnen", 1))
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(text.rsplit("in", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))


special_nouns: t.Dict[str, t.Callable] = {
    "Freund": replace_freund,
    "Freundin": replace_freund,
    "Arzt": replace_freund, #Ärztin",
    "Frisör": replace_freund, #"Friseurin",
    "Chirurg": replace_freund, #"Chirurgin"
}


irregular_replacements = {
    "jedermann": "jeder", # shall be replaced bei jeder
    "Wunderknabe": "Wunderkind",

}