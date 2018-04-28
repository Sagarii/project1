# ## IPython Notebook for [Bommarito Consulting](http://bommaritollc.com/) Blog Post
# ### **Link**: [Fuzzy sentence matching in Python](http://bommaritollc.com/2014/06/fuzzy-match-sentences-in-python): http://bommaritollc.com/2014/06/fuzzy-match-sentences-in-python
# **Author**: [Michael J. Bommarito II](https://www.linkedin.com/in/bommarito/)
#https://pythonspot.com/nltk-stemming/

# Imports
import nltk.corpus
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import string

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

ps = PorterStemmer()

def is_ci_token_stopword_match(a, b):
    """Check if a and b are matches."""
    tokens_a = [token.lower().strip(string.punctuation) for token in word_tokenize(a) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in word_tokenize(b) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    stems_a = [ps.stem(token) for token in tokens_a]
    stems_b = [ps.stem(token) for token in tokens_b]
    
    return (stems_a == stems_b)