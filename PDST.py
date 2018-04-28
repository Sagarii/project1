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
def get_page_content(fileName):
    ### 'fileName' is the pdf file name. 
    fileName = './uploads/'+fileName
    stopWords = set(stopwords.words("english"))
    # creating a pdf file object
    pdfReport = open(fileName, 'rb') #set pdf path

    # creating a pdf reader object
    global pdfReader 
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

    if words[0] == 'Contents':
        words.insert(1,str(content_page_num))

    content = []
    for w in words:
        if re.match('[0-9]+',w):
            sp = re.split('([0-9]+)',w)
            content = content + sp
        else:
            content.append(w)

    content_list = list(filter(None,content))

    string = ''
    formated_list = []
    for w in content_list:
        if re.match(r'[0-9]+',w):
            formated_list.append(string.strip())
            string = ''
            formated_list.append(w)
        else:
            string += w+' '

    return formated_list

# When we give file content list and page we need, this method return page number. 
def get_data_page_number(content_list,content_we_need):
    content_page_num = content_list[content_list.index('Contents') + 1] #Content page number
    page_num = content_list[content_list.index(content_we_need) + 1] #Data page number
    
    return int(page_num) + int(content_page_num)

# When we give pdf page number and new file name this method can extract it to new seperate pdf file 
def write_new_pdf(extracting_page,file_name):
    pageToWrite = pdfReader.getPage(extracting_page)

    pdfWriter = PyPDF2.PdfFileWriter()
    pdfWriter.addPage(pageToWrite)

    newPdfName = file_name+'.pdf'
    outputStream = open('./pdf/'+newPdfName,'wb')
    pdfWriter.write(outputStream)

    return 1


def all_in_one(report_file_name):
    
    list = get_page_content(report_file_name) #Step 1
    
    tables_we_neew = ['Statement of Financial Position','Income Statement', 'Statement of Other Comprehensive Income', 'Statement of Changes in Equity', 'Statement of Cash Flow', 'Five Year Summary']
    content_we_need = 'Statement of Financial Position'
    
    page_num = get_data_page_number(list,content_we_need) #Step 2

    c = write_new_pdf(page_num,content_we_need)

    if c:
        print('Done')
    else:
        print('Sorry')


all_in_one('hotels and travels.pdf')


