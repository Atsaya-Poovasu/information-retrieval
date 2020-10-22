#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#!!!!!!!!!!!!! Informtion  retrieval package PHASE 1 -> Educational institutions search engine   !!!!!!!!!!!!!!!!!!!#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  16pw08 Atsaya P & 16pw16 Jessy G    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('all')
import csv
from csv import writer
from googlesearch import search
import requests 
from bs4 import BeautifulSoup 
import operator 
from collections import Counter
from urllib.request import Request, urlopen
import re
from six.moves import urllib
from urllib.parse import *
import operator 
from collections import Counter

#These three lists will hold necessary information oobtained from each step
#it contains all the words obtained from the documents
document_list = []
#it contains the words obtained after removing symbols which is unnecessary
symbol_removed_list = []
#it contains the words obtained after pre processing 
preprocessed_list = []

#this is a function which removes unwanted symbols found in the document
def symbol_remover(preprocessed_list): 
	symbol_removed_list = [] 
	for term in preprocessed_list: 
		symbols = '!@#$%^&*()_•-\'+={[}]|\;:"<>?/., '
		for i in range (0, len(symbols)): 
			term = term.replace(symbols[i], '') 	
		if len(term) > 0: 
			symbol_removed_list.append(term)
	return symbol_removed_list

#this function creates a dictionary to contain word and their respective frequency
def dictionary_creator(symbol_removed_list): 
	term_count = {} 
	for term in symbol_removed_list: 
		if term in term_count: 
			term_count[term] += 1
		else: 
			term_count[term] = 1
	c = Counter(term_count) 
	result = sorted(c.items(), key=lambda pair: pair[1], reverse=True)
	return result 

#this function creates a term document matrix
def term_document_matrix(document_list):
	length = len(document_list)
	terms = {}
	for d in range(length):
		m = len(document_list[d])
		for i in range(m):
			if(document_list[d][i][0] not in terms.keys()):
				terms[document_list[d][i][0]] = [0 for k in range(length)]
	for d in range(length):
		m = len(document_list[d])
		for i in range(m):
			terms[document_list[d][i][0]][d] = document_list[d][i][1]
	terms = dict(sorted(terms.items()))
	print(terms)


#this function implements inverted indexing
def inverted_indexing(document_list):
	length = len(document_list)
	terms = {}
	for d in range(length):
		m = len(document_list[d])
		for i in range(m):
			if(document_list[d][i][0] not in terms.keys()):
				terms[document_list[d][i][0]] = []
 
	for d in range(length):
		m = len(document_list[d])
		for i in range(m):
			terms[document_list[d][i][0]].append((d+1, all_list[d][i][1]))
	terms = dict(sorted(terms.items()))
	print(terms) 



#this function will extract the text content from the web pages
def web_page_extractor(url, document_list ): 
	symbol_removed_list = []
	new_list = []
	preprocessed_list = []
	print("inverted indexing is performed")
	print(url)
	url = url[:-1]
	source_code = ""
	try:
		source_code = requests.get(url).text
	except:
		print("URL is invalid")
		return 
	soup = BeautifulSoup(source_code, 'html.parser') 
	for each_text in soup.findAll('p'): 
		content = ''
		soup = BeautifulSoup(source_code, 'html.parser') 
		for each_text in soup.findAll('p'): 
			content += each_text.text
		words = word_tokenize(content)	
		preprocessed_list = []
		for w in words:
			preprocessed_list.append(lemmatizer.lemmatize(w).lower())
		preprocessed_list = [w for w in preprocessed_list if not w in stop_words]

	symbol_removed_list = symbol_remover(preprocessed_list)
	new_list = dictionary_creator(symbol_removed_list)
	document_list.append(new_list)	
	return new_list	


#this performs web crawling in unirank web page which has more that 1000 universities of india
req = Request("https://www.4icu.org/in/")#this is the link of the web page
html_page = urlopen(req)
soup = BeautifulSoup(html_page, "html")
#print(soup)
## web links obtained are stored in uni.txt
file = open('universities.txt','a')
for link in soup.findAll('a'):
    schools = link.get('href')
    #print(schools)
    if re.search("/reviews/*[0-9]*.htm", schools):
      file.write("https://www.4icu.org"+link.get('href') + '\n')
file.close()

#this function will identify all available stop words from the module
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer() 
search= open('universities.txt', 'r') 
while True:  
    line = search.readline() 
    if not line: 
        break
    top_list = web_page_extractor(line, document_list)
    print(top_list)

print('\nInverted Index')
inverted_indexing(document_list )
print('\n obtained Term Document Matrix')
term_document_matrix(document_list ) 


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
