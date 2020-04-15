from docx import Document
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import PyPDF2 
import nltk
import os
import sqlite3
import re

def buildIndex():
    final_lemmaList=[]
    final_filtered_sentence=[]
    index=dict();
    dataFilePath=input("Data File path: ")#(make sure it ends with slash(\):")
    #print("dataFilePath = ",dataFilePath)
    for dataFileName in os.listdir(dataFilePath):#takes all files inside the dataset\ directory
        #print("dataFileName=",dataFileName)#ARG ESSAY1.DOCX
        pattern='\S+\.(\S+)'
        file_type=re.findall(pattern,dataFileName)
        if(file_type[0] == 'docx'):
            #print("file_type[0]=",file_type[0]);
            #print("(inside the if loop)dataFileName=",dataFileName)
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



            
        if(file_type[0] == 'pdf'):
            pdfFileObj = open(dataFilePath+dataFileName, 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
            num_pages = pdfReader.numPages
            count = 0
            text = ""
            #The while loop will read each page
            while count < num_pages:
                pageObj = pdfReader.getPage(count)
                count +=1
                text += pageObj.extractText()
            uniqueWordList = text.split()
            #print("uniqueWordList = ", uniqueWordList)
        
        if( file_type[0] == 'c' or file_type[0] == 'cpp'):
            #print("dataFileName = ",dataFileName)
            file = open(dataFilePath+dataFileName, "r") 
            list_of_all_words = file.read().split()
            uniqueWordList=[]
            for word in list_of_all_words:
                if word not in uniqueWordList:
                    uniqueWordList.append(word)
            #print(list( file.read().split() ))

        #print("uniqueWordList = ", uniqueWordList)
        stop_words=list(stopwords.words('english'))
        filtered_sentence=[w for w in uniqueWordList if not w in stop_words] #for each document
        #print("filtered_sentence",filtered_sentence)
            #final_filtered_sentence.append(filtered_sentence)
            # Lemmatization
            #lemmatizer = WordNetLemmatizer()
        lemmaList=[] #LEMMALIST = LIST OF WORDS FOR EACH DOCUMENT 
        for word in filtered_sentence:
            lemmaList.append(WordNetLemmatizer().lemmatize(word))
        #print("lemmaList = ",(lemmaList))
            
            #final_lemmaList.append(WordNetLemmatizer().lemmatize(word))
            #print('*************** After lemmatization**********')
            #print(lemmaList)
        final_lemmaList=[]
        for word in lemmaList:
            if word not in final_lemmaList:
                final_lemmaList.append(word)
        #print("final_lemmaList -> ", final_lemmaList)
            
        for tokenList in final_lemmaList:
                    #print("tokenlist=",tokenList)
            doclist = dataFileName
            if tokenList in index:
                index[tokenList].append(dataFileName)
                                    
            else:
                index[tokenList]=[]
                index[tokenList].append(dataFileName)
                        #index.update({tokenlist:dataFileName})
        #print("index->",index)
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
        

storeIndexInDB()
    
#uniqueWordList -> all the words unique to the file in a list
#filtered_sentence -> removed all stop words from uniqueWordList for that document
#lemma list -> lemmatize all words in filtered_sentence for that document
#final_lemmaList -> remove any duplicacy if any in lemma list
#index -> predefined dict in which new words are appended and documents are appended to the already present word


