import typing as t
import spacy
from spacy.tokens import Token
from special_case_fr import pronoun_no_replacement,noun_lemma_endings, noun_no_replacement, noun_same_no_replacement, adj_lemma_endings

# Pronoun
def replace_pron(pron: spacy.tokens.Token, gender_token="·"):
  morph = pron.morph
  text = pron.text
  # Pron personnels
  if "Person=3" in morph: # il & elle
    if "Number=Sing" in morph:
      if "Gender=Masc" in morph:
        if text[0].isupper():
          pron._.value = text[:-1] + f"{gender_token}El"
        else:
          pron._.value = text[:-1] + f"{gender_token}el"
      elif "Gender=Fem" in morph:
        if text[0].isupper():
          pron._.value = f"I{gender_token}" + text[:-2]
        else:
          pron._.value = f"i{gender_token}" + text[:-2]
    elif "Number=Plur" in morph: # ils & elles
      if "Gender=Masc" in morph:
        if text[0].isupper():
          pron._.value = text[:-2] + f"{gender_token}El{gender_token}s"
        else:
          pron._.value = text[:-2] + f"{gender_token}el{gender_token}s"
      elif "Gender=Fem" in morph:
        if text[0].isupper():
          pron._.value = f"I{gender_token}" + text[:-3] + f"{gender_token}s"
        else:
          pron._.value = f"i{gender_token}" + text[:-3]+ f"{gender_token}s"

  # Pron compléments
  if "PronType=Prs" in morph: # lui & elle
    if "Number=Sing" in morph:
      if "Gender=Masc" in morph:
        pron._.value = f"ell{gender_token}" + text[1:]
      elif "Gender=Fem" in morph:
        pron._.value = text[:-1] + f"{gender_token}ui"
    elif "Number=Plur" in morph: # eux & elles
      if "Gender=Masc" in morph:
        pron._.value = f"ell{gender_token}" + text
      elif "Gender=Fem" in morph:
        pron._.value = text[:-3] + f"{gender_token}eux"

  # Pronoms démonstratifs
  if "PronType=Dem" in morph:
    if "Number=Sing" in morph: # celui & celle
      if "Gender=Masc" in morph:
        if text[0].isupper():
          pron._.value = text + f"{gender_token}Elle"
        else:
          pron._.value = text + f"{gender_token}elle"
      elif "Gender=Fem" in morph:
        if text[0].isupper():
          pron._.value = f"Celui{gender_token}" + text[1:]
        else:
          pron._.value = f"celui{gender_token}" + text[1:]
    elif "Number=Plur" in morph: # ceux & celles
      if "Gender=Masc" in morph:
        if text[0].isupper():
          pron._.value = text + f"{gender_token}Elles"
        else:
          pron._.value = text + f"{gender_token}elles"
      elif "Gender=Fem" in morph:
        if text[0].isupper():
          pron._.value = f"Ceux{gender_token}" + text[1:]
        else:
          pron._.value = f"ceux{gender_token}" + text[1:]

# Article Definite et Indéfinite
def replace_det(det: spacy.tokens.Token, gender_token="·"):
  morph = det.morph
  text = det.text
  lemma = det.lemma_
  # Articles définis & indéfinis
  if "PronType=Art" in morph:
    if "Number=Sing" in morph:
      if "Definite=Def" in morph:
        if lemma.endswith("le"): # le & la
          if "Gender=Masc" in morph:
            if text[0].isupper():
              det._.value = text.replace("Le", f"La{gender_token}le")
            else:
              det._.value = f"la{gender_token}" + text
          elif "Gender=Fem" in morph:
              det._.value = text + f"{gender_token}le"
        #elif lemma.endswith("de"): # du & de la
         # if "Gender=Masc" in morph:
          #  det._.value = f"de li".join(text.rsplit("du", 1))
          #else:
           # return None
        #elif lemma.endswith("au"): # au & à la
         # if "Gender=Masc" in morph:
          #  det._.value = f"à li".join(text.rsplit("au", 1))
      elif "Definite=Ind" in morph:
        if lemma.endswith("un"): # un & une
          if "Gender=Masc" in morph:
            det._.value = text + f"{gender_token}e"
          elif "Gender=Fem" in morph:
            det._.value = text[:-1] + f"{gender_token}e"
    elif "Number=Plur" in morph:
      return None

  # Déterminants démonstratifs
  if "PronType=Dem" in morph:
    if "Number=Sing" in morph:
      if lemma.endswith("ce"): # ce
        if "Gender=Masc" in morph:
          if text.endswith("t"): # cet
            det._.value = text[:-1] + f"{gender_token}tte"
          else:
            det._.value = text + f"{gender_token}tte"
        elif "Gender=Fem" in morph: # cette
          det._.value = text.replace("cette", f"ce{gender_token}tte")
    elif "Number=Plur" in morph:
      return None

  # Déterminants possessifs
  if "Poss=Yes" in morph:
    if "Number=Sing" in morph:
      if lemma.endswith("on"): # mon/ma; ton/ta; son;sa
        if "Gender=Fem" in morph:
          det._.value = text + f"{gender_token}on"
        else:
          det._.value = f"a{gender_token}on".join(text.rsplit("on", 1))
    elif "Number=Plur" in morph:
      return None

  # Déterminants indéfinis
  #if lemma.endswith("aucun"):
    #if "Number=Sing" in morph: # aucun & aucune
      #if "Gender=Masc" in morph:
        #det._.value = text + f"{gender_token}e"
      #elif "Gender=Fem" in morph:
        #det._.value = text[:-1] + f"{gender_token}e"
    #elif "Number=Plur" in morph: # aucuns & aucunes
      #if "Gender=Masc" in morph:
        #det._.value = text + f"{gender_token}e{gender_token}s"
      #elif "Gender=Fem" in morph:
        #det._.value = text[:-1] + f"{gender_token}e{gender_token}s"

# Noun
def replace_noun(noun: spacy.tokens.Token, gender_token="·"):
  morph = noun.morph
  text = noun.text
  lemma = noun.lemma_
  # noun lemma list
  if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
    return None

  # no replacement
  if lemma in noun_no_replacement:
    return None

  # identical nouns no replacement
  if lemma in noun_same_no_replacement:
    return None

  # eau/elle Noun
  if lemma.endswith("eau"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"elle{gender_token}au".join(text.rsplit("eau", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("eaux", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("eau") or text.endswith("eaux"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"elle{gender_token}au".join(text.rsplit("elle", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("elles", 1))

  # el/elle Noun
  if lemma.endswith("el"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"el{gender_token}le".join(text.rsplit("el", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("els", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("el") or text.endswith("els"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"el{gender_token}le".join(text.rsplit("elle", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("elles", 1))

  # eur/rice;euse;eure Noun
  if lemma.endswith("eur"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"eur{gender_token}rice".join(text.rsplit("rice", 1))
        noun._.value = f"eur{gender_token}euse".join(text.rsplit("euse", 1))
        noun._.value = f"eur{gender_token}e".join(text.rsplit("eure", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("rices", 1))
        noun._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("euses", 1))
        noun._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eures", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("eur") or text.endswith("eurs"):
        noun._.value = text
      elif text.endswith("rice") or text.endswith("rices"):  # teur/trice and deur/drice Noun
        if "Number=Sing" in morph:
          noun._.value = f"eur{gender_token}rice".join(text.rsplit("rice", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("rices", 1))
      elif text.endswith("euse") or text.endswith("euses"):  # eur/euse Noun
        if "Number=Sing" in morph:
          noun._.value = f"eur{gender_token}euse".join(text.rsplit("euse", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("euses", 1))
      elif text.endswith("eure") or text.endswith("eures"):  # eur/eure Noun
        if "Number=Sing" in morph:
          noun._.value = f"eur{gender_token}e".join(text.rsplit("eure", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eures", 1))

  # oux/ouse;ousse;ouce Noun
  if lemma.endswith("oux"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"oux{gender_token}e".join(text.rsplit("oux", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("oux", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("oux"):
        noun._.value = text
      elif text.endswith("ouse"):
        if "Number=Sing" in morph:
          noun._.value = f"oux{gender_token}e".join(text.rsplit("ouse", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("ouses", 1))
      elif text.endswith("ousse"):
        if "Number=Sing" in morph:
          noun._.value = f"oux{gender_token}se".join(text.rsplit("ousse", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"oux{gender_token}se{gender_token}s".join(text.rsplit("ousses", 1))
      elif text.endswith("ouce"):
        if "Number=Sing" in morph:
          noun._.value = f"oux{gender_token}ce".join(text.rsplit("ouce", 1))
        elif "Number=Plur" in morph:
          noun._.value = f"oux{gender_token}ce{gender_token}s".join(text.rsplit("ouces", 1))

  # eux/euse Noun
  if lemma.endswith("eux"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"eux{gender_token}e".join(text.rsplit("eux", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("eux", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("eux"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"eux{gender_token}e".join(text.rsplit("euse", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("euses", 1))

  # s/se Noun
  if lemma.endswith("s"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"{gender_token}xe".join(text.rsplit("s", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("s", 1))
    if "Gender=Fem" in morph:
      if text.endswith("s"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"{gender_token}xe".join(text.rsplit("se", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("ses", 1))

  # tre/tresse Noun
  if lemma.endswith("tre"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"tre{gender_token}xe".join(text.rsplit("tre", 1))
      elif "Number=Plur":
        noun._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tres", 1))
    if "Gender=Fem" in morph:
      if text.endswith("tre") or text.endswith("tres"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"tre{gender_token}xe".join(text.rsplit("tresse", 1))
      elif "Number=Plur":
        noun._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tresses", 1))

  # en/enne and ien/ienne Noun
  if lemma.endswith("en"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"en{gender_token}ne".join(text.rsplit("en", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("ens", 1))
    if "Gender=Fem" in morph:
      if text.endswith("en") or text.endswith("ens"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"en{gender_token}ne".join(text.rsplit("enne", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("ennes", 1))

  # er/ère and ier/ière Noun
  if lemma.endswith("er"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"er{gender_token}ère".join(text.rsplit("er", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("ers", 1))
    if "Gender=Fem" in morph:
      if text.endswith("er") or text.endswith("ers"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"er{gender_token}ère".join(text.rsplit("ère", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("ères", 1))

  # nt/nte and t/te Noun
  if lemma.endswith("t"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"t{gender_token}e".join(text.rsplit("t", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("ts", 1))
    if "Gender=Fem" in morph:
      if text.endswith("t") or text.endswith("ts"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"t{gender_token}e".join(text.rsplit("te", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("tes", 1))

  # nd/nde Noun
  if lemma.endswith("nd"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"d{gender_token}e".join(text.rsplit("nd", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("nds", 1))
    if "Gender=Fem" in morph:
      if text.endswith("nd") or text.endswith("nds"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"d{gender_token}e".join(text.rsplit("nde", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("ndes", 1))

  # on/onne Noun
  if lemma.endswith("on"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"on{gender_token}ne".join(text.rsplit("on", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"on{gender_token}ne{gender_token}".join(text.rsplit("ons", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("on") or text.endswith("ons"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"on{gender_token}ne".join(text.rsplit("onne", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"on{gender_token}ne{gender_token}s".join(text.rsplit("onnes", 1))

  # u/ue Noun
  if lemma.endswith("u"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"u{gender_token}e".join(text.rsplit("u", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("us", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("u") or text.endswith("us"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"u{gender_token}e".join(text.rsplit("ue", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("ues", 1))

  # é/ée Noun
  if lemma.endswith("é"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"é{gender_token}e".join(text.rsplit("é", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("és", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("é") or text.endswith("és"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"é{gender_token}e".join(text.rsplit("ée", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("ées", 1))

  # i/ie Noun
  if lemma.endswith("i"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"i{gender_token}e".join(text.rsplit("i", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("is", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("i") or text.endswith("is"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"i{gender_token}e".join(text.rsplit("ie", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("ies", 1))

  # al/ale Noun
  if lemma.endswith("al"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"al{gender_token}e".join(text.rsplit("al", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("aux", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("al") or text.endswith("aux"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"al{gender_token}e".join(text.rsplit("ale", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("ales", 1))

  # ef/effe Noun
  if lemma.endswith("ef"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"ef{gender_token}fe".join(text.rsplit("ef", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"ef{gender_token}fe{gender_token}s".join(text.rsplit("efs", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("ef") or text.endswith("efs"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"ef{gender_token}fe".join(text.rsplit("effe", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"ef{gender_token}fe{gender_token}s".join(text.rsplit("effes", 1))

  # tif/tive Noun
  if lemma.endswith("tif"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        noun._.value = f"tif{gender_token}ive".join(text.rsplit("tif", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"tif{gender_token}ive{gender_token}s".join(text.rsplit("tifs", 1))
    elif "Gender=Fem" in morph:
      if text.endswith("tif") or text.endswith("tifs"):
        noun._.value = text
      elif "Number=Sing" in morph:
        noun._.value = f"tif{gender_token}ive".join(text.rsplit("tive", 1))
      elif "Number=Plur" in morph:
        noun._.value = f"tif{gender_token}ive{gender_token}s".join(text.rsplit("tives", 1))

# Adjective
def replace_adj(adj: spacy.tokens.Token, gender_token="·"):
  morph = adj.morph
  text = adj.text
  lemma = adj.lemma_
  # Adjective lemma list
  if not any(adj.lemma_.endswith(ending) for ending in adj_lemma_endings):
    return None
  # eau/elle Adjective
  if lemma.endswith("eau"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adj._.value = f"elle{gender_token}au".join(text.rsplit("eau", 1))
      elif "Number=Plur" in morph:
        adj._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("eaux", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adj._.value = f"elle{gender_token}au".join(text.rsplit("elle", 1))
      elif "Number=Plur" in morph:
        adj._.value = f"elle{gender_token}au{gender_token}s".join(text.rsplit("elles", 1))

  # el/elle Adjective
  if lemma.endswith("el"):
    if "Gender=Masc" in morph:
      if "Number=Sing" in morph:
        adj._.value = f"el{gender_token}le".join(text.rsplit("el", 1))
      elif "Number=Plur" in morph:
        adj._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("els", 1))
    elif "Gender=Fem" in morph:
      if "Number=Sing" in morph:
        adj._.value = f"el{gender_token}le".join(text.rsplit("elle", 1))
      elif "Number=Plur" in morph:
        adj._.value = f"el{gender_token}le{gender_token}s".join(text.rsplit("elles", 1))

    # eur/rice;euse;eure Adjective
    if lemma.endswith("eur"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"eur{gender_token}rice".join(text.rsplit("rice", 1))
          adj._.value = f"eur{gender_token}euse".join(text.rsplit("euse", 1))
          adj._.value = f"eur{gender_token}e".join(text.rsplit("eure", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("rices", 1))
          adj._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("euses", 1))
          adj._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eures", 1))
      elif "Gender=Fem" in morph:
        if text.endswith("rice") or text.endswith("rices"):  # teur/trice and deur/drice Noun
          if "Number=Sing" in morph:
            adj._.value = f"eur{gender_token}rice".join(text.rsplit("rice", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"eur{gender_token}rice{gender_token}s".join(text.rsplit("rices", 1))
        elif text.endswith("euse") or text.endswith("euses"):  # eur/euse Noun
          if "Number=Sing" in morph:
            adj._.value = f"eur{gender_token}euse".join(text.rsplit("euse", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"eur{gender_token}euse{gender_token}s".join(text.rsplit("euses", 1))
        elif text.endswith("eure") or text.endswith("eures"):  # eur/eure Noun
          if "Number=Sing" in morph:
            adj._.value = f"eur{gender_token}e".join(text.rsplit("eure", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"eur{gender_token}e{gender_token}s".join(text.rsplit("eures", 1))

    # oux/ouse;ousse;ouce Adjective
    if lemma.endswith("oux"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"oux{gender_token}e".join(text.rsplit("oux", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("oux", 1))
      elif "Gender=Fem" in morph:
        if text.endswith("ouse"):
          if "Number=Sing" in morph:
            adj._.value = f"oux{gender_token}e".join(text.rsplit("ouse", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"oux{gender_token}e{gender_token}s".join(text.rsplit("ouses", 1))
        elif text.endswith("ousse"):
          if "Number=Sing" in morph:
            adj._.value = f"oux{gender_token}se".join(text.rsplit("ousse", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"oux{gender_token}se{gender_token}s".join(text.rsplit("ousses", 1))
        elif text.endswith("ouce"):
          if "Number=Sing" in morph:
            adj._.value = f"oux{gender_token}ce".join(text.rsplit("ouce", 1))
          elif "Number=Plur" in morph:
            adj._.value = f"oux{gender_token}ce{gender_token}s".join(text.rsplit("ouces", 1))

    # eux/euse Adjective
    if lemma.endswith("eux"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"eux{gender_token}e".join(text.rsplit("eux", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("eux", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"eux{gender_token}e".join(text.rsplit("euse", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"eux{gender_token}e{gender_token}s".join(text.rsplit("euses", 1))

    # s/se Adjective
    if lemma.endswith("s"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"{gender_token}xe".join(text.rsplit("s", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("s", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"{gender_token}xe".join(text.rsplit("se", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"{gender_token}xe{gender_token}s".join(text.rsplit("ses", 1))

    # tre/tresse Adjective
    if lemma.endswith("tre"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"tre{gender_token}xe".join(text.rsplit("tre", 1))
        elif "Number=Plur":
          adj._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tres", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"tre{gender_token}xe".join(text.rsplit("tresse", 1))
        elif "Number=Plur":
          adj._.value = f"tre{gender_token}xe{gender_token}s".join(text.rsplit("tresses", 1))

    # en/enne and ien/ienne Adjective
    if lemma.endswith("en"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"en{gender_token}ne".join(text.rsplit("en", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("ens", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"en{gender_token}ne".join(text.rsplit("enne", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"en{gender_token}ne{gender_token}s".join(text.rsplit("ennes", 1))

    # er/ère and ier/ière Adjective
    if lemma.endswith("er"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"er{gender_token}ère".join(text.rsplit("er", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("ers", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"er{gender_token}ère".join(text.rsplit("ère", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"er{gender_token}ère{gender_token}s".join(text.rsplit("ères", 1))

    # nt/nte and t/te Adjective
    if lemma.endswith("t"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"t{gender_token}e".join(text.rsplit("t", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("ts", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"t{gender_token}e".join(text.rsplit("te", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"t{gender_token}e{gender_token}s".join(text.rsplit("tes", 1))

    # nd/nde Adjective
    if lemma.endswith("nd"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"d{gender_token}e".join(text.rsplit("nd", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("nds", 1))
      if "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"d{gender_token}e".join(text.rsplit("nde", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"d{gender_token}e{gender_token}s".join(text.rsplit("ndes", 1))

    # on/onne Adjective
    if lemma.endswith("on"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"on{gender_token}ne".join(text.rsplit("on", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"on{gender_token}ne{gender_token}".join(text.rsplit("ons", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"on{gender_token}ne".join(text.rsplit("onne", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"on{gender_token}ne{gender_token}s".join(text.rsplit("onnes", 1))

    # u/ue Adjective
    if lemma.endswith("u"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"u{gender_token}e".join(text.rsplit("u", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("us", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"u{gender_token}e".join(text.rsplit("ue", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"u{gender_token}e{gender_token}s".join(text.rsplit("ues", 1))

    # é/ée Adjective
    if lemma.endswith("é"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"é{gender_token}e".join(text.rsplit("é", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("és", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"é{gender_token}e".join(text.rsplit("ée", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"é{gender_token}e{gender_token}s".join(text.rsplit("ées", 1))

    # i/ie Adjective
    if lemma.endswith("i"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"i{gender_token}e".join(text.rsplit("i", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("is", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"i{gender_token}e".join(text.rsplit("ie", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"i{gender_token}e{gender_token}s".join(text.rsplit("ies", 1))

    # al/ale Adjective
    if lemma.endswith("al"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"al{gender_token}e".join(text.rsplit("al", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("aux", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"al{gender_token}e".join(text.rsplit("ale", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"al{gender_token}e{gender_token}s".join(text.rsplit("ales", 1))

    # ef/effe Adjective
    if lemma.endswith("ef"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"ef{gender_token}fe".join(text.rsplit("ef", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"ef{gender_token}fe{gender_token}s".join(text.rsplit("efs", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"ef{gender_token}fe".join(text.rsplit("effe", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"ef{gender_token}fe{gender_token}s".join(text.rsplit("effes", 1))

    # tif/tive Adjective
    if lemma.endswith("tif"):
      if "Gender=Masc" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"tif{gender_token}ive".join(text.rsplit("tif", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"tif{gender_token}ive{gender_token}s".join(text.rsplit("tifs", 1))
      elif "Gender=Fem" in morph:
        if "Number=Sing" in morph:
          adj._.value = f"tif{gender_token}ive".join(text.rsplit("tive", 1))
        elif "Number=Plur" in morph:
          adj._.value = f"tif{gender_token}ive{gender_token}s".join(text.rsplit("tives", 1))


# TODO: review adjctive suffix and think about the way to match mas-fem nouns and adjectives
# adding ou/olle and others adjective suffix
# same adjective suffix has different forms of mas/fem adjective suffix