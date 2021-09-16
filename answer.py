#Sandesh Koirala
#CSE 4392 - Final Project
# answer generator
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk import tokenize
import nltk
import sys
# !pip install -U spacy
# !python -m spacy download en_core_web_sm -q
nltk.download('punkt',quiet=True)
import spacy
nlp = spacy.load('en_core_web_md')

# Method that reads article line by line and adds it to a string.
def read_article(article):
    with open(article, "r") as f:
        return " ".join([clean_sent for clean_sent in [raw_sent.strip("\n\t ") for raw_sent in f.readlines()] if len(clean_sent) > 0])

# Method to tokenize the string into sentences (documents), returns the data set
def create_data_set(corpus_text):
    data_set = tokenize.sent_tokenize(corpus_text)
    return data_set

# Method that creates the vectorizer and builds the document tfidf
def build_tfidf(dataset):
    vectorizer = TfidfVectorizer(input=dataset, analyzer='word', ngram_range=(1,1),
                                 min_df=0, stop_words=None)
    docs_tfidf = vectorizer.fit_transform(dataset)

    return vectorizer, docs_tfidf

# Method to calculate the cosine similarity scores between the query and the documents.
def get_cosine_similarities(vectorizer, docs_tfidf, question):
    # Vectorizes the question
    query_tfidf = vectorizer.transform([question.lower()])

    # Computes the cosine similarities between the query and the docs.
    cosine_similarities = (query_tfidf * docs_tfidf.T).toarray()

    return cosine_similarities


# Method to test for if the matrix is zeroed or not
def is_zero(cosine_similarities):
    if not np.any(cosine_similarities):
        return True
    return False


# Tests for a zeroed array and will create the proper return sentence and percentage.
def get_return_value(data_set, cosine_similarities):
    if not is_zero(cosine_similarities):
        sentence = data_set[np.argmax(cosine_similarities)]
    else:
        sentence = "Not Found"
    percentage = np.max(cosine_similarities)

    return sentence, percentage


# Main called method to find the most similar document to the query.
def query_sentence(article, question):
    article = read_article(article)
    question = question.lower()
    # Check for if article has data in it. If article not found, skip to the end and return.
    if article:
        data_set = create_data_set(article)

        vectorizer, docs_tfidf = build_tfidf(data_set)

        cosine_similarities = get_cosine_similarities(vectorizer, docs_tfidf, question)

        sentence, percentage = get_return_value(data_set, cosine_similarities)

        return sentence

    return "Not Found"

#find the answer phrase in    question according to the question type
def find_phrase(sentence,q_type,question):
  question_doc=nlp(question)
  doc=nlp(sentence)
  required_entity=None
  if q_type=="who":
    required_entity="PERSON"
  if q_type=="how_many":
    required_entity="CARDINAL"
  if q_type=="when":
    required_entity="DATE"
  if q_type=="where":
    required_entity="GPE"
  if q_type=="which":
    required_entity="PERSON"
  if q_type =="why":
    return sentence
  if q_type=="how":
    return sentence
  if q_type == "what":
    return sentence
  
  ents=list(doc.ents)
  # print("required_ent: " + required_entity)
  # print("ents: ")
  #print(ents)
  question_ents=[x for x in question_doc.ents]
  question_ent_text=[x.text for x in question_ents]
  # print(question_ent_text)
  if len(ents)<1:
    return "Not Found"
  for ent in doc.ents:
    if ent.label_==required_entity:
      if ent.text not in question_ent_text:
        return ent.text
  return "Not Found"

#analyze wh question type
def analyze_question(question_orig):
  question_orig=question_orig.lower()
  question=str(question_orig).lower().split()
  if question_orig.find("how many")>=0:
    return "how_many"
  question_type = ['who','when','where','which','why','what',"how"]
  for x in question_type:
    if x in question:
      return x  
  return "Not Found"

#main query function
def find_answer(article,questions):
  sentence= query_sentence(article,question)
  if sentence == "Not Found":
    return sentence
  q_type=analyze_question(question)
  if q_type=="Not Found":
    return sentence
  answer=find_phrase(sentence,q_type,question)
  # print("sent: "+ sentence)
  # print("q-type: "+q_type)
  # print("question: "+ question)
  # print("answer sentence: "+ sentence)
  return answer

#print(find_answer("/a2.txt", "When did the school open the Blanton Museum of Art?"))

if __name__ == "__main__":
  datafile=sys.argv[1]
  questions=sys.argv[2]
  r=open(questions,"r")
  questions_read=r.read()
  questions=questions_read.split("\n")
  answers=[]
  for question in questions:
    answer=find_answer(datafile,question)
    print(answer)
  
