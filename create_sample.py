import pandas as pd


### Create relevant sample from riksdagsanföranden
### Data collected using https://github.com/kb-labb/riksdagen_anforanden

#data = "/home/gilleti/Documents/riksdagen_anforanden/data/df_anforanden_metadata.parquet"
data = "motioner_2014_2021.parquet"


df = pd.read_parquet(data, engine='fastparquet')

print(df.columns)

df = df[df["text"].notna()]
#o_df = df[df["text"].str.contains('grundskol')] # OR

o_df = df[df["text"].str.contains('grundskol|lärar|skol')] # OR


print(type(o_df.text.str.count("lärar|grundskol|skol")))


o_df = o_df[(o_df['text'].str.contains(' skol')) & (df['text'].str.contains('universit'))] # AND

o_df = o_df[o_df.text.str.count("lärar|grundskol| skol") > 1]


o_df = o_df[~o_df['text'].str.contains('bistånd|skolreaktor')] # NOT

with pd.option_context('display.max_colwidth', None):
  print(o_df["text"])

print(len(df))
print(len(o_df))


#elev lärare kunskap
# skol grundskol

# universitet kan förekomma samtidigt som skol men ej ensamt eller med lärar


# small change to see if i managed to unfuck my bad commit
