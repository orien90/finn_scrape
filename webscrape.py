from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = "https://www.finn.no/job/fulltime/search.html?abTestKey=control&extent=3947&location=1.20001.20061&occupation=0.23&sort=RELEVANCE"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
job_ads = soup.find_all(class_="ads__unit__content")
keywords = ['python', 'java', 'utvikler', 'data', 'developer', "maskin", "kunstig"]
job_list = []

for job_ad in job_ads:
    for key in keywords:
        contents = job_ad.find_all(text=re.compile(key), class_="ads__unit__link")
        keys = job_ad.find_all(class_="ads__unit__content__keys")
        jobs = zip(keys, contents)
        for job in jobs:
            ad_content = []
            ad_content.append(job[0].contents[0].contents[0])
            ad_content.append(job[1].contents[0])
            ad_content.append(job[1].attrs['href'])
            job_list.append(ad_content)

df = pd.DataFrame(job_list, columns=["Tittel", "Beskrivelse", "Url"])
df.to_excel('job_list.xlsx')