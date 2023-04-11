import pandas as pd


### Create relevant sample from riksdagsanföranden
### Data collected using https://github.com/kb-labb/riksdagen_anforanden

data = "/home/gilleti/Documents/riksdagen_anforanden/data/df_anforanden_metadata.parquet"


df = pd.read_parquet(data, engine='fastparquet')
df = df[df["anforandetext"].notna()]
#df = df[df["anforandetext"].str.contains('grundskol|faktakunskap')] # OR
df = df[(df['anforandetext'].str.contains('grundskol')) & (df['anforandetext'].str.contains('idrott'))] # AND
df = df[~df['anforandetext'].str.contains('samverk')] # NOT

with pd.option_context('display.max_colwidth', None):
  print(df["anforandetext"])



