import sw1_utils_schema
import sw1_utils_query
import sw1_utils_metrics
import sw1_utils_plot

from whoosh.analysis import SimpleAnalyzer, StandardAnalyzer, LanguageAnalyzer
from whoosh.fields import *
from whoosh import scoring
from whoosh import index
import numpy as np


# reading and storing Groung Truth for both datasets
directory_containing_Cran_GT = '../Cranfield_DATASET/cran_Ground_Truth.tsv'
directory_containing_Time_GT = '../Time_DATASET/time_Ground_Truth.tsv'

Cran_GT = sw1_utils_query.GT_Q_read(directory_containing_Cran_GT,True)
Time_GT = sw1_utils_query.GT_Q_read(directory_containing_Time_GT,True)

# reading and storing queries for both datasets
directory_containing_Cran_Q = '../Cranfield_DATASET/cran_Queries.tsv'
directory_containing_Time_Q = '../Time_DATASET/time_Queries.tsv'

Cran_Q = sw1_utils_query.GT_Q_read(directory_containing_Cran_Q,False)
Time_Q = sw1_utils_query.GT_Q_read(directory_containing_Time_Q,False)



###
### Define a Text-Analyzer 
###
selected_analyzer = [SimpleAnalyzer(), StandardAnalyzer(), LanguageAnalyzer('en')]
analyzer_names = ['Simple', 'Standard', 'Language']
###
### Create a Schema 
###
datasets = ['Cranfield_DATASET', 'Time_DATASET']
datasets_len = [1400, 423]
dir_idx_list = [] # list to save directories for indexes

# for each of the datasets and for each of the analyzers create empty index
# based on schema in the separate directory. 
# Then fill empty index through parsing dataset. Save directory into list.
for idx in range(len(datasets)):
    if datasets[idx] == 'Cranfield_DATASET':
        for i in range(len(selected_analyzer)):
            analyzer_ = selected_analyzer[i]
            schema = Schema(id=ID(stored=True),title=TEXT(stored=True),\
                            content=TEXT(stored=True,analyzer=analyzer_))
            directory_containing_the_index = sw1_utils_schema.Empty_Schema(datasets[idx],\
                                                          analyzer_names[i],schema)
            
            # filling empty-Index
            sw1_utils_schema.Fill_Empty_Schema(datasets[idx],directory_containing_the_index,\
                              datasets_len[idx])
            dir_idx_list.append(directory_containing_the_index)

    elif datasets[idx] == 'Time_DATASET':
        for i in range(len(selected_analyzer)):
            analyzer_ = selected_analyzer[i]
            schema = Schema(id=ID(stored=True),\
                            content=TEXT(stored=True,analyzer=analyzer_))
            directory_containing_the_index = sw1_utils_schema.Empty_Schema(datasets[idx],\
                                                          analyzer_names[i],schema)
            sw1_utils_schema.Fill_Empty_Schema(datasets[idx],directory_containing_the_index,\
                              datasets_len[idx])
            dir_idx_list.append(directory_containing_the_index)
      
###       
### Open the Index
###
            
# for each of the datasets open index. And for each of the scoring functions
# create a searcher, process queries and save retrieved results into Q_results.
# Compute the MRR value for each of the search engine configurations
Q_Res = []
config_names = []
# scoring functions
sc_functions = [scoring.Frequency(),scoring.TF_IDF(),scoring.BM25F()]
sc_fun_name = ['Frequency','TF_IDF','BM25F']

for idx in range(len(datasets)):
    max_number_of_results = datasets_len[idx]
    print('Search Engine Configuration' + "\t" + "\t" + "\t" + 'MRR')
    if datasets[idx] == 'Cranfield_DATASET':
        Q_dict = Cran_Q
        GT_dict = Cran_GT
        for elem in dir_idx_list[:3]:            
            directory_containing_the_index = elem
            ix = index.open_dir(directory_containing_the_index)
            ### Select a Scoring-Function
            for s in range(len(sc_functions)):
                scoring_function = sc_functions[s]
                ### Create a Searcher for the Index with the selected Scoring-Function 
                searcher = ix.searcher(weighting=scoring_function)
                ### Process query
                parsed_queries_list = sw1_utils_query.Q_process(Q_dict,ix,True)
                ### perform a Search :)
                Q_results = sw1_utils_query.perform_search(Q_dict,searcher,parsed_queries_list,max_number_of_results)
                searcher.close()
                MRR_val = sw1_utils_metrics.MRR(Q_results,GT_dict)
                Q_Res.append(Q_results)
                config_name = ' '.join(elem.split('_')[-3:]) + ' Analyzer ' + sc_fun_name[s]
                config_names.append(config_name)
                print(config_name, MRR_val, '\n')

    elif datasets[idx] == 'Time_DATASET':
        Q_dict = Time_Q
        GT_dict = Time_GT
        for elem in dir_idx_list[3:]:
            directory_containing_the_index = elem
            ix = index.open_dir(directory_containing_the_index)
            ### Select a Scoring-Function
            for s in range(len(sc_functions)):
                scoring_function = sc_functions[s]
                ### Create a Searcher for the Index with the selected Scoring-Function 
                searcher = ix.searcher(weighting=scoring_function)
                ### Process query
                parsed_queries_list = sw1_utils_query.Q_process(Q_dict,ix,False)
                ### perform a Search :)
                Q_results = sw1_utils_query.perform_search(Q_dict,searcher,parsed_queries_list,max_number_of_results)
                searcher.close()
                MRR_val = sw1_utils_metrics.MRR(Q_results,GT_dict)
                Q_Res.append(Q_results)
                config_name = ' '.join(elem.split('_')[-3:]) + ' Analyzer ' + sc_fun_name[s]
                config_names.append(config_name)
                print(config_name, MRR_val, '\n')
###       
### R_precision
###                
# pick the best configurations by MRR value for each of the datasets
indexes_of_the_best_config = [[5,8,2,7,4],[17,14,11,16,13]]
# for each of the best configuraions compute and print R-precision distribution           
for idx in range(len(datasets)):
    if datasets[idx] == 'Cranfield_DATASET':
        GT_dict = Cran_GT
    else:
        GT_dict = Time_GT
       
    for val in indexes_of_the_best_config[idx]:
        print(config_names[val])
        #R_precision
        R_Precision_Q_val = sw1_utils_metrics.R_Precision(Q_Res[val],GT_dict)
        sw1_utils_metrics.R_Prec_print(R_Precision_Q_val)

###       
### Precision at K and nDCG at k + plots
### 
# for each value of k and each best configuration 
# compute and plot average Precision at K and average nDCG at k  
k = [1,3,5,10]

for idx in range(len(datasets)):
    Y_pk = []
    Y_nDCGk = []
    
    if datasets[idx] == 'Cranfield_DATASET':
        GT_dict = Cran_GT
    else:
        GT_dict = Time_GT
    for n in indexes_of_the_best_config[idx]:
        y_pk = []
        y_nDCGk = []
        for elem in k:
            Pk_Q_val = sw1_utils_metrics.PrecK(Q_Res[n],GT_dict,elem)
            nDCGk_Q_val = sw1_utils_metrics.nDCGk(Q_Res[n],GT_dict,elem)
            avg_prec_k = np.average(list(Pk_Q_val.values()))
            avg_nDCGk = np.average(list(nDCGk_Q_val.values()))
            y_pk.append(avg_prec_k)
            y_nDCGk.append(avg_nDCGk)
        Y_pk.append(y_pk)
        Y_nDCGk.append(y_nDCGk)
    sw1_utils_plot.plot_(k,config_names,indexes_of_the_best_config[idx],Y_pk,datasets[idx],True)
    print()
    sw1_utils_plot.plot_(k,config_names,indexes_of_the_best_config[idx],Y_nDCGk,datasets[idx],False)

