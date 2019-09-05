import codecs
import json
import pandas as pd

with codecs.open('merged.json', 'r', 'utf-8') as f:
    df_merged = pd.DataFrame(json.loads(f.read()))

def float_from_sales(sales_datum):
    if isinstance(sales_datum, float):
        return sales_datum
    else:
        try:
            return float(sales_datum[:-1])
        except:
            return 0.0

def float_convert_df(df):
    df['eu_sales'] = float_from_sales(df['eu_sales'])
    df['na_sales'] = float_from_sales(df['na_sales'])
    df['ja_sales'] = float_from_sales(df['ja_sales'])
    df['rest_sales'] = float_from_sales(df['rest_sales'])
    df['global_sales'] = float_from_sales(df['global_sales'])
    return df

df_new = df_merged.apply(float_convert_df,1)

df_new.to_json('floated.json')
