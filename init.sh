!# /bin/sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install -U scikit-learn
pip install numpy
pip install --user -U nltk
pip install -U spacy
python3 -m spacy download en_core_web_md -q
