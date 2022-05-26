import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd


lcw_category = "category=metaverse"

lcw_URL = "https://www.livecoinwatch.com/?" + lcw_category

pg = requests.get(lcw_URL, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(pg.text, 'html.parser')

assets_found = []
assets_main_price = []
assets_last_24 = []

#Scrappy assets list and get name
dv_name = soup.find_all("div", {'class': 'filter-item-name'})
asset_name = soup.find('p')

for asset_name in dv_name:
    asset_name_get_txt = asset_name.get_text()
    assets_found.append(asset_name_get_txt)
    #print(asset_name.get_text())
#####


#Scrappy assets list and get main price
dv_main_pr = soup.find_all("td", {'class': 'main-price'})
m_price = soup.find('p')

for m_price in dv_main_pr:
    asset_get_m_txt_price = m_price.get_text()
    assets_main_price.append(asset_get_m_txt_price)
    #print(m_price.get_text())

######

#Scrappy assets list and get last 24 % change
dv_24h_lp = soup.find_all("span", {'class': 'percent'})

last_24h_quickfix = []

for i in dv_24h_lp:
    gt_24h_change = soup.find('p')
    l_24_txt = i.get_text()
    last_24h_quickfix.append(i.get_text())
    #print(l_24_txt)

#formating and getting last24
for i in last_24h_quickfix[1::2]:
    assets_last_24.append(i)

#####

#Save in a excel file

# Create a Pandas dataframe from the data.
df = pd.DataFrame({
    'Assets': assets_found,
    'Last 24h Change': assets_last_24,
    'Price Now': assets_main_price
})

#Here we print our dataset
print(df)

while True:
    # Then ask if user wants to save it in a excel file
    print("Save in a excel file?")
    print("We can save it in a excel file. Type 'Y' for 'Yes' or 'N' for 'No'?")
    save_in_excel = input()
    try:
        if save_in_excel.upper() == 'Y':
            print("Cool, Done.")
            writer = pd.ExcelWriter('clw.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Coins')
            writer.save()
            break
        if save_in_excel.upper() == 'N':
            print("Ok, bye.")
            break
    except ValueError:
        print("Invalid input. 'Y' for YES or 'N' for NO")




