from bs4 import BeautifulSoup
import requests

url = "https://www.finn.no/job/fulltime/search.html?abTestKey=control&extent=3947&location=1.20001.20061&occupation=0.23&sort=RELEVANCE"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
annonser = soup.find_all(class_="ads__unit__content")
for annonse in annonser:
    contents = annonse.find_all(class_="ads__unit__link")
    keys = annonse.find_all(class_="ads__unit__content__keys")
    jobs = zip(keys, contents)
    for job in jobs:
        print(job[0].contents[0].contents[0])
        print(job[1].contents[0])
        print(job[1].attrs['href'])
        print("----------------")

