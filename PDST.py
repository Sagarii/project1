# ------------------------
# Python Data Scraping Tool
# PDST.py contains required function for find realtive informative pages

import PyPDF2
from nltk import  sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from tabula import read_pdf,convert_into
import re
from fuzzy_match import is_ci_token_stopword_match


# This method use when the content we need not listed on Contents list
# Here read whole document and check for pages
def get_tables_from_page(content_we_need):
    
    page_number = 0
    
    for i in range(0,pdfReader.numPages):
        pageObg = pdfReader.getPage(i)
        pdf_text = pageObg.extractText()
        text_sentense = sent_tokenize(pdf_text)
        
        for sen in text_sentense:

            sn = sen.split('\n')
            for s in sn:
                result = re.findall(r'('+content_we_need+')', s, re.IGNORECASE)
                if(result):
                    # Now check for is this page contain specific words found on 
                    # each tables
                    # TODO
                    print(s)

                
        else:
            continue
        break

    return page_number


# When upload new pdf file, first we can get page content from content page
# This method return list of content page in this format 
# > ['Title',01,'title2',02,'title',03...]
def get_page_content(fileName):

    global pdfReader
    global content_page_num

    ### 'fileName' is the pdf file name. 
    fileName = './uploads/'+fileName
    stopWords = set(stopwords.words("english"))
    # creating a pdf file object
    pdfReport = open(fileName, 'rb') #set pdf path

    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfReport)
    #without looking for whole pdf, just look for first 10 pages
    #pdfReader.numPages <- removed this
    for i in range(0,pdfReader.numPages):

        pageObj = pdfReader.getPage(i)
        pdf_text = pageObj.extractText()
        text_sentense = sent_tokenize(pdf_text)
    
        for sen in text_sentense:
            result = re.findall(r'(Content)', sen, re.IGNORECASE)
            if(result):
                content_page_num = i
                break
        else:
            continue
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
    # content_page_num = content_list[content_list.index('Contents') + 1] #Content page number
    req_page_num = ""
    
    for list_item in content_list:
        if len(list_item) < 5:
            continue

        if '-' in list_item:
            list_item_temp = list_item.split('-')[0]
            if is_ci_token_stopword_match(content_we_need,list_item_temp):
                req_page_num = content_list[content_list.index(list_item) + 1] #Data page number
        else:
            if is_ci_token_stopword_match(content_we_need,list_item):
                req_page_num = content_list[content_list.index(list_item) + 1] #Data page number
            else:
                updated_content = 'Consolidated ' + content_we_need
                if is_ci_token_stopword_match(updated_content,list_item ):
                    req_page_num = content_list[content_list.index(list_item) + 1]

    if req_page_num != "":
        return int(req_page_num) + content_page_num
    else: 
        return 0

# When we give pdf page number and new file name this method can extract it to new seperate pdf file 
def write_new_pdf(extracting_page,file_name):
    pageToWrite = pdfReader.getPage(extracting_page)
    
    pdf_text = pageToWrite.extractText()
    text_sentense = sent_tokenize(pdf_text)
    file_content = file_name.split('-')[1]
    is_correct = False
    for sen in text_sentense:
        # print(sen)
        result = re.findall(r'('+file_content+')', sen, re.IGNORECASE)
        if(result):
            is_correct = True

    if(is_correct):
        pdfWriter = PyPDF2.PdfFileWriter()
        pdfWriter.addPage(pageToWrite)

        newPdfName = file_name+'.pdf'
        outputStream = open('./pdf/'+newPdfName,'wb')
        pdfWriter.write(outputStream)

        return 1
    else:
        if (extracting_page < 0):
            return 0
        
        return write_new_pdf(extracting_page-1, file_name)


def execute(report_file_name):
    
    clist = get_page_content(report_file_name) #Step 1
        
    tables_we_need = ['Statement of Financial Position', 'Income Statement', 'Statement of Other Comprehensive Income', 'Statement of Cash Flow','Cash Flow Statement', 'Five Year Summary','Ten Year Summary']
    list_of_pdf = []
    for content_we_need in tables_we_need:
        page_num = get_data_page_number(clist,content_we_need) #Step 2
        if(page_num):
            new_pdf_name = report_file_name.split('.')[0]+'-'+content_we_need
        
            c = write_new_pdf(page_num,new_pdf_name) #Step 3

            if c:
                print(content_we_need+' done.')
                list_of_pdf.append(new_pdf_name+'.pdf')
            else:
                print('Error on extracting page '+ content_we_need)
        else:
            print('Can\'t found content for '+ content_we_need)

    return list_of_pdf


# aia_list = ['aia-Statement of Financial Position.pdf', 'aia-Income Statement.pdf', 'aia-Statement of Other Comprehensive Income.pdf', 'aia-Statement of Cash Flow.pdf', 'aia-Five Year Summary.pdf']