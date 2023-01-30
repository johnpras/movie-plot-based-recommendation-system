#Content-based recommenders: suggest similar items based on a the plot you want to see.
#built a model that will recommend movies based on the plot we want
#copmare the semantic meaning of the descriptions using cosine similarity score

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
#import torch
import sys
import json

filename = sys.argv[1]
with open(filename, encoding="utf8") as myfile:
    text="".join(line.rstrip() for line in myfile)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda')
df = pd.read_csv('movies_metadata2.csv',dtype='unicode')
df['overview'] = df['overview'].fillna('')

corpus = df['overview'].to_list()

query = [text]

embeddings1 = model.encode(query)
#embeddings2 = model.encode(corpus)
#np.save('embeddings2.npy', embeddings2)

embeddings2 = np.load('embeddings2.npy')
cosine_scores = util.cos_sim(embeddings1, embeddings2)
cosine_scores_list = cosine_scores.tolist()

listtemp=[]
for i in range(len(corpus)):
    temp = []
    temp.append(query[0])
    temp.append(corpus[i])
    temp.append(float("%.4f" % cosine_scores[0][i]))
    listtemp.append(temp)

sorted_listtemp = sorted(listtemp, key=lambda x: float(x[2]))
sorted_listtemp.reverse()

def returntop5():
    final_list=[]
    #print("top 5 suggested movies based on the description:\n")
    for k in sorted_listtemp[:5]:           
        for row in df.itertuples():            
            if row.overview == k[1]:
                #print(row.title, "->", k[2])
                final_list.append(row.title)
    return final_list

res = {"results": returntop5()}
data = json.dumps(returntop5())
print(data)
