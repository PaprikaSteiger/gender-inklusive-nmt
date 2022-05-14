import typing as t

import spacy

# special words
pronouns_no_replacement = {
    "jemand",
    "irgendjemand",
    "niemand",
    "alle",
    "manche",
    "beide",
    "viele",
    "eine",
    "einige",
    "einig",
}

# all words in ende/ender
nominalized_adjectives: t.List[str] = [
    "Dritte",
    "Dritter",
    "Zweiter",
    "Zweite",
    "Krimineller",
    "Kriminelle",
    "Kranker",
    "Kranke",
    "Meditierende",
    "Meditierender",
]

pre_replacements = {
    "jedermanns": "jedes",
    "Jedermanns": "Jedes",
    "jedermann": "jeder",
    "Jedermann": "Jeder",
    "Wunderknabe": "Wunderkind",
}
special_cases = [
    "kein",  # mixed declination, not weak one
]

gendered_no_replacement = [
    "Mann",
    "Herr",
    "Frau",
    "Mutter",
    "Vater",
    "Tochter",
    "Sohn",
    "Bruder",
    "Schwester",
    "Dame",
]
# tokens where gender inclusive shall not be used
no_replacment = [
    "Mutter",
    "Vater",
    "Tochter",
    "Sohn",
    "Bruder",
    "Schwester",
    "Computer",
    "Roboter",
    "Eimer",  # And komposita
    "Fühler",
    "Körper",
    "Gottesanbeterin",
    "Völker",  # shouldn't happen anyway as the lemma is volk
    "Fehler",
    "Hunger",
    "20er",  # TODO: in general numbers+er
    "30er",
    "40er",
    "50er",
    "60er",
    "70er",
    "80er",
    "90er",
    # "Leiter", # only if die Leiter
    "Butter",
    "Papier",
    "Scanner",
    "Fieber",
    "Gelächter",
    "Acker",
    # "Wikinger", TODO: ask an expert? For me it's referring to a population/culture not just the male ones
    # "Bürger", TODO: ask an expert?
    # "Boomer", TODO: ask an expert?
    # "Barde", TODO: ask an expert?
    "Meter",
    "Quadratmeter",
    "Kubikmeter",
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
    "Gründer",
    # - ending in
    "Medizin",
    "Benzin",
    # - ending ent
    "Moment",
    # - ending or
    "Traktor",
    # - ending te
    "Milchprodukte",
    "Minute",
    "Geschichte",
    # - ending at
    "Staat",
    "Plakat",
    "Monat",
]

# important noun endings
noun_lemma_endings = {
    ("er", "in"): 1,  # sg ers:in, just dative: ern:innen
    ("ent", "entin"): 3,  # nom sg ent:in, sonst sg alles enten:in, plural enten:innen
    ("at", "atin"): 3,  # wie ent
    ("experte", "expertin"): 5,  # wie ent, endung einfach nur n nicht en
    ("or", "orin"): 2,  # just genitive ors:in, plural always en:innen
    ("eur", "euse"): 4,  # Coiffeur
    ("eur", "eurin"): 4,
    ("tekt", "tektin"): 3,  # wie ent
    # ("ender", "enderin"): 1, # wie (t)or
    # "se", "sin" # Virtuose, are there other words with ending e - in?
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
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}en", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}e", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit(f"{ending_masc}es", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit(f"{ending_masc}", 1)
                )
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit("innen", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit("innnen", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit("in", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit("in", 1)
                )


# ein Dritter, eine Dritte
# einen Dritten, eine Dritte
def replace_arzt(noun: spacy.tokens.Token, gender_token=":"):
    morph = noun.morph
    text = noun.text
    ending_masc = "zt"
    ending_fem = "in"
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}en", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}e", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit(f"{ending_masc}es", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit(f"{ending_masc}", 1)
                )
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit("innen", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit("innnen", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit("in", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit("in", 1)
                )


def replace_frisör(noun: spacy.tokens.Token, gender_token=":"):
    morph = noun.morph
    text = noun.text
    ending_masc = "ör"
    ending_fem = "in"
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}en", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit(f"{ending_masc}e", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit(f"{ending_masc}es", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit(f"{ending_masc}", 1)
                )
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}en{gender_token}innen".join(
                    text.rsplit("innen", 1)
                )
            else:
                noun._.value = f"{ending_masc}e{gender_token}innen".join(
                    text.rsplit("innnen", 1)
                )
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}es{gender_token}in".join(
                    text.rsplit("in", 1)
                )
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit("in", 1)
                )


def replace_chirurg(noun: spacy.tokens.Token, gender_token=":"):
    morph = noun.morph
    text = noun.text
    ending_masc = "urg"
    ending_fem = "in"
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            noun._.value = f"{ending_masc}en{gender_token}innen".join(
                text.rsplit(f"{ending_masc}en", 1)
            )
        else:
            if "Case=Nom" in morph:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit(f"{ending_masc}", 1)
                )
            else:
                noun._.value = f"{ending_masc}en{gender_token}in".join(
                    text.rsplit(f"{ending_masc}en", 1)
                )
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            noun._.value = f"{ending_masc}en{gender_token}innen".join(
                text.rsplit("innen", 1)
            )
        else:
            if "Case=Nom" in morph:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit("in", 1)
                )
            else:
                noun._.value = f"{ending_masc}en{gender_token}in".join(
                    text.rsplit("in", 1)
                )


def replace_virtuose(noun: spacy.tokens.Token, gender_token=":"):
    morph = noun.morph
    text = noun.text
    ending_masc = "se"
    ending_fem = "in"
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            noun._.value = f"{ending_masc}n{gender_token}innen".join(
                text.rsplit(f"{ending_masc}n", 1)
            )
        else:
            if "Case=Nom" in morph:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit(f"{ending_masc}", 1)
                )
            else:
                noun._.value = f"{ending_masc}en{gender_token}in".join(
                    text.rsplit(f"{ending_masc}n", 1)
                )
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            noun._.value = f"{ending_masc}n{gender_token}innen".join(
                text.rsplit("innen", 1)
            )
        else:
            if "Case=Nom" in morph:
                noun._.value = f"{ending_masc}{gender_token}in".join(
                    text.rsplit("in", 1)
                )
            else:
                noun._.value = f"{ending_masc}n{gender_token}in".join(
                    text.rsplit("in", 1)
                )


special_nouns: t.Dict[str, t.Callable] = {
    "Freund": replace_freund,
    "Freundin": replace_freund,
    "Arzt": replace_arzt,
    "Ärztin": replace_arzt,
    "Frisör": replace_frisör,
    "Friseurin": replace_frisör,
    "Chirurg": replace_chirurg,
    "Chirurgin": replace_chirurg,
    "Virtuose": replace_virtuose,
    "Virtuosin": replace_virtuose,
}
