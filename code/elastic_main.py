from datetime import datetime
from os import read, system
from elasticsearch import Elasticsearch
import csv
import json
import elastic_test_resumes
from gensim.models import Word2Vec


#Not called
def load_csv(filename):
    with open('cv_accenture_1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        #reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            print(str(row))
            return json.loads(str(row))

es = Elasticsearch()

#Update name for every new index created
#Since this is test code, there currently is no index management here.
index_name= "test-cv-v70"


es.indices.create(index = index_name, mappings=elastic_test_resumes.get_mapping())

model = Word2Vec.load("saved_model")


index=1
for resume in elastic_test_resumes.get_resumes():
    for skill in resume.get("skills"):
        lower_case= skill.get("skill").lower()
        if skill.get("skill").lower() in model.wv.key_to_index :
            skill["skill_vector"] = model.wv.get_vector(skill.get("skill").lower())
    res = es.index(index=index_name, id=index, document=resume)
    print("++++ Adding Resume " + str(index) + " ++++")
    print(res['result'])
    print("------------\n")
    index += 1


print("++++ Getting Resumes ++++")
print("------------")
for i in range(1, index):
    print("--- " + str(i) + " ---")

    res = es.get(index=index_name, id=i)
    print(res['_source'])
    print("--- ---\n")
print("------------")
print("++++\n")