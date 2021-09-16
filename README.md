# QA

A Natural Language Processing based Question Answering System.

All commands must be executed from the directory containing this Readme

1. set init.sh as executable with the following command:
   chmod +x init.sh

2. Run init.sh to install all required dependencies and download nltk and spacy packages
   ./init.sh

3. run question generation program as:
   python3 ask.py article.txt nquestions

4. run answer generation program as:
   python3 answer.py article.txt questions.txt
