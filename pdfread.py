# importing required modules 
import PyPDF2 
from docx import Document
#from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# creating a pdf file object 
s='dataset1/cglab.pdf'
pdfFileObj = open(s, 'rb') 

# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

# printing number of pages in pdf file 
#print(pdfReader.numPages) 

num_pages = pdfReader.numPages
count = 0
text = ""
#The while loop will read each page
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()
# creating a page object 
#pageObj = pdfReader.getPage(0) 
tokens = text.split()
#we'll create a new list which contains punctuation we wish to clean
#punctuations = ['(',')',';',':','[',']',',']
#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('english')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
uniqueWordsList = [word for word in tokens if not word in stop_words]
# extracting text from page 
#print(pageObj.extractText()) 
print(tokens)
print()
print(uniqueWordsList)
# closing the pdf file object 
#pdfFileObj.close() 
