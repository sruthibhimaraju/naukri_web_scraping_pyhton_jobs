# import required libraries
import bs4
import urllib.request
import pandas as pd
import math
import time
from pandas import DataFrame,Series
from collections import OrderedDict
import pickle


# Base Url

base_url = 'https://www.naukri.com/python-jobs'
req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
source = urllib.request.urlopen(req).read()

# Using BeautifulSoup extract the HTML
soup = bs4.BeautifulSoup(source,"lxml")

#Extracting numbe rof jobs and pages
num_jobs = int(soup.find("span",{"class":"cnt"}).getText().split(' ')[-1])
tot_num_pages = int(math.ceil(num_jobs/50.0))
num_pages = input('Enter the number of pages:')

labels = ['Salary','Industry', 'Functional Area', 'Role Category', 'Design Role']
naukri_df = pd.DataFrame()

#Extracting all the links in each pages
for page in range(1,int(num_pages)):
    #print(str(page))
    page_url = base_url+'-'+str(page)
    #print(page_url)
    page_request =  urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    source_new = urllib.request.urlopen(page_request).read()
    soup = bs4.BeautifulSoup(source_new,"lxml")
    links = []
    for link in soup.find_all("a",{"class":"content"}):
        links.append(link.get('href'))
    if 'job-listings' in str(links):
        all_links = links
    # Extracting required information in each link
    for url in all_links:
        url_new = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        jd_source = urllib.request.urlopen(url_new).read()
        jd_soup = bs4.BeautifulSoup(jd_source,"lxml")
        try:
            jd_text = jd_soup.find("ul",{"class":"listing mt10 wb"}).getText().strip()
            location = jd_soup.find("div",{"class":"loc"}).getText().strip()
            experience = jd_soup.find("div",{"class":"p"}).find("span",recursive=False).getText().strip()
            role_info = [content.getText().split(':')[-1].strip() for content in jd_soup.find("div",{"class":"jDisc mt20"}).contents 
            if len(str(content).replace(' ',''))!=0]
            role_info_dict = {label:role_info for label ,role_info in zip(labels,role_info)}
            key_skills = '|'.join(jd_soup.find("div",{"class":"ksTags"}).getText().split('  '))[1:]
            company_name = jd_soup.find("div",{"class":"row mb8"}).find("a",{"itemprop":"hiringOrganization"}).getText()
                        
        except AttributeError:
            continue
        df_dict = OrderedDict({'Location':location,'Link':url,'Job Description':jd_text,'Experience':experience,'Skills':key_skills,'Company Name':company_name})
        df_dict.update(role_info_dict)
        naukri_df = naukri_df.append(df_dict,ignore_index=True)
        time.sleep(1)
    
    
column_names = ['Location','Link','Job Description','Experience','Salary','Industry','Functional Area','Role Category','Design Role','Skills','Company Name']
naukri_df = naukri_df.reindex(columns=column_names)

#Exporting the data to a csv file
naukri_df.to_csv('naukri.csv') 
naukri_df.shape
naukri_df.head()


























