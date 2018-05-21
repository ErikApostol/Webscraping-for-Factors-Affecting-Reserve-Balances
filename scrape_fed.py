from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import urllib2

data = pd.DataFrame()

page_link ='https://www.federalreserve.gov/releases/h41/'
# fetch the content from url
page_response = requests.get(page_link, timeout=5)
# parse html
page_content = BeautifulSoup(page_response.content, "html.parser")

# extract all html elements where price is stored
weekly_releases = page_content.find_all(class_='col-xs-1')
print(len(weekly_releases))

week_num = 0
for week in weekly_releases:
    date = week.find('a').attrs['href']
    if date == 'current':
        data.loc[week_num, 'Date'] = "May 17, 2018"
    else:
        data.loc[week_num, 'Date'] = datetime.strptime(date, '%Y%m%d').strftime('%b %d, %Y')

    txt = urllib2.urlopen('https://www.federalreserve.gov/releases/h41/'+date+'/H41.TXT')
    for line in txt:
        if 'Gold certificate account' in line:
            print(line)
    txt.close()

    week_num += 1

data.to_csv('data.csv')
