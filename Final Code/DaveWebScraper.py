from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup 

def writeLyrics(url, outputFile):
    uClient = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')

    tables = page_soup.findAll("table")

    for table in tables:
        if table.tr.get_text() == "Lyrics":
            rows = table.findAll("tr")
            lyrics = rows[-1].get_text(separator="\n")

            try:
                outputFile.write(lyrics)
            except Exception as inst:
                print("Writing failed due to " + str(inst))

my_url = "https://www.cs.ubc.ca/~davet/music/genre/genre6.html"
url_head = "https://www.cs.ubc.ca/~davet/music"

uClient = urlopen(Request(my_url, headers={'User-Agent': 'Mozilla/5.0'}))
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, 'html.parser')

#get table elements
table_elements = page_soup.findAll("td")

urls = list()
for element in table_elements:
    if not element.a == None and element.a.get_text() == 'details...':
        urls.append(url_head + element.a.get('href').split("..")[1])


outputFile = open("all_lyrics.txt", "+w")
outputFile.write("")
outputFile.close()

i = 0
for url in urls:
    outputFile = open("all_lyrics.txt", "a")
    print("Writing song " + str(i))
    writeLyrics(url, outputFile)
    outputFile.write("\n")
    outputFile.close()
    i += 1

