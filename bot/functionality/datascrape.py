from random import betavariate
from bs4 import BeautifulSoup
import requests

anime_id = input('enter anime id')
url = f'https://myanimelist.net/anime/{anime_id}/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


tags = soup('div', id="horiznav_nav")
for tag in tags:
    link = tag.find_all('li')
    s = link[2]
    link = s.find('a')
    episode_link = link.get('href')
    print(episode_link)


repos = requests.get(episode_link)

soupy = BeautifulSoup(repos.text, 'html.parser')


images = soupy.find_all('div', id="content")
# print(images)
for image in images:
    o = image.find('a')
    img = o.get('href')

tars = soupy.find_all('tr', class_="episode-list-data")
count = 0
name_anime = list()
date_air = list()
number_episode = list()

for tar in tars:
    # getting anime name
    s = tar.find('td', class_="episode-title")
    g = s.get_text()
    g.strip()
    f = g.replace('\n', ' ')
    d = f.replace('\xa0', ' ')
    name_anime.append(d)
    # getting anime air date
    u = tar.find('td', class_="episode-aired nowrap")
    t = u.get_text()
    t.strip()
    date_air.append(t)
    # getting episode number
    y = tar.find('td', class_="episode-number nowrap")
    q = y.get_text()
    q = int(q.strip())
    number_episode.append(q)


num = int(len(name_anime)/2)
anime_name = name_anime[0:num]
air_date = date_air[0:num]
episode_number = number_episode[0:num]

print(anime_name)
print(air_date)
print(episode_number)
print(img)
