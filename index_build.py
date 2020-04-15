#from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
#import docx as Document
from docx import Document
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import os
#import os.path
#import collections
import sqlite3
def init():
   from email._header_value_parser import TokenList
   isProxyNeeded=input("proxy required?(yes/no):")
   print(isProxyNeeded);
   if isProxyNeeded=='yes':
       proxyDetails=input("provide proxy details:")
       nltk.set_proxy(proxyDetails)
   nltk.download('stopwords',quiet=True)
   nltk.download('wordnet', quiet=True) 
def buildIndex():
    final_lemmaList=[]
    final_filtered_sentence=[]
    dataFilePath=input("Data File path: ")#(make sure it ends with slash(\):")
    print("dataFilePath = ",dataFilePath)
    for dataFileName in os.listdir(dataFilePath):#takes all files inside the dataset\ directory
        print("dataFileName=",dataFileName)#ARG ESSAY1.DOCX
        document=Document(dataFilePath+dataFileName)#TAKES EACH DOCUMENT IN THE DIRECTORY, RETURNS A DOC OBJECT
        #print("document",document)
        finalList=[]
        uniqueWordList=[]
        #flag=0
        for p in document.paragraphs:
            #print("p.text->",p.text)#PRINTS WHOLE PARAGRAPH 
            listT=p.text.split()#paragraph words in listT
            for word in listT:
                if word not in uniqueWordList:
                    uniqueWordList.append(word)
                #finalList.append(word)
        #ps=PorterStemmer()
        #uniqueWordList=finalList
        #for word in finalList:
        #    if word not in uniqueWordList:
        #        uniqueWordList.append(word)



        stop_words=list(stopwords.words('english'))
        filtered_sentence=[w for w in uniqueWordList if not w in stop_words] #for each document
        #print("filtered_sentence",filtered_sentence)
        #final_filtered_sentence.append(filtered_sentence)
        # Lemmatization
        #lemmatizer = WordNetLemmatizer()
        lemmaList=[] #LEMMALIST = LIST OF WORDS FOR EACH DOCUMENT 
        for word in filtered_sentence:
            lemmaList.append(WordNetLemmatizer().lemmatize(word))
        print("len(lemmaList) = ",len(lemmaList))
        
        #final_lemmaList.append(WordNetLemmatizer().lemmatize(word))
        #print('*************** After lemmatization**********')
        #print(lemmaList)
        #FINAL_LEMMALIST ---> [[DOC1 LEMMA LIST],[DOC2 LEMMA LIST],[DOC1 LEMMA LIST]]   
        final_lemmaList.append(lemmaList)
        print("len(final_lemmaList) = ",len(final_lemmaList))
        
        #print("final_lemmaList",final_lemmaList)
    #print(final_filtered_sentence)
    #print(final_lemmaList)
    index=dict();
    documentCount=0;
    for tokenList in final_lemmaList:
        documentCount=documentCount+1
        #print("tokenlist=",tokenList)
        for term in tokenList:
            docList=["Doc"+str(documentCount)+".docx"]
            if term in index.keys():
                if 'Doc'+str(documentCount)+".docx" not in index.get(term):
                    docList.extend(index.get(term));
                    index.update({term: docList})
                        
            else:
                index[term]=docList
                #index.update({term:docList})
    print("index->",index)
    return index
def prepareDB():
    try:
        os.makedirs("db1")
    except:
        print("Folder Already exists")    
    conn = sqlite3.connect('db1\\index1.db');
    c = conn.cursor()
    # Create index table
    c.execute("drop TABLE if exists index_store")
    c.execute('''CREATE TABLE index_store
             (term text, df text, documents text)''')
    conn.close()
def storeIndexInDB():
    prepareDB()
    conn = sqlite3.connect('db1\\index1.db');
    c = conn.cursor()
    index=buildIndex()
    print("Creating index for following terms:")
    print("="*20)
    for term in sorted(index):
        #c.execute("insert into index_store values('"+"anushka"+"','"+"1"+"','"+"aaaaa.docx"+"')")
        print("["+term+":"+str(len(index[term]))+"]->"+str(sorted(index[term])))
        #c.execute("INSERT INTO index_store VALUES (\""+term+"\",\""+str(len(index[term]))+"\",\""+str(sorted(index[term]))+"\")")
        c.execute("INSERT INTO index_store VALUES ('"+term+"','"+str(len(index[term]))+"',\""+str(sorted(index[term]))+"\")")
        conn.commit()
        #print("committing")
        
#init()        
storeIndexInDB()
    



