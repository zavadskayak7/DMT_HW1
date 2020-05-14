import math
import numpy as np
import pandas as pd

def nDCGk(Q_results,GT,k):
    IDGC = sum([1/(math.log(1+kk,2)) for kk in range(1,k+1)])
    nDCGk_Q_val = {}
    
    for i in range(len(Q_results)):
        
        q_idx = Q_results[i][0]
        results = Q_results[i][1] # list of tuples
        if q_idx in list(GT.keys()): # GT exist
            retrieved_docs = Q_result_list(results, k)
            Total_DCG = 0
            for idx in range(k):
                if retrieved_docs[idx] in GT[q_idx]:
                    nom = 1
                else:
                    nom = 0
                DCG_part = nom / (math.log(idx+1+1,2))
                Total_DCG += DCG_part
            nDCGk = Total_DCG / IDGC
            nDCGk_Q_val[q_idx] = nDCGk
        else: # GT does not exist
            continue
    return nDCGk_Q_val


def PrecK(Q_results,GT,k):
    ''' Precision at k
    '''
    Pk_Q_val = {}
    for i in range(len(Q_results)):
        q_idx = Q_results[i][0]
        results = Q_results[i][1] # list of tuples (rank,doc_id)
        num_of_relevant_docs = 0
        if q_idx in GT.keys(): # GT exist
            retrieved_docs = Q_result_list(results, k)
            #num_of_relevant_docs = 0
            for idx in range(len(retrieved_docs)):
                if retrieved_docs[idx] in GT[q_idx]:
                    num_of_relevant_docs += 1
                else:
                    continue
            Pk_q = num_of_relevant_docs / min(k,len(GT[q_idx]))
            Pk_Q_val[q_idx] = Pk_q
        else: # GT does not exist
            continue
    return Pk_Q_val

def R_Precision(Q_results,GT):
    R_Precision_Q_val = {}
    for i in range(len(Q_results)):
        q_idx = Q_results[i][0]
        results = Q_results[i][1] # list of tuples
        if q_idx in GT.keys(): # GT exist
            retrieved_docs = Q_result_list(results,len(GT[q_idx]))
            num_of_relevant_docs = 0
            for doc in retrieved_docs:
                if doc in GT[q_idx]:
                    num_of_relevant_docs += 1
                else:
                    continue
            R_Prec_q = num_of_relevant_docs / len(GT[q_idx])
            R_Precision_Q_val[q_idx] = R_Prec_q
        else: # GT does not exist
            continue
    return R_Precision_Q_val

def R_Prec_print(R_Precision_Q_val):
    lst = list(R_Precision_Q_val.values())
    print('R-Precision distribution table')
    stats = ['MEAN',"MIN",'1_QR','MEDIAN','3_QR','MAX']
    vals = [round(np.mean(lst),3), round(np.min(lst),3), round(np.percentile(lst,25),3), \
    round(np.percentile(lst,50),3), round(np.percentile(lst,75),3), round(np.max(lst),3)]
    data_tuples = list(zip(stats,vals))
    df = pd.DataFrame(data_tuples, columns=['Statistic','Value'],index=stats)
    df = df.drop(columns=['Statistic'])
    print(df.T)
    print()

def MRR(Q_results,GT):
    # in GT not all the queries are presented
    # so we compute MRR only for queries we have in GT
    # and number of queries in set are considered to be only those which in GT
    Q_n = 0
    ssum = 0
    for i in range(len(Q_results)):
        q_idx = Q_results[i][0]        
        results = Q_results[i][1] # list of tuples
        if q_idx in GT.keys():
            Q_n = Q_n + 1
            for j in range(len(results)):
                frac = 0
                if results[j][1] in set(GT[q_idx]):
                    frac = 1 / int(results[j][0])
                    ssum = ssum + frac
                    break
                else:
                    continue
        elif q_idx not in GT.keys():
            continue
    MRR = ssum / Q_n
    return MRR

def Q_result_list(results,k):
    ''' Returns list of document_ids of given lenght k
    '''
    res_list = []
    for e in range(k):
        res_list.append(results[e][1])
    return res_list