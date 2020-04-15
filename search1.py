#from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
from docx import Document
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
#import os
#import collections
import sqlite3
#import operator
#from functools import reduce
import ast

def search(search_string):
    #final_lemmaList=[]
    #final_filtered_sentence=[]
    uniqueWordList=[]
    #flag=0
    
        #print(p.text)
    #listT=search_string.split()
    #print(listT)
    #for word in listT:
    #    finalList.append(word)
    for word in search_string.split():
        #wordT=ps.stem(word)
        #for wordX in uniqueWordList:
        #    if(word==wordX):
        #        flag=1
        #if(flag==0):
        #    uniqueWordList.append(word)
        #if(flag==1):
        #    flag=0
        if word not in uniqueWordList:
            uniqueWordList.append(word)
    stop_words=list(stopwords.words('english'))
    stop_words.append('AND')
    filtered_sentence=[w for w in uniqueWordList if not w in stop_words]
    # Lemmatization
    lemmaList=[]
    for word in filtered_sentence:
        lemmaList.append(WordNetLemmatizer().lemmatize(word))
    #print('*************** After lemmatization**********')
    print("lemmatized list = ",lemmaList)
    retreivedFromIndex(lemmaList,search_string)
def retreivedFromIndex(lemmaList,search_string):
    if "AND".upper() in search_string.upper():
        retreiveFromIndex_Cond_And(lemmaList)
    else:
        retreiveFromIndex_Cond_Or(lemmaList)    
def retreiveFromIndex_Cond_Or(lemmaList):
    qCondition=""
    all_matches=[]
    conn = sqlite3.connect('db1\\index1.db');
    c = conn.cursor()
    for term in lemmaList:
        qCondition=qCondition+"\""+term+"\","
    print('search results for:'+search_string)    
    for row in c.execute('select documents from index_store where term in('+qCondition[:-1]+')'):
        all_matches.append(set(ast.literal_eval(row[0])))
    if len(all_matches)>0:  
        results=list(set.union(*all_matches))
        print(sorted(results))  
    else:
        print("No matches found for the given query")  
    print('-'*20)         
def retreiveFromIndex_Cond_And(lemmaList):
    
    all_matches=[]
    qCondition=""
    conn = sqlite3.connect('db1\\index1.db');
    c = conn.cursor()
    for term in lemmaList:
        qCondition=qCondition+"\""+term+"\","
    #print('qCondition = ',qCondition)
    print('search results for:'+search_string)
    
    '''
    for i in lemmaList:
        print('i=',i)
        print(type(i))
        if(i not in all_terms):
            print(term,' not found')
        for row in c.execute('select documents from index_store where term =("'+i+'")'):
        #row=c.execute('select documents from index_store where term =("'+i+'")')
            print('row[0]=',row)
            all_matches.append(ast.literal_eval(row))
    print('all_matches=',all_matches)

    '''
    actual_words=0
    words_taken=0
    for i in qCondition[:-1].split(","):
        #print(i)
        actual_words+=1
    #print('actual_words = ',actual_words)
    for row in c.execute('select documents from index_store where term in('+qCondition[:-1]+')'):
        #print('row[0] = ',qCondition,row[0])
        words_taken+=1
    #print('words_taken = ',words_taken)
        #all_matches.append(set(ast.literal_eval(row[0])))

    if(words_taken==actual_words):
        for row in c.execute('select documents from index_store where term in('+qCondition[:-1]+')'):
            #print('row[0] = ',qCondition,row[0])
            all_matches.append(set(ast.literal_eval(row[0])))
        if len(all_matches)>0:  
            results=list(set.intersection(*all_matches))  
            print(sorted(results))
        else:
            print("No matches found for the given query")
        

    else:
        print("No matches found for the given query")
    print('-'*20)  

            
while True:            
    search_string=input("Search for? ")
    search(search_string)


