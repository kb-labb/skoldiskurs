mkdir motioner_1971-2013_json

wget https://data.riksdagen.se/dataset/dokument/mot-1971-1979.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-1980-1989.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-1990-1997.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-1998-2001.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-2002-2005.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-2006-2009.json.zip -P motioner_1971-2013_json
wget https://data.riksdagen.se/dataset/dokument/mot-2010-2013.json.zip -P motioner_1971-2013_json

unzip motioner_1971-2013_json/mot-1971-1979.json.zip -d motioner_1971-2013_json
unzip motioner_1971-2013_json/mot-1980-1989.json.zip -d motioner_1971-2013_json
unzip motioner_1971-2013_json/mot-1990-1997.json.zip -d motioner_1971-2013_json
unzip motioner_1971-2013_json/mot-1998-2001.json.zip -d motioner_1971-2013_json
unzip motioner_1971-2013_json/mot-2002-2005.json.zip -d motioner_1971-2013_json
unzip motioner_1971-2013_json/mot-2010-2013.json.zip -d motioner_1971-2013_json

rm motioner_1971-2013_json/*.json.zip
