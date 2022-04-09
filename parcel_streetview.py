import pandas as pd
import shutil
import requests
from tqdm import tqdm

tqdm.pandas()
gmaps_key =""

  
def get_streetview_request(coords):
  clean_coords = coords.replace('(','').replace(')','') 
  
  api_url = "https://maps.googleapis.com/maps/api/streetview?"
  size = "size=640x640"
  location = "&location=" + clean_coords
  key = "&key=" + gmaps_key
    
  return  api_url + size + location + key


def get_file_path(address):
  folder = "./images/"
  file_type = ".jpg"
  
  return folder + address.replace(" ", "") + file_type

def get_streetview(url, path):
  response = requests.get(url, stream=True)
    
  if response.status_code == 200:
    with open(path, 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)
      
    del response
    
    return True
  
  del response
  return False

def main():
  data = pd.read_csv('sideyards_coords.csv',encoding="ISO-8859-1")
  df = data.copy()
  
  df = df.drop(['Unnamed: 0'], axis=1)
  df['streetViewRequest'] = df['coords'].apply(get_streetview_request)
  df['streetViewFilePath'] = df['property_address'].apply(get_file_path)
  
  df['isStreetViewPresent'] = df.progress_apply(lambda x: get_streetview(x['streetViewRequest'], x['streetViewFilePath']), axis=1) 

  
  print(df.head())
  
  df.to_csv("sideyards_requests.csv")
  
main()