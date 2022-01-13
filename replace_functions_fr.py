import typing as t

import spacy
from spacy.tokens import Token

# Article Definite et Indéfinite
def replace_article(article: spacy.tokens.Token, gender_token="・"):
  morph = article.morph
  text = article.text
  # Articles singular
  if "Number=Sing" in morph:
    if "Definite=Def" in morph:
      if "Gender=Masc" in morph:
        article._.value = f"la{gender_token}" + text
      elif "Gender=Fem" in morph:
        article._.value = text + f"{gender_token}le"
    else:
      if "Gender=Masc" in morph:
        article._.value = text + f"{gender_token}e"
      elif "Gender=Fem" in morph:
        article._.value = text[:-1] + f"{gender_token}e"

  # Articles plural
  if "Number=Plur" in morph:
    return None

# TODO: review adjctive suffix and think about the way to match mas-fem adjectives
# adding ou/olle and others adjective suffix
# same adjective suffix has different forms of mas/fem adjective suffix

# Adjective
def replace_adjective(adjective: spacy.tokens.Token, gender_token="・"):
  morph = adjective.morph
  text = adjective.text
  lemma = adjective.lemma_
  # eau/elle Adjective
  if lemma.endswith("eau") or lemma.endswith("elle"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"elle{gender_token}au".join(text.rsplit("eau",1))
      else:
        adjective._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("eau", 1))
    if "Gender=Fem" in morph: #lemmatization with the masculine form of -eau
      if "Number=Sing" in morph:
        adjective._.value = f"elle{gender_token}au".join(text.rsplit("elle",1))
      else:
        adjective._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("elle", 1))

  # el/elle Adjective
  if lemma.endswith("el") or lemma.endswith("elle"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"el{gender_token}le".join(text.rsplit("el", 1))
      else:
        adjective._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("el", 1))
    else: #lemmatization with the masculine form of -el
      if "Number=Sing" in morph:
        adjective._.value = f"el{gender_token}le".join(text.rsplit("elle", 1))
      else:
        adjective._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("elle", 1))
  
  # teur/trice and deur/drice Adjective
  if lemma.endswith("eur") or lemma.endswith("rice"): #lemmatization with the feminine form of -rice
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}rice".join(text.rsplit("eur", 1))
      else:
        adjective._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("eur", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}rice".join(text.rsplit("rice", 1))
      else:
        adjective._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("rice", 1))

  # eur/euse Adjective
  if lemma.endswith("eur") or lemma.endswith("euse"): #lemmatization with the feminine form of -euse
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}euse".join(text.rsplit("eur", 1))
      else:
        adjective._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("eur", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}euse".join(text.rsplit("euse", 1))
      else:
        adjective._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("euse", 1))

  # eur/eure Adjective
  if lemma.endswith("eur") or lemma.endswith("eure"): #lemmatization with the feminine form of -eure
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}e".join(text.rsplit("eur", 1))
      else:
        adjective._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eur", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eur{gender_token}e".join(text.rsplit("eure", 1))
      else:
        adjective._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eure", 1))
        
  # oux/ouse Adjective
  if lemma.endswith("oux") or lemma.endswith("ouse"): #lemmatization with the feminine form of -ouse
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}e".join(text.rsplit("oux", 1))
      else:
        adjective._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("oux", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}e".join(text.rsplit("ouse", 1))
      else:
        adjective._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("ouse", 1))

  # eux/euse Adjective
  if lemma.endswith("eux") or lemma.endswith("euse"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eux{gender_token}e".join(text.rsplit("eux", 1))
      else:
        adjective._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("eux", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"eux{gender_token}e".join(text.rsplit("euse", 1))
      else:
        adjective._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("euse", 1))

  # oux/ousse Adjective
  if lemma.endswith("oux") or lemma.endswith("ousse"): #lemmatization with the feminine form of -ousse
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}se".join(text.rsplit("oux", 1))
      else:
        adjective._.value = f"oux{gender_token}se{gender_token}s".join(text.rsplit("oux", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}se".join(text.rsplit("ousse", 1))
      else:
        adjective._.value = f"oux{gender_token}se{gender_token}s".join(text.rsplit("ousse", 1))

  # oux/ouce Adjective
  if lemma.endswith("oux") or lemma.endswith("ouce"): #lemmatization with the feminine form of -ouce
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}ce".join(text.rsplit("oux", 1))
      else:
        adjective._.value = f"oux{gender_token}ce{gender_token}s".join(text.rsplit("oux", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"oux{gender_token}ce".join(text.rsplit("ouse", 1))
      else:
        adjective._.value = f"oux{gender_token}ce{gender_token}s".join(text.rsplit("ouce", 1))

  # s/se Adjective
  if lemma.endswith("s") or lemma.endswith("se"): #lemmatization with the feminine form of -se
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"{gender_token}xe".join(text.rsplit("s", 1))
      else:
        adjective._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("s", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"{gender_token}xe".join(text.rsplit("se", 1))
      else:
        adjective._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("se", 1))  

  # tre/tresse Adjective
  if lemma.endswith("tre") or lemma.endswith("tresse"): #lemmatization with the feminine form of -tresse
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"tre{gender_token}xe".join(text.rsplit("tre", 1))
      else:
        adjective._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tre", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"tre{gender_token}xe".join(text.rsplit("tresse", 1))
      else:
        adjective._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tresse", 1))

  # en/enne Adjective
  if lemma.endswith("en") or lemma.endswith("enne"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"en{gender_token}ne".join(text.rsplit("en", 1))
      else:
        adjective._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("en", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"en{gender_token}ne".join(text.rsplit("enne", 1))
      else:
        adjective._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("enne", 1))

  # er/ère Adjective
  if lemma.endswith("er") or lemma.endswith("ère"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"er{gender_token}ère".join(text.rsplit("er", 1))
      else:
        adjective._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("er", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"er{gender_token}ère".join(text.rsplit("ère", 1))
      else:
        adjective._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("ère", 1))

  # t/te Adjective
  if lemma.endswith("t") or lemma.endswith("te"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"t{gender_token}e".join(text.rsplit("t", 1))
      else:
        adjective._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("t", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"t{gender_token}e".join(text.rsplit("te", 1))
      else:
        adjective._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("te", 1))  

  # d/de Adjective
  if lemma.endswith("d") or lemma.endswith("de"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"d{gender_token}e".join(text.rsplit("d", 1))
      else:
        adjective._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("d", 1))
    if "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"d{gender_token}e".join(text.rsplit("de", 1))
      else:
        adjective._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("de", 1))
  
  # on/onne Adjective
  if lemma.endswith("on") or lemma.endswith("onne"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"on{gender_token}ne".join(text.rsplit("on", 1))
      else:
        adjective._.value = f"on{gender_token}ne{gender_token}".join(text.rsplit("on", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"on{gender_token}ne".join(text.rsplit("onne", 1))
      else:
        adjective._.value = f"on{gender_token}ne{gender_token}s".join(text.rsplit("onne", 1))

  # u/ue Adjective
  if lemma.endswith("u") or lemma.endswith("ue"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"u{gender_token}e".join(text.rsplit("u", 1))
      else:
        adjective._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("u", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"u{gender_token}e".join(text.rsplit("ue", 1))
      else:
        adjective._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("ue", 1))

  # é/ée Adjective
  if lemma.endswith("é") or lemma.endswith("ée"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"é{gender_token}e".join(text.rsplit("é", 1))
      else:
        adjective._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("é", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"é{gender_token}e".join(text.rsplit("ée", 1))
      else:
        adjective._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("ée", 1))

  # i/ie Adjective
  if lemma.endswith("i") or lemma.endswith("ie"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"i{gender_token}e".join(text.rsplit("i", 1))
      else:
        adjective._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("i", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"i{gender_token}e".join(text.rsplit("ie", 1))
      else:
        adjective._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("ie", 1))

  # al/ale Adjective
  if lemma.endswith("al"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"al{gender_token}e".join(text.rsplit("al", 1))
  elif lemma.endswith("aux"):
    if "Gender=Masc" in morph:
      if "Number=Plur" in morph:
        adjective._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("aux", 1))  
  elif lemma.endswith("ale"):
    if "Gender=Fem"in morph:
      if "Number=Sing" in morph:
        adjective._.value = f"al{gender_token}e".join(text.rsplit("ale", 1))
      else:
        adjective._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("ale", 1))

  # ef/effe Adjective
  # tif/tive Adjective

# TODO: review adjctive suffix and think about the way to match mas-fem adjectives
# adding ou/olle and others adjective suffix
# same adjective suffix has different forms of mas/fem adjective suffix

# Noun