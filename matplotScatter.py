import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
"""
GoogleAPIから渡されたデータを散布図として表す
"""

def pickData(scores,key):
    datas=[]
    for object in scores:
        datas.append(object[key])
    return datas



def scatterPlot(scores):
    magnitude = pickData(scores,'magnitude')
    score = pickData(scores,'score')
    plt.scatter(score,magnitude)
    #plt.grid(True)
    plt.title('NegaPosi_Scatter')
    plt.xlabel('score')
    plt.ylabel('magnitude')
    plt.show()
    return 

# APIのスコアの散布図
def swarmPlot(scores):
    magnitude = pickData(scores,'magnitude')
    score = pickData(scores,'score')
    data = [score,magnitude]
    sns.swarmplot(x=score,y=magnitude)
    plt.show()
    return

# appレビューとAPIスコアの散布図
def correlationPlot(scores):
    score = pickData(scores,1)
    rate = pickData(scores,0)
    sns.swarmplot(x=rate,y=score)
    plt.show()
    return