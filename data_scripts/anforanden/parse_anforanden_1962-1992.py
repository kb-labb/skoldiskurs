import os
import pandas as pd
import xml.etree.ElementTree as ElementTree

path = "/home/gilleti/Documents/riksdagen-corpus/corpus/protocols/"

all_paths = os.listdir(path)

prefixes = ["1962", "1963", "1964", "1965", "1966", "1967", "1968", "1969", "197", "198", "1990", "1991", "1992"]

year_paths = []

for year_path in all_paths:
    if any(year_path.startswith(prefix) for prefix in prefixes):
        year_paths.append(year_path)

dfs = []
for year in year_paths:
    full_dir_path = path + year
    
    files = os.listdir(full_dir_path)
    for file in files:
        document = []
        dok_id = file[:-4]
        file = full_dir_path + "/" + file
        tree = ElementTree.parse(file).getroot()
        for e in tree.iter():
            if "seg" in e.tag:
                paragraph = e.text
                if not "___" in paragraph:
                    paragraph = paragraph.replace("\n              ", "")
                    document.append(paragraph.strip())
            elif "docDate" in e.tag:
                year = e.text
            elif "pb" in e.tag:
                #url = e.text
                urls = list(e.attrib.values())
                url = urls[0].split("#")[0]
                url = str(url)

        text = " ".join(document)
        data = [[dok_id, text, year]]
        tmp_df = pd.DataFrame(data, columns=[['dok_id', 'text', 'year']])
        dfs.append(tmp_df)

df = pd.concat(dfs, ignore_index=True)
df.to_parquet("anforanden_1962-1992.parquet")
