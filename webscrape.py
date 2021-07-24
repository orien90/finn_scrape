from bs4 import BeautifulSoup
import requests
import re

url = "https://www.finn.no/job/fulltime/search.html?abTestKey=control&extent=3947&location=1.20001.20061&occupation=0.23&sort=RELEVANCE"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
annonser = soup.find_all(class_="ads__unit__content")
keywords = ['nyutdannet', '2022', 'utvikler', 'økonom', 'developer']
job_list = []
for annonse in annonser:
    for key in keywords:
        contents = annonse.find_all(text=re.compile(key), class_="ads__unit__link")
        keys = annonse.find_all(class_="ads__unit__content__keys")
        jobs = zip(keys, contents)
        for job in jobs:
            ad = []
            ad.append(job[0].contents[0].contents[0])
            ad.append(job[1].contents[0])
            ad.append(job[1].attrs['href'])
            job_list.append([ad])

for item in job_list:
    print(item)
