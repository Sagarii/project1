from tabula import read_pdf,convert_into
import json
import PDST


def getData(filename):
    list_of_file = PDST.execute(filename)
    # temp = ['hotels_and_travels-Statement of Financial Position.pdf', 'hotels_and_travels-Income Statement.pdf', 'hotels_and_travels-Statement of Cash Flow.pdf', 'hotels_and_travels-Five Year Summary.pdf']
    temp = ['hotels_and_travels-Statement of Financial Position.pdf', 'hotels_and_travels-Five Year Summary.pdf']

    json_obj = dict()
    for pdf_name in temp: #change 'temp' => 'list_of_file' TODO
        df = read_pdf("pdf/"+pdf_name)
        if df.empty == False:
            new_column_name = df.columns.values
            new_column_name[0] = 'value'
            df.columns = new_column_name

            my_key = pdf_name.split('.')[0].split('-')[1]
            json_obj[my_key] = json.loads(df.to_json(orient='records'))
            
            print(pdf_name + ' done.')
        else:
            print('Error on reading page '+pdf_name)

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
    

# def getContent():
#     df = read_new_pdf()    
#     return df.to_json(orient='records')


    # print(df.iloc[2].tolist())
    # print(df.iloc[0:4,1].tolist())
    # print(df.to_json(orient='index'))
    # print(df.shape)
    # print(df.columns[0])

# def getIndexs():
#     ls=new_column_name.tolist()
#     return json.dumps(ls)
