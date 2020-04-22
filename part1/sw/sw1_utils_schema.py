import os
from whoosh.index import create_in
from whoosh import index
from bs4 import BeautifulSoup

def Empty_Schema(dataset,analyzer,schema,part1_path):
    '''
    Create empty schema and directory for saving it.
    input: dataset = dataset name str, analyzer = analyzer's name str, and schema
    output: directory_containing_the_index str
    '''
    # Create directory to save empty-Index
    directory_containing_the_index = part1_path + '/directory_index_' + dataset + '_' + str(analyzer)
    try:
        os.mkdir(directory_containing_the_index)
    except OSError:
        print ("Creation of the directory %s failed" % directory_containing_the_index)
    else:
        print ("Successfully created the directory %s " % directory_containing_the_index)
    ### Create an empty-Index according to the defined Schema
    create_in(directory_containing_the_index, schema)

    return directory_containing_the_index


def Fill_Empty_Schema(dataset,dir_idx,n,part1_path):
    '''
    Fill empty schema through parsing documents
    Input: dataset = dataset name str, dir_idx = directory_containing_the_index str,
    n = number of documents in dataset
    '''
    directory_containing_the_documents = part1_path + '/' + dataset + '/DOCUMENTS/'
    ix = index.open_dir(dir_idx) # open index
    writer = ix.writer(procs=4, limitmb=999)
    for i in range(1,n+1):
        # open and read each file of dataset
        with open(directory_containing_the_documents + '______'+str(i) + '.html', "r") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml') # a BeautifulSoup object is created
            body_ = soup.body.get_text().replace('\n',' ').strip()
            # use different filds for each dataset
            if dataset == 'Cranfield_DATASET':
                title_ = soup.title.get_text().replace('\n',' ').strip()
                # add document to the index
                writer.add_document(id=str(i), title=title_, content=body_)
            elif dataset == 'Time_DATASET':
                # add document to the index
                writer.add_document(id=str(i), content=body_)
    print("Commiting to  %s " % dir_idx)
    writer.commit()