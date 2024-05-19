import time  # Для задержки
import requests  # Для отправки запросов
import re  # Для регулярных выражений
import asyncio  # Для асинхронности
import aiohttp  # Для асинхронных запросов к сайту

from bs4 import BeautifulSoup  # Парсинг по тегам
from slugify import slugify  # Для формирования slug-а
from pymongo import MongoClient  # Подключение к БД
from fuzzywuzzy import fuzz  # Библиотека для сравнения слов

# Парсер с имитацией действий пользователя
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathes import tags_and_pathes  # Пути для парсинга информации
from cache_games_info import all_links, temp_all_links

all_links_async = []  # Хранение всех ссылок на игры
unique_publishers = set()  # Сохраняем имена всех УНИКАЛЬНЫХ издателей
domen = 'https://rawg.io'  # Домен сайта с которого парсятся игры


def get_db_collection(name_collection):
    """Подключение к базе данных MongoDB"""
    try:
        conn = MongoClient()
    except:
        print('Cannot Connect')

    db = conn.game_info_box
    collection = db[name_collection]

    return collection


def get_publisher_info():
    """ Получение информации об издателе. Для уменьшения кол-ва промахов используется сравнение слов"""
    browser = webdriver.Chrome()  # Создание клиента браузера
    browser.get('https://www.mobygames.com/company/page:0/')  # Получение страницы
    full_name = None  # Запоминаем имя
    # publishers_list = get_all_unique_publishers()
    publishers_list = list(unique_publishers)  # Преобразование множества в массив
    for name in publishers_list:  # Проходим по всем издателям
        time.sleep(4)  # Задержка для загрузки страницы
        # Находим элемент поиска на сайте
        search_input = browser.find_element(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/form/div/input')
        result_path = ''  # Запоминаем путь для перехода к полной информации издателя
        if search_input:  # Если нашли поисковик
            search_input.clear()  # Очистка поля поиска
            search_input.click()
            search_input.send_keys(f'/c {name}')  # Заполняем поле поиска
            WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]')))
            time.sleep(4)  # Ждем загрузку результатов
            results = browser.find_elements(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li')

            # Проходимся по всем результатам
            for i in range(len(results) - 1):
                # Если мы дошли до конца и первое название в результатах очень схожи, то запоминаем его
                if fuzz.token_set_ratio(name, results[0].text.split('\n')[1]) > 85 and i == len(results) - 2:
                    result_path = '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]'
                    full_name = re.sub(r' \([^)]*\)', '', results[i].text.split('\n')[0])  # Удаляем все что между скобками
                    break

                # Если находим полное совпадение, то запоминаем его
                if name in results[i].text.split('\n')[1]:
                    result_path = f'//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[{i + 1}]'
                    full_name = re.sub(r' \([^)]*\)', '', results[i].text.split('\n')[0])
                    break
            else:  # Если прошлись по всем результатам с ключем "/c" и не нашли ничего, то берем другой ключ
                search_input.clear()
                search_input.click()
                search_input.send_keys(f'/p {name}')
                WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located(
                    (By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]')))
                time.sleep(4)
                results = browser.find_elements(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li')
                full_name = re.sub(r' \([^)]*\)', '', results[0].text.split('\n')[0])
                result_path = '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]'

            result = browser.find_element(By.XPATH, result_path)  # Находим ссылку для перехода и переходим
            result.click()
            # Получаем всю нужную информацию
            try:
                photo = browser.find_element(By.XPATH,
                                             '/html/body/div/main/div/div[2]/div[1]/figure/a/img').get_property('src')
                try:
                    description = browser.find_element(By.XPATH,
                                                       '/html/body/div/main/div/div[1]/section[1]/div/p[1]').text
                except:
                    description = browser.find_element(By.XPATH, '/html/body/div/main/div/div[1]/section[2]/div').text
            except:
                photo, description = None, "Sorry! Publisher information is missing. Could be a little known publisher or indie developer. Good luck to him..."

            # Формируем словарь(объект) издателя
            publisher = {
                "name": full_name,
                "slug": slugify(name),
                "description": description,
                "photo_url": photo
            }

            # Заносим издателя в БД и возвращаемся на страницу поиска
            collection = get_db_collection('publisher_info')
            if collection.find_one({'slug': publisher['slug']}) is None:
                collection.insert_one(publisher)
            else:
                continue
            browser.back()


def get_game_info(link):
    """
        Получение полной информации об игре по ссылке
        Args:
            link(str): Ссылка на игру

        Returns:
            game(dict): Словарь(объект) игры для БД
    """
    page_html = requests.get(link)  # Получение страницы
    # Пока не получим страницу, получаем ее
    while page_html.status_code != 200:
        page_html = requests.get(link)

    soup = BeautifulSoup(page_html.text, "html.parser")  # Находим все теги

    name = soup.select_one(tags_and_pathes["name"]).text if soup.select_one(tags_and_pathes["name"]) else None
    time_to_play = soup.select_one(tags_and_pathes["playtime"]).text.split(': ')[1] if soup.select_one(
        tags_and_pathes["playtime"]) else None
    temp_description = soup.select_one(tags_and_pathes["about"]) if soup.select_one(
        tags_and_pathes["about"]) else None
    description = ""
    # Удаляем лишние абзацы на другом языке
    for p in temp_description:
        if 'Español' in p.text:
            break
        description += p.text.strip().replace('\n', '')

    # Получение превью фото
    preview_photo_path = tags_and_pathes["preview_photo"]
    preview_photo_match = re.finditer(r'https?:\/\/[\w.\/\-]+', soup.select_one(preview_photo_path).get('style'))
    preview_photo = ''
    for i in preview_photo_match:
        preview_photo = i[0].replace('/1280/', '/600/')

    # Получение половины фотографий
    photos_arr = []
    photos_page = requests.get(link + '/screenshots')
    while photos_page.status_code != 200:
        photos_page = requests.get(link + '/screenshots')

    photos = BeautifulSoup(photos_page.text, "html.parser")
    all_photos = photos.findAll('img',
                                class_='responsive-image game-subpage__block-item game-subpage__screenshots-item')
    for i in all_photos:
        photos_arr.append(i.get('src').replace('/200/', '/600/'))

    # Получение всей подробной информации из тегов
    info_full = soup.select_one(tags_and_pathes["full_info"]).findAll('div', class_='game__meta-block')
    platforms, score, genres, date, publisher_obj, age = [], None, [], {}, [], None
    for i in info_full:
        all_info_tags = i.find('div', class_='game__meta-title').text
        curr_info = i.find('div', class_='game__meta-text')
        # Используем конструкцию чтобы автоматически пропускать блоки, если их нет
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
                for publisher in publishers:
                    publisher_obj.append({"name": publisher, "slug": slugify(publisher)})
            case 'Publisher':
                publisher_obj = []
                publishers = curr_info.text.split(', ')
                for publisher in publishers:
                    publisher_obj.append({"name": publisher, "slug": slugify(publisher)})
            case 'Age rating':
                age = curr_info.text.split(' ')[0]
    # Добавляем уникальных издателей
    for i in publisher_obj:
        unique_publishers.add(i['name'])
    # формируем объект игры
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
        "publishers": publisher_obj,
        "preview_url": preview_photo,
        "photos": photos_arr
    }

    return game


def insert_data_into_db(links):
    collection = get_db_collection('game_info')
    for i in links:
        game = get_game_info(i)
        if collection.find_one({'slug': game['slug']}) is None:
            print(game)
            collection.insert_one(game)
        else:
            print(f'Игра есть {game["name"]}')
            continue


# Асинхронные функции для БЫСТРОГО получения ссылок на игры
async def get_info(session, page):
    url = f'{domen}/games?page={page}'

    async with session.get(url=url) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "html.parser")

        all_names = soup.findAll('a', class_='game-card-medium__info__name')

        for data in all_names:
            all_links_async.append(domen + data.get('href'))


async def get_all_links_async(stop, start=1):
    async with aiohttp.ClientSession() as session:
        all_links = []

        for page in range(start, stop + 1):
            link = asyncio.create_task(get_info(session, page))
            all_links.append(link)

        await asyncio.gather(*all_links)


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_all_links_async(14, 13))

    insert_data_into_db(all_links_async)

    get_publisher_info()

    # insert_data_into_db(['https://rawg.io/games/adventure-capitalist', 'https://rawg.io/games/grand-theft-auto-v'])
    # print(unique_publishers)

    # try:
    #     conn = MongoClient()
    # except:
    #     print('Cannot Connect')
    #
    # db = conn.game_info_box
    # collection = db.game_info
    # for document in collection.find():
    #     publishers = document.get('publishers', [])
    #     # print(publishers)
    #     publisher_obj = [{"name": publisher, "slug": slugify(publisher)} for publisher in publishers]
    #     print(publisher_obj)
    #     collection.update_one(
    #         {"_id": document["_id"]},
    #         {"$set": {"publishers": publisher_obj}}
    #     )

    # for link in temp_all_links:
    #     page_html = requests.get(link)
    #
    #     while page_html.status_code != 200:
    #         page_html = requests.get(link)
    #
    #     soup = BeautifulSoup(page_html.text, "html.parser")
    #     name = soup.select_one(tags_and_pathes["name"]).text if soup.select_one(tags_and_pathes["name"]) else None
    #     photos_arr = []
    #     photos_page = requests.get(link + '/screenshots')
    #     while photos_page.status_code != 200:
    #         photos_page = requests.get(link + '/screenshots')
    #
    #     photos = BeautifulSoup(photos_page.text, "html.parser")
    #     all_photos = photos.findAll('img',
    #                                 class_='responsive-image game-subpage__block-item game-subpage__screenshots-item')
    #     for i in all_photos:
    #         photos_arr.append(i.get('src').replace('/200/', '/600/'))
    #
    #     try:
    #         conn = MongoClient()
    #     except:
    #         print('Cannot Connect')
    #
    #     print(name)
    #     db = conn.game_info_box
    #     collection = db.game_info
    #     query_filter = {'slug': slugify(name)}
    #     update_op = {'$set': {'photos': photos_arr} }
    #     result = collection.update_one(query_filter, update_op)


if __name__ == '__main__':
    main()
