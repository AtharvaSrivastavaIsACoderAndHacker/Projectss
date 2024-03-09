import requests
from bs4 import BeautifulSoup
from os import system

system("cls")

query = input('Enter The Product To Scrape : ')
url = f"https://www.amazon.in/s?k={query}"
response = requests.get(url)
html = response.text 
soup = BeautifulSoup(html, "html.parser")


links = []
for link in soup.findAll('a'):
      linkhref = link.get('href')
      if linkhref != None:
            if "/dp/" in linkhref:
                  links.append(link.get("href"))
                   
print(links)