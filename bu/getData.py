#! /usr/bin/env python3

import numpy as np
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text

passw = '12345'
engine=create_engine(f'postgresql://team4:{passw}@ds4a-instance.c5zadjwjarvt.sa-east-1.rds.amazonaws.com/ds4afp', max_overflow=20)
def runQuery(sql):
    result = engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

#Get data from DB
df = runQuery(
"""SELECT file_year AS year, id_birth ,resultado_emb, count(*) FROM eevv
GROUP BY file_year, resultado_emb, id_birth
""")

df['id_birth'] = df['id_birth'].apply(lambda x: str(x).zfill(5))

#GeoData: this contains names and codes
geo = gpd.read_file('../Data/GeoData/Municip.json')

#Create name column
df['mpio_name'] = df['id_birth'].copy().replace(geo['MPIO_CCNCT'].to_list(),geo['MPIO_CNMBR'].to_list())

df.to_csv('year_outcome_count.csv',index=False) #Save for later use 