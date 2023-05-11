mkdir motioner_2014-2023_json

wget https://data.riksdagen.se/dataset/dokument/mot-2022-2025.json.zip -P motioner_2014-2023_json
wget https://data.riksdagen.se/dataset/dokument/mot-2018-2021.json.zip -P motioner_2014-2023_json
wget https://data.riksdagen.se/dataset/dokument/mot-2014-2017.json.zip -P motioner_2014-2023_json

unzip motioner_2014-2023_json/mot-2022-2025.json.zip -d motioner_2014-2023_json
unzip motioner_2014-2023_json/mot-2018-2021.json.zip -d motioner_2014-2023_json
unzip motioner_2014-2023_json/mot-2014-2017.json.zip -d motioner_2014-2023_json

rm motioner_2014-2023_json/*.json.zip
