import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import pickle

rating_enum = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

df = pd.DataFrame({
    'Title': [],
    'Price': [],
    'Rating': [],
    'Stock': []
})

with open('links.json') as file:
    links = json.load(file)


for link in links:

    r = requests.get(link)

    soup = BeautifulSoup(r.text, 'html.parser')

    stock_el = soup.find(class_='availability').stripped_strings
    rating_key = soup.find(class_='star-rating').attrs['class'][1]

    title = soup.find('h1').text
    price = soup.find(class_='price_color').text[2:]
    stock = list(stock_el)[0].split(' ')[2][1:]
    rating = rating_enum[rating_key]

    df.loc[len(df)] = {'Title': title, 'Price': float(price),
                       'Stock': stock, 'Rating': rating}

df.sort_values('Rating', inplace=True)

with open('data_frame.pickle', 'wb') as file:
    pickle.dump(df, file)
