import time
import requests
import re
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from slugify import slugify
from pymongo import MongoClient
from fuzzywuzzy import fuzz

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathes import tags_and_pathes

all_links_async = []
all_names_arr = []
domen = 'https://rawg.io'


def get_all_links_of_games(count_of_pages: int) -> list:
    all_links = []

    for page in range(1, count_of_pages + 1):
        url = f'https://rawg.io/games?page={page}'

        page_html = requests.get(url)
        soup = BeautifulSoup(page_html.text, "html.parser")

        all_names = soup.findAll('a', class_='game-card-medium__info__name')

        for data in all_names:
            all_links.append(data.get('href'))

    return all_links


def get_all_unique_publishers():
    try:
        conn = MongoClient()
    except:
        print('Cannot Connect')

    db = conn.game_info_box
    collection = db.game_info
    return collection.find({}).distinct('publishers')

# ['SCE Japan Studio', 'Edmund McMillen', 'Capcom', '3909', '2K Games']
# ['Edmund McMillen', 'Capcom', '3909', '2K Games']
# ['Capcom', '3909', '2K Games']
# ['3909', '2K Games']
# ['2K Games']
def get_publisher_info():
    browser = webdriver.Chrome()
    browser.get('https://www.mobygames.com/company/page:0/')
    full_name = None
    publishers_list = get_all_unique_publishers()
    for name in publishers_list:
        time.sleep(4)
        search_input = browser.find_element(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/form/div/input')
        result_path = ''
        if search_input:
            search_input.clear()
            search_input.click()
            search_input.send_keys(f'/c {name}')
            WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]')))
            time.sleep(4)
            results = browser.find_elements(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li')

            for i in range(len(results) - 1):
                if fuzz.token_set_ratio(name, results[0].text.split('\n')[1]) > 85 and i == len(results) - 2:
                    result_path = '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]'
                    full_name = re.sub(r' \([^)]*\)', '', results[i].text.split('\n')[0])
                    break

                if name in results[i].text.split('\n')[1]:
                    result_path = f'//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[{i + 1}]'
                    full_name = re.sub(r' \([^)]*\)', '', results[i].text.split('\n')[0])
                    break
            else:
                search_input.clear()
                search_input.click()
                search_input.send_keys(f'/p {name}')
                WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located(
                    (By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]')))
                time.sleep(4)
                results = browser.find_elements(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li')
                full_name = re.sub(r' \([^)]*\)', '', results[0].text.split('\n')[0])
                result_path = '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]'

            result = browser.find_element(By.XPATH, result_path)
            result.click()
            try:
                photo = browser.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div[1]/figure/a/img').get_property('src')
                try:
                    description = browser.find_element(By.XPATH, '/html/body/div/main/div/div[1]/section[1]/div/p[1]').text
                except:
                    description = browser.find_element(By.XPATH, '/html/body/div/main/div/div[1]/section[2]/div').text
            except:
                photo, description = None, "Sorry! Publisher information is missing. Could be a little known publisher or indie developer. Good luck to him..."

            publisher = {
                "name": full_name,
                "slug": slugify(name),
                "description": description,
                "photo_url": photo
            }
            print(publisher, '\n')
            try:
                conn = MongoClient()
            except:
                print('Cannot Connect')

            db = conn.game_info_box
            collection = db.publisher_info
            collection.insert_one(publisher)
            browser.back()


def temp_publishers():
    t = []
    print('[')
    for i in range(1, 16):
        page_html = requests.get(f'https://www.mobygames.com/company/page:{i}/')
        soup = BeautifulSoup(page_html.text, "html.parser")

        companies = soup.findAll('tr')[1:]

        for i in companies:
            print(f"\"{[e.text.strip() for e in i.find_all('td')][0]}\",")
        # t.append([e.text.strip() for e in i.find_all('td')][0])
    print(']')


def get_game_info(link):
    page_html = requests.get(link)

    while page_html.status_code != 200:
        page_html = requests.get(link)

    soup = BeautifulSoup(page_html.text, "html.parser")

    name = soup.select_one(tags_and_pathes["name"]).text if soup.select_one(tags_and_pathes["name"]) else None
    time_to_play = soup.select_one(tags_and_pathes["playtime"]).text.split(': ')[1] if soup.select_one(
        tags_and_pathes["playtime"]) else None
    temp_description = soup.select_one(tags_and_pathes["about"]).find_all('p') if soup.select_one(
        tags_and_pathes["about"]) else None
    description = ""
    for p in temp_description:
        if 'Español' in p.text:
            break
        description += p.text.strip()

    # Получение превью фото
    preview_photo_path = tags_and_pathes["preview_photo"]
    preview_photo_match = re.finditer(r'https?:\/\/[\w.\/\-]+', soup.select_one(preview_photo_path).get('style'))
    preview_photo = ''
    for i in preview_photo_match:
        preview_photo = i[0].replace('/1280/', '/600/')

    # Получение половины фотографий
    photos_arr = []
    photos_page = requests.get('https://rawg.io/games/grand-theft-auto-v/screenshots')
    while photos_page.status_code != 200:
        photos_page = requests.get('https://rawg.io/games/grand-theft-auto-v/screenshots')

    photos = BeautifulSoup(photos_page.text, "html.parser")
    all_photos = photos.findAll('img',
                                class_='responsive-image game-subpage__block-item game-subpage__screenshots-item')
    for i in all_photos:
        photos_arr.append(i.get('src').replace('/200/', '/600/'))

    # Получение всей подробной информации из тегов
    info_full = soup.select_one(tags_and_pathes["full_info"]).findAll('div', class_='game__meta-block')
    platforms, score, genres, date, publishers, age = [], None, [], {}, [], None
    for i in info_full:
        all_info_tags = i.find('div', class_='game__meta-title').text
        curr_info = i.find('div', class_='game__meta-text')
        match all_info_tags:
            case 'Platforms':
                platforms = curr_info.text.split(', ')
            case 'Metascore':
                score = curr_info.text
            case 'Genre':
                genres = curr_info.text.split(', ')
            case 'Release date':
                release_date = curr_info.text.split(', ')
                day_and_month = release_date[0].split(' ')
                date = {
                    "day": int(day_and_month[1]),
                    "month": str(day_and_month[0]),
                    "year": int(release_date[1])
                }
            case 'Developer':
                publishers = curr_info.text.split(', ')
            case 'Publisher':
                publishers = curr_info.text.split(', ')
            case 'Age rating':
                age = curr_info.text.split(' ')[0]

    game = {
        "name": name,
        "slug": slugify(name),
        "age": age,
        "playtime": time_to_play,
        "description": description,
        "score": score,
        "date": date,
        "genres": genres,
        "platforms": platforms,
        "publishers": publishers,
        "preview_url": preview_photo,
        "photos": photos_arr
    }

    return game


def insert_data_into_db(links):
    try:
        conn = MongoClient()
    except:
        print('Cannot Connect')

    db = conn.game_info_box
    collection = db.game_info
    for i in links:
        collection.insert_one(get_game_info(i))


async def get_info(session, page):
    url = f'{domen}/games?page={page}'

    async with session.get(url=url) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "html.parser")

        all_names = soup.findAll('a', class_='game-card-medium__info__name')

        for data in all_names:
            all_links_async.append(domen + data.get('href'))


async def get_all_links_async(count_of_pages):
    async with aiohttp.ClientSession() as session:
        all_links = []

        for page in range(1, count_of_pages + 1):
            link = asyncio.create_task(get_info(session, page))
            all_links.append(link)

        await asyncio.gather(*all_links)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_all_links_async(13))

    insert_data_into_db(all_links_async)
    
    get_publisher_info()


if __name__ == '__main__':
    main()
