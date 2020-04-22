import numpy as np
import matplotlib.pyplot as plt

def plot_(k,names,ids,Y,ds,flag):
    
    nm = np.take(names, ids)

    plt.figure(figsize=(10,8))
    plt.plot(k, Y[0],color='green', marker='o', linestyle='-',linewidth=2, markersize=10)
    plt.plot(k, Y[1],color='red', marker='o', linestyle='-',linewidth=2, markersize=10)
    plt.plot(k, Y[2],color='blue', marker='o', linestyle='-',linewidth=2, markersize=10)
    plt.plot(k, Y[3],color='orange', marker='o', linestyle='-',linewidth=2, markersize=10)
    plt.plot(k, Y[4],color='pink', marker='o', linestyle='-',linewidth=2, markersize=10)

    plt.legend(nm)
    plt.xlabel('k value',fontsize=15)
    if flag:
        plt.ylabel(ds + '  average P@k',fontsize=15)
    elif not flag:
        plt.ylabel(ds + '  average nDCG@k',fontsize=15)