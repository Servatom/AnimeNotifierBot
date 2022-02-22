from bs4 import BeautifulSoup
import requests

def getAnimeName(id):
    url = "https://myanimelist.net/anime/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    anime_name = soup.find('p', class_="title-english title-inherit")
    if anime_name is None:
        anime_name = soup.find(
            'h1', class_="title-name").text.strip()
    else:
        anime_name = anime_name.text.strip()
    return anime_name

def getAnime(id):
    url = f'https://myanimelist.net/anime/{id}/'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    tags = soup('div', id="horiznav_nav")
    for tag in tags:
        link = tag.find_all('li')
        s = link[2]
        link = s.find('a')
        episode_link = link.get('href')

    episode_link = requests.get(episode_link)

    soupy = BeautifulSoup(episode_link.text, 'html.parser')
    # get tbody
    table_body = soupy.find('tbody')
    # find all tr with class episode-list-data
    trs = table_body.find_all('tr', class_="episode-list-data")

    episode_number = None
    episode_name = ""
    anime_name = ""
    image_url = ""

    for tr in trs:
        # td with class episode-number nowrap
        episode_number = tr.find('td', class_="episode-number nowrap").text
        # td with class episode-title
        episode_name = tr.find('td', class_="episode-title").text.strip()

    # h1 class title-name
    anime_name = soupy.find('p', class_="title-english title-inherit")
    if anime_name is None:
        anime_name = soupy.find(
            'h1', class_="title-name").text.strip()
    else:
        anime_name = anime_name.text.strip()

    # img class  lazyloaded
    image_url = soupy.find(
        'div', style="text-align: center;").find('a').find('img').get('data-src')

    data = {"anime_id": id, "anime_name": anime_name, "episode_name": episode_name,
            "image_url": image_url, "episode_number": episode_number}
    
    return data