from datetime import datetime
from os import read, system
from elasticsearch import Elasticsearch
import csv
import json
import resumes
import simple_resumes

es = Elasticsearch()

index_name= "test-cv-v40"

index = 3

print("++++ Getting Resumes ++++")
print("------------")
for i in range(1, index+1):
    print("--- " + str(i) + " ---")

    res = es.get(index=index_name, id=i)
    print(res['_source'])
    print("--- ---\n")
print("------------")
print("++++\n")


print("++++ Query 1 (tem python como skill?) ++++")
print("------------")
res2 = es.search(index=index_name, query={
    "nested" : {
        "path" : "skills",
        "query" : {
            "match" : {
                "skills.skill" : "Python"
            }
        },
        "inner_hits": {}
    }
})
#print(res2)
print("Got %d Hits:" % res2['hits']['total']['value'])
for hit in res2['hits']['hits']:
    print(hit["_source"])
print("------------")
print("++++\n")




print("++++ Query 2 (Python + Begginer)++++")
print("------------")
res1 = es.search(index=index_name, query={
    "nested" : {
        "path" : "skills",
        "query" : {
            "bool": {
                "must": [
                        {"match" : {"skills.skill" : "Python" } },
                        {"match" : {"skills.experience" : "Begginer" } }
                ]
            }
        },
        "inner_hits": {}
    }
})
#print(res1)
print("Got %d Hits:" % res1['hits']['total']['value'])
for hit in res1['hits']['hits']:
    print(hit["_source"])
print("------------")
print("++++\n")





print("++++ Query 3 (Python + Begginer e English Advanced)++++")
print("------------")
res3 = es.search(index=index_name, query={
    "bool" : {
        "must" : {
            "nested" : {
                "path" : "skills",
                "query" : {
                    "bool": {
                        "must": [
                                {"match" : {"skills.skill" : "Python" } },
                                {"match" : {"skills.experience" : "Begginer" } }
                        ]
                    }
                },
                "inner_hits": {}
        }
        },
        "must" : {
            "nested" : {
                "path" : "languages",
                "query" : {
                    "bool": {
                        "must": [
                                {"match" : {"languages.language" : "English" } },
                                {"match" : {"languages.level" : "Advanced" } }
                        ]
                    }
                },
                "inner_hits": {}
            }
        }
    }
})
#print(res3)
print("Got %d Hits:" % res3['hits']['total']['value'])
for hit in res3['hits']['hits']:
    print(hit["_source"])
print("------------")
print("++++\n")




print("++++ Query 4 (Python + Begginer e English Advanced com boost em free_date)++++")
print("------------")
res3 = es.search(index=index_name, query={
    "bool" : {
        "must" : {
            "nested" : {
                "path" : "skills",
                "query" : {
                    "bool": {
                        "must": [
                                {"match" : {"skills.skill" : "Python" } },
                                {"match" : {"skills.experience" : "Begginer" } }
                        ]
                    }
                },
                "inner_hits": {}
        }
        },
        "must" : {
            "nested" : {
                "path" : "languages",
                "query" : {
                    "bool": {
                        "must": [
                                {"match" : {"languages.language" : "English" } },
                                {"match" : {"languages.level" : "Advanced" } }
                        ]
                    }
                },
                "inner_hits": {}
            }
        },
        "should" : {
            "query" : {
                "bool": {
                    "must": [
                            {"match" : {"languages.language" : "English" } },
                            {"match" : {"languages.level" : "Advanced" } }
                    ]
                }
            },
            "inner_hits": {}
        }
        }
    }
)
#print(res3)
print("Got %d Hits:" % res3['hits']['total']['value'])
for hit in res3['hits']['hits']:
    print(hit["_source"])
print("------------")
print("++++\n")