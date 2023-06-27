import pandas as pd
import argparse
import json
import os
from tqdm import tqdm

def preprocess_text(df, textcol="anftext", is_audio_metadata=False):
    """
    Preprocess the text field.

    Args:
        df (pd.DataFrame): A pandas dataframe that contains text column with speeches.
        textcol (str): The name of the text column.

    Returns:
        pd.DataFrame: A pandas dataframe with preprocessed text column.
    """

    # Remove all text within <p> tags that contain "STYLEREF".
    # These are headers mistakenly included in the text as paragraphs.
    df[textcol] = df[textcol].str.replace(r"(<p> STYLEREF.*?</p>)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(<p>Gransknings- STYLEREF.*?</p>)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(<p><em></em><em> STYLEREF.*?</p>)", "", regex=True)

    # Some extra headers that don't contain "STYLEREF", but are still in <p> tags.
    # We grab the headers from the header column and remove "<p>{header}</p>" from the text column.
    # data/headers.csv is created in scripts/preprocess_speeches_metadata.py.
    headers = pd.read_csv("headers.csv")["avsnittsrubrik"].tolist()

    for header in headers:
        remove_header_p = f"<p>{header}</p>"
        df[textcol] = df[textcol].str.replace(remove_header_p, "", regex=False)

    df[textcol] = df[textcol].str.replace(r"<.*?>", " ", regex=True)  # Remove HTML tags
    # Remove text within parentheses, e.g. (applåder)
    df[textcol] = df[textcol].str.replace(r"\(.*?\)", "", regex=True)

    # Speaker of the house or other text not part of actual speech.
    # Found at the end of a transcript.
    df[textcol] = df[textcol].str.replace(r"(Interpellationsdebatten var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Partiledardebatten var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Frågestunden var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Överläggningen var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den särskilda debatten var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Statsministerns frågestund var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Återrapporteringen var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den muntliga frågestunden var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den utrikespolitiska debatten var [h|d]ärmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den allmänpolitiska debatten var härmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den aktuella debatten var härmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Informationen var härmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Den EU-politiska (partiledar)?debatten var härmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(Debatten med anledning av (vår|budget)propositionens avlämnande var härmed avslutad.*)", "", regex=True)
    df[textcol] = df[textcol].str.replace(r"(I detta anförande instämde.*)", "", regex=True)
    df[textcol] = df[textcol].str.strip()

    # Normalize text
    df[textcol] = df[textcol].str.normalize("NFKC")  # Normalize unicode characters
    # Remove multiple spaces
    df[textcol] = df[textcol].str.replace(r"(\s){2,}", " ", regex=True)
    # Replace &amp; with &
    df[textcol] = df[textcol].str.replace(r"&amp;", "&", regex=True)

    return df

parser = argparse.ArgumentParser(
    description="""Read json files of riksdagens anföranden, save relevant metadata fields to file."""
)
parser.add_argument("-f", "--folder", type=str, default="anforanden_1993-2023_json")
parser.add_argument("-d", "--dest_folder", type=str, default="")
args = parser.parse_args()

json_files = [
    os.path.join(args.folder, filename) for filename in os.listdir(args.folder) if filename.endswith(".json")
]

json_speeches = []

for file in tqdm(json_files):
    with open(os.path.join(file), "r", encoding="utf-8-sig") as f:
        json_speeches.append(json.load(f)["anforande"])

print("Normalizing json to dataframe...")
df = pd.json_normalize(json_speeches)
# df = df.drop(columns=["anforandetext"])
df["anforande_nummer"] = df["anforande_nummer"].astype(int)

# Headers to clean up when next script is run (download_audio_metadata.py)
headers = df.groupby("avsnittsrubrik").size().sort_values(ascending=False).head(1000)
headers.reset_index().rename(columns={0: "count"}).to_csv("headers.csv", index=False)

print("Preprocessing text...")
df = preprocess_text(df, textcol="anforandetext")

df = df.sort_values(["dok_id", "anforande_nummer"]).reset_index(drop=True)
df.loc[df["rel_dok_id"] == "", "rel_dok_id"] = None

print(f"Saving file to {os.path.join(args.dest_folder, 'anforanden_1993-2023.parquet')}")
df.to_parquet(os.path.join(args.dest_folder, "anforanden_1993-2023.parquet"))
