#   NAMED ENTITY RECOGNITION SERIES   #
#             Lesson 04.02            #
#        Leveraging spaCy's NER       #
#               with                  #
#        Dr. W.J.B. Mattingly         #

# Take training data to cultivate a good training dataset

import spacy
import json
import random

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def test_model(model, text):
    doc = nlp(text)
    results = []
    entities = []

    for ent in doc.ents: # spacy wants to see TRAIN_DATA = [(text, ("entities": [(start, end, label)]})]
        entities.append((ent.start_char, ent.end_char, ent.label_)) # building out the (start, end, label) part

    if len(entities) > 0: # if an entity has been found
        results = [text, {"entities": entities}]
    return results

nlp = spacy.load("hp_ner") # load model
TRAIN_DATA = []

with open("data/hp.txt", "r") as f:
    text = f.read()

    # cleaning up data a bit
    chapters = text.split("CHAPTER")[1:] # ex. "CHAPTER 1" --> " " "1" --> grab "1" onwards

    # break down data into chapters
    for chapter in chapters:
        chapter_num, chapter_title = chapter.split("\n\n")[0:2]
        chapter_num = chapter_num.strip()
        segments = chapter.split("\n\n")[2:]
        hits = []

        for segment in segments:
            segment = segment.strip()
            segment = segment.replace("\n", " ") # ALWAYS remove line breaks from nlp - throws it off
            results = test_model(nlp, segment)

            if results != []: # if found something
                TRAIN_DATA.append(results)
    
save_data("data/hp_training_data.json", TRAIN_DATA)

print(len(TRAIN_DATA))