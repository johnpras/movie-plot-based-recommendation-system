import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda')
df = pd.read_csv('movies_metadata2.csv',dtype='unicode')
df['overview'] = df['overview'].fillna('')

corpus = df['overview'].to_list()

query = ['''John Wick comes off his meds to track down the bounders that killed his dog and made off with his self-respect''']

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
    print("top 5 suggested movies based on the description:\n")
    for k in sorted_listtemp[:5]:           
        for row in df.itertuples():            
            if row.overview == k[1]:
                print(row.title, "->", k[2])
                final_list.append(row.title)
    return final_list

returntop5()
