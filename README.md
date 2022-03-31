# Intro

This is an exploratory/Proof Of Concept project that seeks to create a cv search engine. By providing at least one skill and a date, this should return the list of CVs that best match that skill(s) and that are available as close as possible to the chosen date.

Eg: Wanting to search for skills in Django and not having anyone with that skill explicitly written in the resume, the program should be able to find the top matching cv's with the most simillar techologies/expertise (for example, Python).


# Reasoning and possible paths

There are several possible paths to tackle this problem. Each with their own advantages and difficulties. This section seeks to go through the various paths available so that we can understand the reasons that led us to the current solution.

Starting with the essential ingredients, you will always need:
  - A database that stores each person's skills (Does it store complete CVs? Only skills in a list?);
  - A way to calculate similarities between various skills (or between various cv's) so that we can relate them (use hand-made lists? Natural Language Processing? Neural Networks?); 



## Data Base

The database is the most pragmatic variable - it will only be set according the the rest of the decisions.
In this case, we chose Elasticsearch as it appears to fit in well with the other constraints (mainly: It has vector searchs built in).

## Skill Similarity

The method to determine the similarities between skills will be the trickiest. In practice, we don't need to have a hyper-precise degree of similarity between all existing skills - it would be of very little value to determine whether Python is closer to React or to Angular. The only thing that matters is that the model understands that both React and Angular are much closer to each other than to Python. 

Keeping this in mind, there will be several classes of solutions:
   - Hand-compiled solutions *(like have a list of similar skills)* -> Overwelming and not maintanable;
   - NLP models *(like Word2Vec)*
   - Neural Networks
   - Knowledge Graph *(A directed graph, which shows the relationships between the various skills: https://www.baeldung.com/cs/ml-knowledge-graphs)*

Hand-compiled solutions are obviously a no-go (slow to create, hard to maintain, needs to have complex decisions taken for every skill,...).

It appears that the best solution for understanding the similarities among skills would be a Knowledge Graph that automatically learns and explicitaly represents all the relationships between each skills.
This is, however, incredibly non-trivial. Maybe it would be a good decision when the field is more mature or if we have someone with the proper set of expertise.

Models base on Neural Nets offer good performance and are able to make good generalistic models (https://tfhub.dev/google/universal-sentence-encoder/4, https://github.com/google-research/bert).
When it comes to the pre-trained models (like USE4 and BERT), they are good for generalistic porpuses but they fail when it comes to specific knowledge. This means that USE4 can understand that "Javascript" is closer to "Angular" than to "dog" but it has no ideia on weather "javascript" is closer to "angular" or to 

Optámos por treinar o nosso próprio modelo de NLP, utilizando como base Word2Vec e alguns outros projectos que já caminharam neste sentido (bibliografia no fim).


Uma neural network precisa de datasets muito maiores que as opções e não traz nenhuma vantagem ao problema.

# Tecnologias
Para isto, vamos utilizar o Elasticsearch juntamente com um modelo de Natural Language Processing (NLP).

O Elasticsearch tem uma funcionalidade que nos permite utilizar um modelo pré-treinado de NLP para calcular um score de próximidade entre um critério de pesquisa e os dados em base de dados (criando assim uma lista ordenada por critérios de maior semelhança) : https://www.elastic.co/blog/text-similarity-search-with-vectors-in-elasticsearch

O Elasticsearch oferece vários modelos já treinados que podem ser usados para calcular este grau de próximidade. No entanto, como procuram ser modelos generalizados não conseguem capturar as diferenças várias tecnologias diferentes (conseguem perceber que "C++" está mais perto de "Java" do que de "lavatório" mas não têm noção das relações entre as várias tecnologias onde, por exemplo, "Python" e "Flask" teriam de estar sempre mais próximos do que "Python" e "PowerPoint").

# Understanding the Project


This project is (conceptually) split into the following responsabilities:
 - Processing and transforming the dataset (so that you can efficiently use it for the NLP model); -> **skill_transform_v4.py** (called by skill_similarity.py)
 - Training the NLP model; -> **skill_similarity.py**
 - Defining an Elasticsearch index with the proper mapping; -> **elastic_test_resumes.py**
 - Spin up Elastic -> Docker *(elastic.sh)*
 - Upload new data to the Elasticsearch index, making sure to translate the raw data *(skill names)* into the proper vectors from the model trained in skill_similarity.py -> Currently handled by *elastic_main.py* for testing porpuses
 - Listen for queries as inputs *(currently missing)*, automatically translate them and retrieve data -> Currently **elastic_query.py** for testing porpuses, not complete - should be **elastic_main.py** *(could also add options to the console so that you can decide on weather to start a new instance, submit new queries, decide index name,...)*


```
project
|   requirements.txt
|   requirements_elastic.txt
|   requirements_nlp.txt
|   saved_model
|---code
    | skill_similarity.py
    | skill_transform_v4.py
    | elastic_main.py
    | elastic_query.py
|---scripts
    | first-run.sh
    | elastic.sh
    | kibana.sh
|---data
    |....

```

# Instalation


This requires python 3.8. It has not been tested with other python versions.

```
  Python --version:
    python 3.8.10
```

**If** you want to run the whole project you should pip install "requirements.txt" using the terminal:

```
pip install -r requirements.txt
```

**If** you only want to run the Elasticsearch or the NLP part of the project, you can *pip install* the corresponding *requirements_...*  using the terminal:

```
pip install -r requirements_word2vec.txt
```
**OR**
```
pip install -r requirements_elasticsearch.txt
```

**If** you're using Elasticsearch, you should also download and run the corresponding docker images (for elasticsearch and kibana):

For elasticsearch:
```
docker pull elasticsearch
```
For kibana *(In short: Run first-run.sh; Pull the docker kibana image with `docker pull docker.elastic.co/kibana/kibana:8.0.1`)*:
```
Follow: https://www.elastic.co/guide/en/kibana/current/docker.html
```


# Usage

- 1: For Elasticsearch and Kibana, you should first run **elastic.sh** and then **kibana.sh**.

Both files are included in the /scripts folder.
For following runs, you can list your docker containers (docker ps -a) and restart the stop elastic and kibana containers (docker start ID_HERE).
Kibana is only usefull to have an easier insight into the elastic database - it's not mandatory.

- 2: For NLP, **read the comments at the start of skill_transform_v4.py**.
- 3: If you wish to retrain and save a new model, run **skill_similarity.py**. You can change the data or the functions to get a better model. A pre-trained model is currently in this repo.
- 4: If you wish to create a new index in your elastic database, run **elastic_main.py**. This also uploads some test data that you can find in *elastic_test_resumes.py*. The mappings for the database is also in this last file. The index name must be unique.
- 5: Search your database. There are some example queries in **elastic_request.py**. The query for skill similarity *(that looks for similar vectors)* is not currently working *(there is something wrong with the way the script is created - the database has the vectors)*.

# Known Problems

1- The query for skill similarity *(that looks for similar vectors)* is not currently working.
ElasticSearch has its own query language. Querying for normal fields is not the same as nested fields. Searching for vector similarity is also not the same as searching for word matches. Quering for vector similarity in a nested field does not appear to be trivial.

2- This only works for known skills. If a certain skill is not present in the dataset used for training, the model won't be able to compute the distance to other skills. This means that the database needs to be bigger.


# Bibliography
Bibliography from several other NLP projects:

    https://github.com/ggeop/Job-Recommendation-Engine.git
    https://github.com/vgangaprasad/ML_Skills_Match.git
    https://github.com/Jwata/job-word-embeddings.git
    https://github.com/duyet/skill2vec.git
    https://github.com/duyet/skill2vec-dataset.git
    https://github.com/duyet/related-skills.git


###     https://github.com/ggeop/Job-Recommendation-Engine.git

-> Utiliza a descrição de um trabalho para tentar prever o seu título.
Obtém os dados (10K) do indeed.com.
Partilhar o código do crawler.
Testam vários modelos para perceber qual o mais eficiente a fazer o mapeamento "Descrição" -> "Título";
Têm um número limitado de "Títulos" (a que eles chamam de Queries);
Os modelos testados (ex.: CNN) não são fáceis de aplicar a este problema: seria preciso criar uma lista de todas as tecnologias existentes para calcular as distâncias entre estas e cada descrição fornecida.
No que toca ao modelo de Word2Vec, ainda não testei a eficácia... 10K é um bom dataset, mas é preciso filtrar tudo o que não sejam tecnologias...



###     https://github.com/vgangaprasad/ML_Skills_Match.git

###    https://github.com/Jwata/job-word-embeddings.git



###    https://github.com/duyet/skill2vec-dataset.git
-> Has a 50K token "skills" dataset. The dataset is not perfect and the "skills" aren't allways perfect, and you don't have access to the raw data.

Word2Vec with this dataset alone prodeces no usefull results.
-------- INSERT EXAMPLE ---------

###    https://github.com/duyet/related-skills.git
-> Has a 1k raw Dataset and nothing else of use;

###    https://github.com/duyet/skill2vec.git