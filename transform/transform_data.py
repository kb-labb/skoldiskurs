import stanza
import pandas as pd

### READ DATA

motioner_new = "/home/hilhag/prjs/skoldiskurs/data/motioner_2014_2023.parquet"
mot_new = pd.read_parquet(motioner_new)
mot_new = mot_new[mot_new['text'].notna()]
mot_new_df = mot_new[['text', 'datum']] # date var is "('year',)" # date is datum

anforanden_new = "/home/hilhag/prjs/skoldiskurs/data/anforanden_1993-2023.parquet"
anf_new = pd.read_parquet(anforanden_new)
anf_new = anf_new[anf_new['anforandetext'].notna()]
anf_new_df = anf_new[["anforandetext", "dok_datum"]] # date variable is dok_datum
anf_new_df = anf_new_df.rename(columns={"anforandetext": "text", "dok_datum": "datum"})

# Some super weird column formatting has accidentally happened in the older files
# The column names are as follows: ('dok_id',), ('text',), ('year',)
# TODO()
# Go back to parsing script and fix it
# List column command: print(anf_old.columns.tolist())
anforanden_old = "/home/hilhag/prjs/skoldiskurs/data/anforanden_1962-1992.parquet"
anf_old = pd.read_parquet(anforanden_old)
anf_old = anf_old[anf_old['(\'text\',)'].notna()]
anf_old_df = anf_old[['(\'text\',)', '(\'year\',)']]
anf_old_df = anf_old_df.rename(columns={"(\'text\',)": "text", '(\'year\',)': "datum"})

motioner_old = "/home/hilhag/prjs/skoldiskurs/data/motioner_1971_2013.parquet"
mot_old = pd.read_parquet(motioner_old)
mot_old = mot_old[mot_old['(\'text\',)'].notna()]
mot_old_df = mot_old[['(\'text\',)', '(\'datum\',)']] # date var is "('datum',)"
mot_old_df = mot_old_df.rename(columns={"(\'text\',)": "text", '(\'datum\',)': "datum"})

### MERGE FRAMES

df = pd.concat([mot_new_df, anf_new_df, mot_old_df, anf_old_df], axis=0)
df['datum'] = df['datum'].astype(str)
df.to_parquet("political_corpus.parquet")
