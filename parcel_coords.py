import pandas as pd
import googlemaps
from tqdm import tqdm

tqdm.pandas()
key =""


gmaps_key = googlemaps.Client(key=key)

def geocode(add):
    g = gmaps_key.geocode(add)
    lat = g[0]["geometry"]["location"]["lat"]
    lng = g[0]["geometry"]["location"]["lng"]
    return (lat,lng)
  
def full_address(add, city):
  return add + ", " + city + ", PA"

def main():
  data = pd.read_csv('sideyard473.csv',encoding="ISO-8859-1")
  df = data.copy()
  
  df['property_address'] = df['ï»¿Property_Address']
  df = df.drop(['ï»¿Property_Address'], axis=1)
  
  
  df['full_address'] = df.progress_apply(lambda x: full_address(x['property_address'], x['City']), axis=1)
  df = df.drop(['City'], axis=1)

  df['coords'] = df['full_address'].apply(geocode)

  df.to_csv("sideyards_coords.csv")
  
main()