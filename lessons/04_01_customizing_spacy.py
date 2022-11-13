#   NAMED ENTITY RECOGNITION SERIES   #
#             Lesson 04               #
#        Leveraging spaCy's NER       #
#               with                  #
#        Dr. W.J.B. Mattingly         #

# Generating rules in spaCy
# leverage training process to customize spaCy

# works only on clean data... doesn't account for misspellings etc.

from catalogue import create
import spacy 
from spacy.lang.en import English
from spacy.pipeline import EntityRuler #helps create rules
import json

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def generate_better_characters(file):
    data = load_data(file)

    print(f"original list #: {len(data)}") 

    new_characters = []

    for item in data:
        new_characters.append(item)

    # cleaning up name list
    for item in data:
        item = item.replace("The", "").replace("the", "").replace("and", "").replace("And", "")
        names = item.split(" ")

        for name in names:
            name = name.strip()
            new_characters.append(name)

        if "(" in item:
            names = item.split("(")
            for name in names:
                name = name.replace(")", "").strip()
                new_characters.append(name)
        
        if "," in item:
            names = item.split(",")
            for name in names:
                name = name.replace("and", "").strip()
                
                if " " in name:
                    new_names = name.split()
                    for x in new_names:
                        x = x.strip()
                        new_characters.append(x)
                new_characters.append(name)
    
    print(f"cleaned list #: {len(new_characters)}")  

    final_characters = [] # list of all potential patterns of how characters might appear
    titles = ["Dr.", "Professor", "Mr.", "Mrs.", "Ms.", "Miss", "Aunt", "Uncle", "Mr. and Mrs."]

    for character in new_characters:
        if character != "": # remove blank instances
            final_characters.append(character)

            for title in titles: # accounting for all possibilities of titles + names
                titled_char = f"{title} {character}"
                final_characters.append(titled_char)

    print(f"all potential titles for characters included #: {len(final_characters)}")
    
    final_characters = list(set(final_characters)) # remove duplicates
    print(f"all potential titles w/o duplicates #: {len(final_characters)}")

    final_characters.sort() #alphabetically sort 
    return final_characters


# Done! At this stage the data is cleaned and ready to be processed into spaCy

def create_training_data(file, type):
    data = generate_better_characters(file)
    patterns = []

    for item in data:

        pattern = { #training models aways need a type and a pattern
                    "label": type,
                    "pattern": item
                    }

        patterns.append(pattern)
    return patterns

def generate_rules(patterns):
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns) # passing our patterns to spaCy
    nlp.to_disk("hp_ner") # save model

def test_model(model, text):
    doc = nlp(text)
    results = []

    for ent in doc.ents:
        results.append(ent.text)
    return results

patterns = create_training_data("data/hp_characters.json", "PERSON")
# print(patterns)

# generate_rules(patterns) #load patterns

nlp = spacy.load("hp_ner") # load model

with open("data/hp.txt", "r") as f:
    text = f.read()
    ie_data = {}

    # cleaning up data a bit
    chapters = text.split("CHAPTER")[1:] # ex. "CHAPTER 1" --> " " "1" --> grab "1" onwards

    for chapter in chapters:
        chapter_num, chapter_title = chapter.split("\n\n")[0:2]
        chapter_num = chapter_num.strip()
        segments = chapter.split("\n\n")[2:]
        hits = []

        for segment in segments:
            segment = segment.strip()
            segment = segment.replace("\n", " ") # ALWAYS remove line breaks from nlp - throws it off
            results = test_model(nlp, segment)

            for result in results:
                hits.append(result)

        ie_data[chapter_num] = hits # create dictionary
    
save_data("data/hp_data.json", ie_data)

# Split names into first and last name

# import spacy
# from spacy.lang.en import English
# from spacy.pipeline import EntityRuler
# import json


# def load_data(file):
#     with open(file, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return (data)

# def save_data(file, data):
#     with open (file, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)

# def generate_better_characters(file):
#     data = load_data(file)
#     print (len(data))
#     new_characters = []
#     for item in data:
#         new_characters.append(item)
#     for item in data:
#         item = item.replace("The", "").replace("the", "").replace("and", "").replace("And", "")
#         names = item.split(" ")
#         for name in names:
#             name = name.strip()
#             new_characters.append(name)
#         if "(" in item:
#             names = item.split("(")
#             for name in names:
#                 name = name.replace(")", "").strip()
#                 new_characters.append(name)
#         if "," in item:
#             names = item.split(",")
#             for name in names:
#                 name = name.replace("and", "").strip()
#                 if " " in name:
#                     new_names = name.split()
#                     for x in new_names:
#                         x = x.strip()
#                         new_characters.append(x)
#                 new_characters.append(name)
#     print (len(new_characters))
#     final_characters = []
#     titles = ["Dr.", "Professor", "Mr.", "Mrs.", "Ms.", "Miss", "Aunt", "Uncle", "Mr. and Mrs."]
#     for character in new_characters:
#         if "" != character:
#             final_characters.append(character)
#             for title in titles:
#                 titled_char = f"{title} {character}"
#                 final_characters.append(titled_char)


#     print (len(final_characters))
#     final_characters = list(set(final_characters))
#     print (len(final_characters))
#     final_characters.sort()
#     return (final_characters)

# def create_training_data(file, type):
#     data = generate_better_characters(file)
#     patterns = []
#     for item in data:
#         pattern = {
#                     "label": type,
#                     "pattern": item
#                     }
#         patterns.append(pattern)
#     return (patterns)

# def generate_rules(patterns):
#     nlp = English()
#     ruler = EntityRuler(nlp)
#     ruler.add_patterns(patterns)
#     nlp.add_pipe(ruler)
#     nlp.to_disk("hp_ner")

# def test_model(model, text):
#     doc = nlp(text)
#     results = []
#     for ent in doc.ents:
#         results.append(ent.text)
#     return (results)

# patterns = create_training_data("data/hp_characters.json", "PERSON")
# generate_rules(patterns)
# # print (patterns)

# nlp = spacy.load("hp_ner")
# ie_data = {}
# with open ("data/hp.txt", "r")as f:
#     text = f.read()

#     chapters = text.split("CHAPTER")[1:]
#     for chapter in chapters:
#         chapter_num, chapter_title = chapter.split("\n\n")[0:2]
#         chapter_num = chapter_num.strip()
#         segments = chapter.split("\n\n")[2:]
#         hits = []
#         for segment in segments:
#             segment = segment.strip()
#             segment = segment.replace("\n", " ")
#             results = test_model(nlp, segment)
#             for result in results:
#                 hits.append(result)
#         ie_data[chapter_num] = hits

# save_data("data/hp_data.json", ie_data)
