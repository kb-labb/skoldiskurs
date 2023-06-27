import os
import io
import json
import pandas as pd
import multiprocessing as mp
from bs4 import BeautifulSoup, NavigableString


def read_motion_json(filename, folder="motioner_2014-2023_json"):
    with io.open(os.path.join(folder, filename), "r", encoding="utf-8-sig") as f:
        motion_json = json.load(f)

    return motion_json


def author_party_count(motion):
    authors = motion["dokumentstatus"]["dokintressent"]["intressent"]

    party_count = {
        "V": 0,
        "S": 0,
        "MP": 0,
        "C": 0,
        "L": 0,
        "KD": 0,
        "M": 0,
        "SD": 0,
        "-": 0,
    }

    if isinstance(authors, dict):
        authors = [authors]

    for author in authors:
        party_count[author["partibet"]] += 1

    return party_count


def parse_html(motion):
    motion_html = motion["dokumentstatus"]["dokument"]["html"]
    soup = BeautifulSoup(motion_html, "html.parser")

    if motion["dokumentstatus"]["dokument"]["status"] == "Utgången":
        return None

    # Remove signatures at bottom of bill that contain party affiliations
    for signature in soup.find_all(
        "p", attrs={"style": "-aw-sdt-tag:CC_Underskrifter; -aw-sdt-title:CC_Underskrifter"}
    ):
        signature.extract()

    for table in soup.find_all("table"):
        table.extract()

    # Add periods to headers, so we can perform sentence segmentation later if necessary
    for title in soup.find_all(["h1", "h2", "h3"]):
        for span in title.find_all("span"):
            span.insert(len(span.get_text()), NavigableString("."))

    # We only want text after motion has started
    if soup.find("a", attrs={"name": "MotionsStart"}) is not None:
        motion_start = soup.find("a", attrs={"name": "MotionsStart"})
    elif soup.find("h1") is not None:
        motion_start = soup.find("h1")
    else:
        # Ignore 4 motioner that don't conform to html formatting standard
        print(print(motion["dokumentstatus"]["dokument"]["dok_id"]))
        return None

    # Find all headers and paragraphs after motion start
    soup = motion_start.find_all_next(["h1", "h2", "h3", "p"])
    soup = BeautifulSoup("".join([str(tag) for tag in soup]), "html.parser")

    motion_text = "".join(tag.get_text() for tag in soup)
    motion_text = " ".join(motion_text.split())  # Remove newlines, excessive whitespace

    party_count = author_party_count(motion)

    motion_fields = {
        "dok_id": motion["dokumentstatus"]["dokument"]["dok_id"],
        "text": motion_text,
        "datum": motion["dokumentstatus"]["dokument"]["datum"],
        "dokument_url_html": motion["dokumentstatus"]["dokument"]["dokument_url_html"],
        "titel": motion["dokumentstatus"]["dokument"]["titel"],
        "subtitel": motion["dokumentstatus"]["dokument"]["subtitel"],
        "organ": motion["dokumentstatus"]["dokument"]["organ"],
        "subtyp": motion["dokumentstatus"]["dokument"]["subtyp"],
        "party_count": [party_count],
        "hangar_id": motion["dokumentstatus"]["dokument"]["hangar_id"],
    }

    return motion_fields


def get_motion_text(filename, folder="motioner_2014-2023_json"):
    """
    Parse folder with bunch of json files of parliamentary motions.
    """

    motion_json = read_motion_json(filename, folder)
    motion_text = parse_html(motion_json)
    return motion_text


motioner_list = os.listdir("motioner_2014-2023_json")

pool = mp.Pool()
res = pool.map(get_motion_text, motioner_list)
pool.close()

res = [motion for motion in res if motion is not None]

df = pd.json_normalize(res)
df["datum"] = pd.to_datetime(df["datum"])
df["hangar_id"] = pd.to_numeric(df["hangar_id"])

df_authors = pd.DataFrame(df["party_count"].explode().tolist()).add_prefix("authors_")
df_authors["nr_authors"] = df_authors.sum(axis=1)
df_authors = df_authors.rename(columns={"authors_-": "authors_independent"})
df_authors["party"] = (df_authors.iloc[:, 0:9] >= 1).apply(
    lambda col: ",".join(col.index[col].str.slice(8)), axis=1
)

df = pd.concat([df.drop("party_count", axis=1), df_authors], axis=1)

df["single_party_authors"] = (
    df[
        [
            "authors_V",
            "authors_S",
            "authors_MP",
            "authors_C",
            "authors_L",
            "authors_KD",
            "authors_M",
            "authors_SD",
            "authors_independent",
        ]
    ]
    >= 1
).sum(axis="columns")

df["single_party_authors"] = df["single_party_authors"] <= 1
df["text"] = df["text"].str.replace("^\.", "", regex=True)
df["text"] = df["text"].str.replace("^Motivering.", "", regex=True).str.strip()
df["text"] = df["text"].str.replace("^Bakgrund.", "", regex=True).str.strip()
df["text"] = df["text"].str.replace("^Inledning", "", regex=True).str.strip()
# https://stackoverflow.com/questions/51976328/best-way-to-remove-xad-in-python
df["text"] = df["text"].str.replace("\xad", "", regex=True)


df.to_parquet("motioner_2014_2023.parquet")
