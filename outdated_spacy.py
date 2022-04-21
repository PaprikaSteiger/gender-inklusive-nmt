# ------ outdated ----

def on_match_ar_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    article = entities.pop(0)
    noun = entities.pop(-1)
    # TODO decide given the noun whether to replace anything or not -> or is this a job for the replace noun function?
    # Check endings of lemma
    # check the noun if something has to be replaced
    # if noun.lemma_ in gendered_no_replacement:
    #     return
    # # todo: move this part to the replace noun function, so I might check the noun of a match if it was change and decide based on that if the rest has to be changed or not
    # if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
    #     return None
    # no adjective or adverb
    if len(entities) == 0:
        if replace_noun(noun=noun, gender_token=gender_token):
            replace_article(article=article, gender_token=gender_token)
    else:
        # adverbs are invariant in German, so just replace the adjectives
        # also ignore cunjunctions and punctuation
        adjectives = [t for t in entities if t.tag_ == "ADJA"]

        if replace_noun(noun=noun, gender_token=gender_token):
            declination_type = get_declination_type(determiner=article)
            replace_article(article=article, gender_token=gender_token)
            for adjective in adjectives:
                replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)

def on_match_ip_dp_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = ":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    pronoun = entities.pop(0)
    noun = entities.pop(0)
    #breakpoint()
    # the pronoun follows (as it is used attributively without determiner) the strong declination of an adjective
    # only transform pronoun if transformation applied to noun
    if replace_noun(noun=noun, gender_token=gender_token):
        if pronoun.lemma_ == "kein":
            # kein identical with indefinite article
            replace_article(article=pronoun, gender_token=gender_token, manual_morph="Definite=Ind")
        else:
            replace_adjective(adjective=pronoun, declination_type="strong", gender_token=gender_token)


def on_match_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # first token is the not-determiner
    entities.pop(0)
    noun = entities.pop(-1)
    # check how many adjectives
    # if there is no determiner, its always going to be a strong declination
    declination_type = "strong"
    if len(entities) == 1:
        adjective = entities[0]
        if replace_noun(noun=noun, gender_token=gender_token):
            replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)
    else:
        # adverbs are invariant in German, so just replace the adjectives
        adjectives = [t for t in entities if t.tag_ == "ADJA"]
        if replace_noun(noun=noun, gender_token=gender_token):
            for adjective in adjectives:
                replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)

def on_match_pp_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # first token is possessive determiner
    pos = entities.pop(0)
    noun = entities.pop(-1)
    #print(entities)
    # check how many words are left and if adjective
    if replace_noun(noun=noun, gender_token=gender_token):
        # replace possessive determiner
        replace_adjective(adjective=pos, declination_type="strong", gender_token=gender_token)
        adjectives = [t for t in entities if t.tag_ == "ADJA"]
        for adjective in adjectives:
            replace_adjective(adjective=adjective, declination_type="weak", gender_token=gender_token)


    # noun phrase without determiner modified by adjectives
    # just adjective and noun not preceded by article
    # e.g. in a case where it is preceded by und we might have to check whether we transformed something before
    # TODO: this also matches noun preceded by nothing, do we want that?
    # TODO. probably not, a sentences starting with a noun that needs to be replaced wouldn't be matched. So probably as a last step just check for single nouns
    # e.g. von Lehrer:in zu Schüler:in
    ad_nn = [
        {"POS": {"NOT_IN": ["DET"]}},
        {"POS": {"IN": ["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "+"},  # with + single nouns are not matched
        {"LEMMA": {"IN": ["und", "sowie"]}, "OP": "*"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]

    # noun phrase with attributive indefinite or demonstrative pronoun
    ip_dp_nn = [
        {"TAG": "ART", "OP": "?"},
        {"TAG": {"IN": ["PDAT", "PIAT"]}},
        {"POS": "NOUN"},
    ]

    # noun phrase with attributive possessive pronoun and possible adjectives
    pp_ad_nn = [
        {"TAG": "PPOSAT"},
        # {"POS": {"IN": ["ADV"]}, "OP": "*"},
        # {"TAG": "ADJA", "OP": "*"},
        # {"LEMMA": {"IN": ["und", "sowie"]}, "OP": "?"},
        # {"IS_PUNCT": True, "OP": "?"},
        # {"POS": {"IN": ["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]

    # isolated noun not preceded by any determiner or pronoun
    nn_isolated = [
        {"POS": "NOUN"}
    ]
    # personal pronoun, no entity in sentence, no object, not referring to a noun not describing a person
    pp = [
        {"TAG": "PPER", "MORPH": {"INTERSECTS": ["Number=Sing", "Gender=Masc", "Gender=Fem"]}}
    ]
