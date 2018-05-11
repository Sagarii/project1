from tabula import read_pdf,convert_into
import json
import PDST


def getData(filename):
    list_of_file = PDST.execute(filename)
    json_obj = []
    for pdf_name in list_of_file:
        df = read_pdf("pdf/"+pdf_name)
        new_column_name = df.columns.values
        new_column_name[0] = 'value'
        df.columns = new_column_name
        json_obj.append(df.to_json(orient='records'))

    return json_obj

def read_new_pdf():
    # print(list_of_pdf)
    global df
    # list_of_pdf = ['acl-Statement of Financial Position.pdf', 'acl-Income Statement.pdf', 'acl-Statement of Other Comprehensive Income.pdf', 'acl-Statement of Cash Flow.pdf', 'acl-Five Year Summary.pdf']
    list_of_pdf = ['acl-Statement of Financial Position.pdf', 'acl-Five Year Summary.pdf']
    for pdf_name in list_of_pdf:
        df = read_pdf("pdf/"+pdf_name)
        new_column_name = df.columns.values
        new_column_name[0] = 'value'
        df.columns = new_column_name
        print('-'*100)
        print(pdf_name.split('.')[0])
        print('-'*100)
        # print(df)
        print(df.to_json(orient='records'))
    

def getContent():
    df = read_new_pdf()    
    return df.to_json(orient='records')


    # print(df.iloc[2].tolist())
    # print(df.iloc[0:4,1].tolist())
    # print(df.to_json(orient='index'))
    # print(df.shape)
    # print(df.columns[0])

def getIndexs():
    ls=new_column_name.tolist()
    return json.dumps(ls)
