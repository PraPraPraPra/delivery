# import from nltk the functions that split a text into sentences and tokens
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk import word_tokenize, pos_tag, chunk
from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer

from gensim.test.utils import common_texts, get_tmpfile

#--------------------------------------------!ATTENTION!---------------------------------------------
#----------------------------------------!FIRST TIME RUNNING!----------------------------------------
# The first time using nltk, you should run:
#           import nltk
#           nltk.download()
# ---- OR ----
#           import nltk
#           nltk.download('punkt')
#           nltk.download('wordnet')
#           nltk.download('omw-1.4')
#           nltk.download('stopwords')
#----------------------------------------!FIRST TIME RUNNING!----------------------------------------
#--------------------------------------------!ATTENTION!---------------------------------------------



"""
Problems:

Erros na lematização:
    ex.: EE e Java EE não são a mesma coisa (Electrical Engeneering e Java Enterprise Edition);
    ex.: muitas palavras com "/" -> A barra tem que ser " "(espaço)


"""

#----------------------------------------------!INTRO!-----------------------------------------------
#----------------------------------------------------------------------------------------------------
# This method receives the dava (read from a csv) and transforms it to a more usefull state for
#  Word2Vec.
#
# It follows the following sequence:
#
# 1- Replace most of the symbols found in the dataset with a whitespace " ".
#     This is usefull for reducing the number of total words in the full vocabulary.
#   
# 2- Uses a hand-crafted synonym list for some skills present in the dataset.
#     This is needed because "angular", "angular2" and "angular5" all represent the same skill.
#       
#     Word2Vec has no way to know that these words are actually the same skill.
#     It is possible that, with a big enough dataset we won't need a synonym list;
#     However, that would be dependent on people explicitly writing "angular2 and angular5" in cvs.
#       
#     A possible alternative is to use lemmatization, but this lead to other problems in our
#     initial approach. We left the code for lemmatization as a comment if you want to try it.
#
# 3- Remove stopwords (like and, or, if,....) using "stopwords" from nltk to reduce vocab size.
#     Read: https://towardsdatascience.com/text-pre-processing-stop-words-removal-using-different-libraries-f20bac19929a
#
# 4- Write word count to file (for hand analysis) and return: (filtered_words, max_size, version)
#----------------------------------------------------------------------------------------------------
#----------------------------------------------!INTRO!-----------------------------------------------

#TODO insert number of vocab reduced
#TODO symbols before or after stopwords?
def skill_transform(data):

    # Replace the version number so that the output is stored in a different named file.
    # Otherwise, it overrides the last file with the same version
    version = "v7"

    #Synonym:
    # Special cases replace
    special_case = {}
    special_case["javascript"] = [ "java script ", "java script." ]
    special_case["ood"] = [ "object oriented design", ]
    special_case["oop"] = [ "object oriented programming", ]
    special_case["olap"] = [ "online analytical processing" ]
    special_case["ecommerce"] = [ "e commerce" ]
    special_case["ux"] = [ "user experience", "web user experience design", "user experience design", "ux designer", "user experience/ux" ]
    special_case["html5"] = [ "html 5" ]
    special_case["j2ee"] = [ "jee" ]
    special_case["osx"] = [ "mac os x", "os x" ]
    special_case["senior"] = [ " sr ", " sr. " ]
    special_case["qa"] = [ "quality" ]
    special_case["bigdata"] = [ "big data"]
    special_case["webservice"] = [ "webservices", "website", "webapps" ]
    special_case["xml"] = [ "xml file", "xml schemas", "xml web service" ]
    special_case["nlp"] = [ "natural language process", "natural language", "nltk" ]
    special_case["aws"] = [ "amazon web service"]
    special_case["java"] = [ "java ee"]
    special_case["angular"] = ["angularjs", "angular2", "angular5", "angular", "angular.js", "angular2+", "angularjs-"]
    special_case["backend"] = ["back-end", "back- end", "back end"]
    special_case["frontend"] = ["front-end", "front- end", "front end"]
    special_case["springboot"] = ["spring-boot", "spring boot"]


    # Create Job description list;
    # Each element of the List will be a a single job description in the form: [ [[first], [job], [description]], [[2nd], [job], [here]], ...]
    job_descriptions=[]

    #Replace symbols; Each "job" is a single job description.
    for job in data.Description:
        j = job.replace(',', ' ')
        i = j.replace('/', ' ')
        l = i.replace(';', ' ')
        m = l.replace('%', ' ')
        n = m.replace('(', ' ')
        o = n.replace(')', ' ')
        p = o.replace('. ', ' ') # This has to be ". " (a full stop) and not "." because skills like .net and D3.js are valid skill names.
        q = p.replace(' - ', ' ')
        r = q.replace(' -- ', ' ')

        x = r.replace('\\', ' ')

        # Quick way to translate multiple whitespaces to a single whitespace.
        z = " ".join(x.split())

        # Everything to lowercase (reduces the total vocab size: JavaScript is the same as Javascript and javascript).
        k = z.lower()

        # Iterate through the hand-crafted synonym list and replace each term with its canonnical form.
        for root_skill in special_case:
            for synonym in special_case[root_skill]:
                k = k.replace(synonym, root_skill)

        # Add complete description to job_description list.
        job_descriptions.append(k)


    #Words tokenization (using nltk)
    jobs = [word_tokenize(d) for d in job_descriptions]



    #Lemmatize - Left this here in case you want to try it
    #lemmatizer = WordNetLemmatizer()
    #lem=[]
    #for job in no_capitals:
    #    lem.append([lemmatizer.lemmatize(j) for j in job])

    #Remove stopwords (using nltk)
    #Good intro to stopwords:
    #https://towardsdatascience.com/text-pre-processing-stop-words-removal-using-different-libraries-f20bac19929a
    filtered_words = []
    stopwords_dict = {key : "" for key in stopwords.words('english')}
    for job in jobs:
        filtered_words.append([j for j in job if not j in stopwords_dict])




    #TODO Remove symbols here...?
    #cleaned_description=[]
    #extra_dict = {key : "" for key in ['(',')','.',',',':','%', ';']}
    #for job in filtered_words:
    #    cleaned_description.append([j for j in job if not j in extra_dict])



    #Easy way to count number of appearences of each unique word
    from collections import Counter
    count = Counter(x for xs in filtered_words for x in set(xs))
    ordered_count_list = count.most_common()
    
    #Save word count to a file
    with open(f'data/ggeop/counter_{version}.txt', 'w') as f:
        for item in ordered_count_list:
            f.write(f'{item[0]} : {item[1]}\n')

    #Max_size will be needed to choose the parameters for training the model
    max_size = len(max(filtered_words, key=len))

    return (filtered_words, max_size, version)
