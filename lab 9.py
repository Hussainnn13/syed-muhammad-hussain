import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Natural Language Processing is fun. Let's learn it step by step!"

sentences = sent_tokenize(text)
print("Sentence Tokenization:")
print(sentences)


words = word_tokenize(text)
print("\nWord Tokenization:")
print(words)
