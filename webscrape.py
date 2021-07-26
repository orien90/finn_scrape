from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os.path

url = "https://www.finn.no/job/fulltime/search.html?abTestKey=control&extent=3947&location=1.20001.20061&occupation=0.23&sort=RELEVANCE"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
job_ads = soup.find_all(class_="ads__unit__content")
keywords = ['utvikler', 'data', 'developer']
job_list = []
hrefs = []
df_read = []

# opens file (if exists) and get url column into hrefs
if not os.path.isfile('job_list.xlsx'):
    df_create = pd.DataFrame(job_list)
    df_create.to_excel('job_list.xlsx')
else:
    df_read = pd.read_excel('job_list.xlsx')
    if not df_read.empty:
        hrefs = [x[3] for x in df_read.values.tolist()]  # urls is stored in column 3 in excel file

for job_ad in job_ads:
    for key in keywords:
        # get finn.no jobads via BeautifulSoup
        contents = job_ad.find_all(text=re.compile(key), class_="ads__unit__link")
        keys = job_ad.find_all(class_="ads__unit__content__keys")
        jobs = zip(keys, contents)
        # add job title, summary and url to job_list
        for job in jobs:
            ad_content = []
            if job[1].attrs['href'] not in hrefs:
                ad_content.append(job[0].contents[0].contents[0])
                ad_content.append(job[1].contents[0])
                ad_content.append(job[1].attrs['href'])
                job_list.append(ad_content)

if type(df_read) is not list:
    for old in df_read.values.tolist():
        job_list.append([old[1], old[2], old[3]])
if job_list:
    df = pd.DataFrame(job_list, columns=["Tittel", "Beskrivelse", "Url"])
    df.to_excel('job_list.xlsx', sheet_name="ark1")
