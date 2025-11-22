import requests
from bs4 import BeautifulSoup

URL = "https://genshin-impact.fandom.com/wiki/Character/List"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

characters = []

tables = soup.find_all("table", class_="fandom-table article-table sortable alternating-colors-table")

for table in tables:
    rows = table.find_all("tr")[1:]  # skip header row
    if len(rows) < 100:
        continue
    for row in rows:
        cols = row.find_all("td")
        if cols:
            name_tag = cols[1].find("a")
            if name_tag:
                characters.append(name_tag.get_text(strip=True))

print(characters)
print("Total characters:", len(characters))
