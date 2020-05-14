from whoosh.qparser import MultifieldParser
from whoosh.qparser import QueryParser

def GT_Q_read(directory_containing_the_file,GT):
    ''' Create dictionary from query Ground Truth file
    '''
    dict_ = {}
    with open(directory_containing_the_file,"r") as f:
        next(f) # skip header
        for line in f:
            key = line.split()[0]
            if GT == True:
                val = line.split()[1]
            elif GT == False:
                val = ' '.join(line.split()[1:])
                
            if key not in dict_:
                dict_[key] = [val]
            elif key in dict_:
                dict_[key].append(val)
    return dict_

def Q_process(Q_dict,ix,Cran):
    ''' Query parser using defined schema
    '''
    parsed_queries_list = []
    for elem in list(Q_dict.keys()):
        input_query = Q_dict[elem][0]

        if Cran == True:            
            qp = MultifieldParser(["title", "content"], ix.schema)
        elif Cran == False:
            qp = QueryParser("content", ix.schema)
        parsed_query = qp.parse(input_query)  # parsing the query
        parsed_queries_list.append(parsed_query)
    return parsed_queries_list

def perform_search(Q_dict,searcher,Q_list_parsed,max_n):
    ''' Perform search for a given query
    Output: list, where each element is tuple of query_id and list of ranked retrieved documents = q_results_list
    q_results_list is a list of tuples, where each tuple consists of rank of retrieved document and document_id
    '''
    q_results_list = []
    Q_results = []
    for i in range(len(Q_dict)):
        results = searcher.search(Q_list_parsed[i], limit=max_n)
        q_results_list = []
        for hit in results:
            q_results_list.append((str(hit.rank + 1),hit['id']))
        Q_results.append((list(Q_dict.keys())[i],q_results_list))
    return Q_results
