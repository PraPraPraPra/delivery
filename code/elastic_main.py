from datetime import datetime
from os import read, system
from elasticsearch import Elasticsearch
import csv
import json
import resumes
import simple_resumes

def load_csv(filename):
    with open('cv_accenture_1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        #reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            print(str(row))
            return json.loads(str(row))

es = Elasticsearch()

index_name= "test-cv-v40"


es.indices.create(index = index_name, mappings=simple_resumes.get_mapping())
#es.indices.create(index = index_name)

index=1
for resume in simple_resumes.get_resumes():
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