import codecs
import json
import pandas as pd

df = pd.read_json('floated.json')

df_new = pd.DataFrame(columns=['basename', 'baseplatform', 'source', 'score'])

for rt in df.iterrows():
    # rt is a tuple (index, data)
    r = rt[1]
    for s in r['reviews']:
        try:
            new_row = {}
            new_row['basename'] = r['basename']
            new_row['baseplatform'] = r['baseplatform']
            new_row['source'] = s['source']
            new_row['score'] = s['score']
            index = pd.MultiIndex.from_product([[new_row['basename']], [new_row['baseplatform']], [new_row['source']]], names=['basename', 'baseplatform', 'source'])
            df_new_row = pd.DataFrame(new_row, index=index)
            df_new = pd.concat([df_new, df_new_row])
        except Exception as e:
            print(e)
    #print(df_new)

df_new = df_new.reset_index()
df_new.to_json('normalized_sources.json')
