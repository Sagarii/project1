# ------------------------
# Python Data Scraping Tool
# PDST.py contains required function for find realtive informative pages

import PyPDF2
from nltk import  sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from tabula import read_pdf,convert_into
import re

# When upload new pdf file, first we can get page content from content page
# This method return list of content page in this format 
# > ['Title',01,'title2',02,'title',03...]
def getPageContent(fileName):
    ### 'fileName' is the pdf file name. 
    fileName = './uploads/'+fileName
    stopWords = set(stopwords.words("english"))
    # creating a pdf file object
    pdfReport = open(fileName, 'rb') #set pdf path

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfReport)

    for i in range(0,pdfReader.numPages):

        pageObj = pdfReader.getPage(i)
        pdf_text = pageObj.extractText()
        text_sentense = sent_tokenize(pdf_text)

        for sen in text_sentense:
            result = re.findall(r'(Contents)', sen)
            if(result):
                content_page_num = i
                break

    pageObj = pdfReader.getPage(content_page_num)
    select_page_text = pageObj.extractText()
    words = word_tokenize(select_page_text)

    content = []
    for w in words:
        if re.match('[0-9]+',w):
            sp = re.split('([0-9]+)',w)
            content = content + sp
        else:
            content.append(w)

    content_list = list(filter(None,content))

    str = ''
    formated_list = []
    for w in content_list:
        if re.match(r'[0-9]+',w):
            formated_list.append(str.strip())
            str = ''
            formated_list.append(w)
        else:
            str += w+' '

    return formated_list

# When we give file content list and page we need, this method return page number. 
def getDataPageNumber(content_list,content_we_need):
    table_page_num = content_list[content_list.index(content_we_need) + 1]
    
    return table_page_num



print(getPageContent('hotels and travels.pdf'))