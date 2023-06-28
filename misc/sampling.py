import pandas as pd

# This script consists of sampling criterion to catch relevant school material from the political dataset.
# Sampling strategy developed by Ema Demir.
# Ultimately, we ended up not using it because of data scarcity but they could come in handy later.


data = "motioner_2014_2021.parquet"
df = pd.read_parquet(data, engine='fastparquet')

df = df[df["text"].notna()]
df = df[df["text"].str.contains('grundskol|lärar|skol')] # OR
df = df[(df['text'].str.contains(' skol')) & (df['text'].str.contains('universit'))] 
df = df[df.text.str.count("lärar|grundskol| skol") > 1]
df = df[~df['text'].str.contains('bistånd|skolreaktor')]
with pd.option_context('display.max_colwidth', None):
  print(df["text"])
