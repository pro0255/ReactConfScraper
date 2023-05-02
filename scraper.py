import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime




talk = "talks"
workshops = "workshops"

SEP = ','

EMPTY = "NADA!!"




class Scraper:
  def __init__(self, url) -> None:
    self.url = url
    print(f'Initialized scaper with {url}')
    
    
    
  def save_talks(self):
    target_url = os.path.join(self.url, talk)
  
    page = requests.get(target_url)    
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="row-margin__item")
    
    
    scraped_items = {}
    
    for i, item in enumerate(items):
      time = item.find("div", class_="time upcoming").text
      
      #Jun 1, 12:30
      date_object = datetime.strptime(time, '%b %d, %H:%M')      
      time = date_object
      
    
    
      title = item.find("div", class_="article-box__title").text
      author_name = EMPTY
      author_cat = EMPTY
      
      if item.find("div", class_="abh-author__name"):
        author_name = item.find("div", class_="abh-author__name").text
      
      if item.find("div", class_="abh-author__cat"):
        author_cat = item.find("div", class_="abh-author__cat").text
      
      tags_list = item.find("div", class_="tags-list")
      tags = [tag.text for tag in tags_list]
      scraped_items[i] = [time, title, author_name, author_cat, ','.join(tags)]
      
    columns = ['Time', 'Title', "Author", "Catogery", "Tags"]
    
    return pd.DataFrame.from_dict(scraped_items, orient='index', columns=columns)
    
    
    
  def save_workshops(self):
    target_url = os.path.join(self.url, workshops)
    
    page = requests.get(target_url)    
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="row-margin__item")
    
    
    scraped_items = {}
    
    for i, item in enumerate(items):
      time = item.find("div", class_="time upcoming").text
      
      date_object = datetime.strptime(time, '%b %d, %H:%M')      
      time = date_object
      
    
      title = item.find("div", class_="article-box__title").text
      author_name = EMPTY
      author_cat = EMPTY
      
      if item.find("div", class_="ab-author__name"):
        author_name = item.find("div", class_="ab-author__name").text
      
      content = item.find("div", class_="article-box__text").text
      
      scraped_items[i] = [time, title, author_name, content]
      
    columns = ['Time', 'Title', "Author", "Content"]
    return pd.DataFrame.from_dict(scraped_items, orient='index', columns=columns)
    
  def get_name(self):
    return self.url.split(os.path.sep)[-1]
  
  def scrape(self):
    talks_df = self.save_talks()
    workshops_df = self.save_workshops()
    
    dir = "confs"
    
    conf_name = self.get_name()
    path = os.path.join(dir, conf_name)
    
    
    if not os.path.exists(path):
      os.makedirs(path)


    #Sort by time
    talks_df = talks_df.sort_values(by=['Time'])
    workshops_df = workshops_df.sort_values(by=['Time'])
    
    talks_df.Time = [t.strftime("%b %d, %H:%M") for t in talks_df.Time] 
    workshops_df.Time = [t.strftime("%b %d, %H:%M") for t in workshops_df.Time] 
    
    
    #Save to directory
    talks_df.to_csv(os.path.join(path, f"{talk}.csv"), sep=SEP, index=False)
    workshops_df.to_csv(os.path.join(path, f"{workshops}.csv"), sep=SEP, index=False)


    
    
    