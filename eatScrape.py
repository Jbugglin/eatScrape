import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Columbus%2C+OH"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
businesses = soup.find_all("div", class_="info")
for business in businesses:
    business_name = business.find("a", class_="business-name")
    business_phone = business.find("div", class_="phone")
    
    data = {
        'business_name': business_name,
        'business_phone': business_phone
    }
    df = pd.DataFrame(data)

    #################
    # Save to excel #
    #################

    excel_file = 'restaurant_data.xlsx'
    df.to_excel(excel_file, index=False)