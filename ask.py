# Sandesh Koirala
# CSE 4392 - Final Project
# Question Generator

# !pip install -U spacy -q
#python -m spacy download en_core_web_md -q
import sys
import spacy
nlp = spacy.load('en_core_web_md')

"""# main function"""

def first_word_removed_questions(doc,numQ):
  questions=[]
  for sent in doc.sents:
    if len(questions)>=numQ:
      return questions
    if len(sent)<25:
      temp_q=""
      flag=0
      # print(sent)
      for token in sent:
        if (token.i-sent.start==0):
          if token.ent_type_ == "PERSON":
            flag=1
            temp_q=temp_q+"Who"
          elif token.ent_type_ == "ORG":
            flag=1
            temp_q=temp_q+"What"
          elif token.ent_type_ == "GPE":
            flag=1
            temp_q=temp_q+"What"
          elif token.ent_type_ == "DATE":
            flag=1
            temp_q=temp_q+"When"
          elif token.ent_type_ == "CARDINAL":
            flag=1
            temp_q=temp_q+"How Many"
          elif token.ent_type_ == "LOCATION":
            flag=1
            temp_q=temp_q+"How Many"
          else:
            temp_q=temp_q+" "+token.text
        elif (token.i-sent.start<4):
          if token.ent_iob_=="O":
            temp_q=temp_q+" "+token.text
        else:
          if token.text == ".":
            temp_q=temp_q+"?"
            continue
          temp_q=temp_q+" "+token.text
      if flag==1:
        # print(sent)
        questions.append(temp_q)
  return questions
  
def nsubj_removal(doc,numQ):
  questions=[]
  for sent in doc.sents:
    if len(questions)>=numQ:
      return questions
    if len(sent)<25 and len(sent)>4:
      temp_q=""
      flag=0
      # print(sent)
      for token in sent:
        if (token.i-sent.start==0):
          if token.dep_ == "nsubj" or token.dep_ == "pobj":
              if token.ent_type_ == "ORG":
                flag=1
                temp_q=temp_q+"What"
              elif token.ent_type_ == "GPE":
                flag=1
                temp_q=temp_q+"What"
              elif token.ent_type_ == "DATE":
                flag=1
                temp_q=temp_q+"When"
              elif token.ent_type_ == "CARDINAL":
                flag=1
                temp_q=temp_q+"How Many"
              elif token.ent_type_ == "LOCATION":
                flag=1
                temp_q=temp_q+"Where"
              else:
                temp_q=temp_q+"What"
                flag=1            
          else:
            if token.text == "'s":
              temp_q=temp_q+"'s"
              continue
            temp_q=temp_q+" "+token.text
        # elif (token.i-sent.start<4):
        #   if token.ent_iob_=="O":
        #     temp_q=temp_q+" "+token.text
        else:
          if token.text == ".":
            temp_q=temp_q+"?"
            continue
          if token.text == "'s":
            temp_q=temp_q+"'s"
            continue
          temp_q=temp_q+" "+token.text
      if flag==1:
        # print(sent)
        questions.append(temp_q)
  return questions


def main(datafile,numQ):
  f = open(datafile, "r")
  corpus= f.read()
  # print(corpus)
  doc=nlp(corpus)
  questions=[]
  questions1=first_word_removed_questions(doc,numQ)
  more_quest2=nsubj_removal(doc,numQ-len(questions))
  for x in questions1:
    x=x.replace("\n","")
    questions.append(x)
  for x in more_quest2:
    x = x.replace("\n", "")
    questions.append(x)
  return questions
    

if __name__ == "__main__":
    datafile = sys.argv[1]
    numQ = int(sys.argv[2])
    questions = main(datafile, numQ)
    for question in questions:
      print(question)
