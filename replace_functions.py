import typing as t

import spacy
from spacy.tokens import Token
from pygermanet import load_germanet

from special_cases_de import \
    no_replacment, gendered_no_replacement, pre_replacements, noun_lemma_endings, \
    special_nouns, nominalized_adjectives, pronouns_no_replacement

# customize spacy Token slightly to have attribute vor replaced text
# Token.set_extension("value", default="")


# Artikel
def replace_article(article: spacy.tokens.Token, gender_token=":", manual_morph: t.Optional[str]=None):
    morph = article.morph
    text = article.text
    capital = False
    if text[0].isupper():
        capital = True
    manual_morph = manual_morph or ""
    if "Number=Plur" in morph:
        return None
    if "Definite=Def" in morph or "Definite=Def" in manual_morph:
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}{'d' if not capital else 'D'}er"
            elif "Gender=Masc" in morph:
                article._.value = f"{'d' if not capital else 'D'}ie{gender_token}" + text
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}{'d' if not capital else 'D'}es"
            elif "Gender=Masc" in morph:
                article._.value = f"{'d' if not capital else 'D'}er{gender_token}" + text
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}{'d' if not capital else 'D'}em"
            elif "Gender=Masc" in morph:
                article._.value = f"{'d' if not capital else 'D'}er{gender_token}" + text
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}{'d' if not capital else 'D'}en"
            elif "Gender=Masc" in morph:
                article._.value = f"{'d' if not capital else 'D'}ie{gender_token}" + text
    elif "Definite=Ind" in morph or "Definite=Ind" in manual_morph:
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                article._.value = text[:-1] + f"{gender_token}e"
            elif "Gender=Masc" in morph:
                article._.value = text + f"{gender_token}e"
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}s"
            elif "Gender=Masc" in morph:
                article._.value = text[:-1] + f"r{gender_token}s"
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}m"
            elif "Gender=Masc" in morph:
                article._.value = text[:-1] + f"r{gender_token}m"
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                article._.value = text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                article._.value = text[:-1] + f"{gender_token}n"

# weak declination if
# ["derselbe", "dieser", "jeder", "jener", "mancher", "welcher", "der", "die", "das", "alle", "sämtliche", "beide"
# mixed if ["ein", "kein", "mein", "dein", "sein"]
#
def get_declination_type(determiner: spacy.tokens.Token):
    # TODO do for other than Art:
    tag = determiner.tag_
    morph = determiner.morph
    if tag == "ART":
        if "Definite=Ind" in morph or determiner.lemma_ in {"kein"}:
            return "mixed"
        else:
            return "weak"
    elif determiner.lemma_.lower() in \
            {"derselbe", "dasselbe", "dieselbe","diese", "jene", "beid", "jed", "manch", "welch", "alle", "sämtliche"}:
        return "weak"
    else:
        return "strong"

# TODO: checke this special adjective endings:
# Adjektive auf -el, -er, -en
# Bei Adjektiven, die auf -el, -er oder -en enden, fällt, wenn sie mit einem vokalisch endenden Suffix kombiniert werden, zuweilen ein unbetontes e weg (e-Tilgung):[38]
# dunkel → ein dunkler Wald; illuster → eine illustre Gesellschaft; zerbrochen → ein zerbroch(e)ner Krug (Einzelheiten siehe im Artikel Kontraktion)
def replace_adjective(adjective: spacy.tokens.Token, declination_type: str, gender_token=":"):
    morph = adjective.morph
    text = adjective.text
    if adjective.lemma_.lower() in pronouns_no_replacement:
        return None
    if "Number=Plur" in morph:
        return None

    elif declination_type=="weak":
        if "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"{gender_token}n"

    elif declination_type=="strong":
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}r"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"{gender_token}r"
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"r{gender_token}n"
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}m"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"r{gender_token}m"
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"{gender_token}n"

    elif declination_type=="mixed":
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}r"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"{gender_token}r"
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = text[:-1] + f"{gender_token}n"

# S6: unveränderter Plural
def replace_type_1(noun: spacy.tokens.Token, ending: t.Iterable[str], gender_token=":"):
    ending_masc, ending_fem = ending
    morph = noun.morph
    text = noun.text
    if "Gender=Masc" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit(f"{ending_masc}", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit(f"{ending_masc}", 1))
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit(f"{ending_masc}s", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
    # female nouns in in erin
    elif "Gender=Fem" in morph:
        if "Number=Plur" in morph:
            if "Case=Dat" in morph:
                noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit("innen", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit("innnen", 1))
        else:
            if "Case=Gen" in morph:
                noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit("in", 1))
            else:
                noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))


gn = load_germanet()
def check_germa_net(lemma):
    # synset = gn.synsets(lemma)
    # if synset:
    #     return synset[0].gn_class == "Mensch"
    # else:
    #     return False
    return True


def replace_noun(noun: spacy.tokens.Token, gender_token=":"):
    # TODO: the order of checking the endings matter. How to overcome this?
    # TODO: e.g. 'ender' is thus transformed to 'ender:in', but it should be 'ende'
    # TODO: maybe order endings by length and make a loop to match, then use another dict that returns the replacement function for the given ending
    # TODO: maybe implement a class, that can do this?
    # check the ending
    # er
    # nouns in er / erin
    morph = noun.morph
    lemma = noun.lemma_
    text = noun.text
    # conditions for not changing nouns
    if lemma in gendered_no_replacement or lemma in no_replacment:
        return None
    for word in no_replacment:
        if lemma.endswith(word):  # or lemma.lower().endswith(word.lower()):
            return None
    if not check_germa_net(lemma):
        return None
    # special cases still to handle
    if text == "Wunderknabe":
        pass
    if lemma == "Virtuose":
        #breakpoint()

    if lemma in pre_replacements:
        noun._.value = pre_replacements[lemma]
        return True

    elif lemma in special_nouns:
        special_nouns[lemma](noun=noun, gender_token=gender_token)
        return True
    # TODO: use nominalized adjective endings
    elif lemma in nominalized_adjectives:
        #breakpoint()
        if noun.left_edge.pos_ == "DET":
            declination_type = get_declination_type(noun.left_edge)
            replace_adjective(adjective=noun, declination_type=declination_type, gender_token=gender_token)
            return True
    # TODO: get plural ending
    for endings, type in noun_lemma_endings.items():
        ending_masc, ending_fem = endings
        if type == 1 and lemma.endswith(f"{ending_masc}") or lemma.endswith(f"{ending_fem}"):
            # type 1 (er) - plural invariant
            #replace_type_1(noun=noun, ending=(ending_masc, ending_fem), gender_token=gender_token)
            if "Gender=Masc" in morph:
                if "Number=Plur" in morph:
                    if "Case=Dat" in morph:
                        noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit(f"{ending_masc}n", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit(f"{ending_masc}", 1))
                else:
                    if "Case=Gen" in morph:
                        noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit(f"{ending_masc}s", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
            # female nouns in in erin
            elif "Gender=Fem" in morph:
                if "Number=Plur" in morph:
                    if "Case=Dat" in morph:
                        noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit("innen", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit("innnen", 1))
                else:
                    if "Case=Gen" in morph:
                        noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit("in", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))
            return True
        elif type == 2 and lemma.endswith(f"{ending_masc}") or lemma.endswith(f"{ending_fem}"): # type 2 (tor,
            if "Gender=Masc" in morph:
                if "Number=Plur" in morph:
                    if "Case=Dat" in morph:
                        noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit(f"{ending_masc}", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit(f"{ending_masc}", 1))
                else:
                    if "Case=Gen" in morph:
                        noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit(f"{ending_masc}s", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
            # torin
            elif "Gender=Fem" in morph:
                if "Number=Plur" in morph:
                    if "Case=Dat" in morph:
                        noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit("in", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}innen".join(text.rsplit("in", 1))
                else:
                    if "Case=Gen" in morph:
                        noun._.value = f"{ending_masc}s{gender_token}in".join(text.rsplit("in", 1))
                    else:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))
            return True
        elif type == 3 and lemma.endswith(f"{ending_masc}") or lemma.endswith(f"{ending_fem}"): # type 2 (at, et,
            if "Gender=Masc" in morph:
                if "Number=Plur" in morph:
                    noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit(f"{ending_masc}en", 1))
                else:
                    if "Case=Nom" in morph:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
                    else:
                        noun._.value = f"{ending_masc}en{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
            # atin, etin
            elif "Gender=Fem" in morph:
                if "Number=Plur" in morph:
                    noun._.value = f"{ending_masc}en{gender_token}innen".join(text.rsplit("in", 1))
                else:
                    if "Case=Nom" in morph:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))
                    else:
                        noun._.value = f"{ending_masc}en{gender_token}in".join(text.rsplit("in", 1))
            return True
        elif type == 5 and lemma.endswith(f"{ending_masc}") or lemma.endswith(f"{ending_fem}"): # type 5 te
            if "Gender=Masc" in morph:
                if "Number=Plur" in morph:
                    noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit(f"{ending_masc}n", 1))
                else:
                    if "Case=Nom" in morph:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit(f"{ending_masc}", 1))
                    else:
                        noun._.value = f"{ending_masc}n{gender_token}in".join(text.rsplit(f"{ending_masc}n", 1))
            # tin
            elif "Gender=Fem" in morph:
                if "Number=Plur" in morph:
                    noun._.value = f"{ending_masc}n{gender_token}innen".join(text.rsplit("in", 1))
                else:
                    if "Case=Nom" in morph:
                        noun._.value = f"{ending_masc}{gender_token}in".join(text.rsplit("in", 1))
                    else:
                        noun._.value = f"{ending_masc}n{gender_token}in".join(text.rsplit("in", 1))
            return True
        # nouns in te / tin
        # elif lemma.endswith("te") or lemma.endswith("tin"):
        #     if "Gender=Masc" in morph:
        #         pass
        #     if "Gender=Fem" in morph:
        #         pass
        # # nouns in t / tin
        # if lemma.endswith("t") or lemma.endswith("tin"):
        #     if "Gender=Masc" in morph:
        #         pass
        #     if "Gender=Fem" in morph:
        #         pass
    return False


def replace_personal_pronoun(pronoun: spacy.tokens.Token, gender_token=":"):
    morph = pronoun.morph
    text = pronoun.text
    # just for safety, if some personal pronouns are matched
    if "Number=Plur" in morph:
        return None
    if "Case=Nom" in morph:
        if "Gender=Fem" in morph:
            if text[0].isupper():
                pronoun._.value = text + f"{gender_token}Er"
            else:
                pronoun._.value = text + f"{gender_token}er"
        elif "Gender=Masc" in morph:
            if text[0].isupper():
                pronoun._.value = f"Sie{gender_token}" + text
            else:
                pronoun._.value = f"sie{gender_token}" + text
    elif "Case=Gen" in morph:
        if "Gender=Fem" in morph:
            if text[0].isupper():
                pronoun._.value = text + f"{gender_token}Seiner"
            else:
                pronoun._.value = text + f"{gender_token}seiner"
        elif "Gender=Masc" in morph:
            if text[0].isupper():
                pronoun._.value = f"Ihrer{gender_token}" + text
            else:
                pronoun._.value = f"ihrer{gender_token}" + text
    elif "Case=Dat" in morph:
        if "Gender=Fem" in morph:
            pronoun._.value = text + f"{gender_token}m"
        elif "Gender=Masc" in morph:
            if text[0].isupper():
                pronoun._.value = f"Ihr{gender_token}m"
            else:
                pronoun._.value = f"ihr{gender_token}m"
    elif "Case=Acc" in morph:
        if "Gender=Fem" in morph:
            if text[0].isupper():
                pronoun._.value = text + f"{gender_token}Ihn"
            else:
                pronoun._.value = text + f"{gender_token}ihn"
        elif "Gender=Masc" in morph:
            if text[0].isupper():
                pronoun._.value = f"Sie{gender_token}" + text
            else:
                pronoun._.value = f"sie{gender_token}" + text


def replace_indefinite_pronouns(pronoun: spacy.tokens.Token, gender_token=":"):
    replace_adjective(adjective=pronoun, declination_type="strong", gender_token=gender_token)
