from bs4 import BeautifulSoup
import json
import pandas as pd
import io
import os

# This is a quick and dirty adaptation of script found here: https://github.com/kb-labb/bertopic_workshop/blob/main/parse_motioner.py
# Less detailed due to the structure of older riksdagsmotioner

dir = "/home/gilleti/Documents/skoldiskurs/data_scripts/motioner/motioner_1971-2013_json/"
files = os.listdir(dir)

def read_motion_json(filename, folder):
    with io.open(os.path.join(folder, filename), "r", encoding="utf-8-sig") as f:
        motion_json = json.load(f)
    return motion_json

def parse_html(motion):
    motion_html = motion["dokumentstatus"]["dokument"]["html"]
    soup = BeautifulSoup(motion_html, "html.parser")
    try:
        page = soup.find('p').getText()
        d = []
        for data in soup.find_all("p"):
            p = data.get_text()
            if len(p) > 100:
                d.append(p)
        document = " ".join(d)
        document = document.replace("\n", "")
        document = document.replace("\r", "")
        return document
    except AttributeError:
        return None

def get_motion_data(filename, folder):
    """
    Parse folder with bunch of json files of parliamentary motions.
    """

    motion_json = read_motion_json(filename, folder)
    datum = motion_json["dokumentstatus"]["dokument"]["datum"]
    dok_id = motion_json["dokumentstatus"]["dokument"]["dok_id"]
    url = motion_json["dokumentstatus"]["dokument"]["dokument_url_html"]
    motion_text = parse_html(motion_json)
    data = [[dok_id, motion_text, datum, url]]
    df = pd.DataFrame(data, columns=[['dok_id', 'text', 'datum', 'url']])
    return df

dfs = []

for file in files:
    tmp_df = get_motion_data(file, dir)
    dfs.append(tmp_df)

df = pd.concat(dfs, ignore_index=True)
df.to_parquet("motioner_1971_2013.parquet")
