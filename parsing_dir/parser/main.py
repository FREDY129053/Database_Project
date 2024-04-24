import time
import requests
import datetime
import asyncio
import aiohttp

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cache_games_info import all_links, studios
from pathes import tags_and_pathes


all_links_async = []
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


def get_publisher_info(t = ['Includes Source SDK']):
	browser = webdriver.Chrome()
	browser.get('https://www.mobygames.com/company/page:0/')
	for name in t:
		time.sleep(3)
		search_input = browser.find_element(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/form/div/input')
		if search_input:
			search_input.clear()
			search_input.click()
			search_input.send_keys(f'/c {name}')
			WebDriverWait(browser, 15).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]')))
			time.sleep(3)
			results = browser.find_elements(By.XPATH, '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li')
			result_path = ''
			for i in range(len(results) - 1):
				if name in results[i].text.split('\n')[1]:
					result_path = f'//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[{i + 1}]'
					break
				else:
					result_path = '//*[@id="root"]/header/nav/ul/li[3]/div/div/div/ul/li[1]'
				
			result = browser.find_element(By.XPATH, result_path)
			result.click()
			print(browser.current_url)
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
	# return t

# a = 0
def get_game_info(link):
	# global a
	page_html = requests.get(link)

	while page_html.status_code != 200:
		page_html = requests.get(link)

	# a += 1
	# print(a)
	soup = BeautifulSoup(page_html.text, "html.parser")

	# name = soup.select_one(tags_and_pathes["name"]).text
	# time_to_play = soup.select_one(tags_and_pathes["playtime"]).text.split(': ')[1]
	# temp_description = soup.select_one(tags_and_pathes["about"]).find_all('p')
	# description = ""
	# for p in temp_description:
	# 	if 'Español' in p.text:
	# 		break
	# 	description += p.text.strip()
 
	x_path = "#root > div > div.page.game > div.page__content-wrap-centerer > div > main > div > div.game-content-columns > div:nth-child(1) > div.game__meta"
	info_full = soup.select_one(x_path).findAll('div', class_='game__meta-block')
 
	# platforms = soup.select_one(tags_and_pathes["platforms"]).text.split(', ')
	# score = soup.select_one(tags_and_pathes["score"]).text
	# genres = soup.select_one(tags_and_pathes["genres"]).text.split(', ')
	# age = soup.select_one(tags_and_pathes["age"]).text.split(' ')[0]
	# date = soup.select_one(tags_and_pathes["release_date"]).text.split(', ')
	# release_date = {
	# 	"date": str(date[0]),
	# 	"year": int(date[1])
	# }

	# Получение студий
	# TODO: проверить кол-во div чтоб НОРМАЛЬНО оценить разработчика!!!
	# publishers = soup.select_one(tags_and_pathes["publisher"]).text.split(', ')


	# Получение ссылок на фотографии
	# photos_url = requests.get(link + '/screenshots')
	# photos_soup = BeautifulSoup(photos_url.text, "html.parser")

	# count_of_photos = int(photos_soup.select_one(tags_and_pathes["count_of_photos"]).text.strip())

	# photos = photos_soup.select_one(tags_and_pathes["media"]).find_all('img')
	# photos = [i.get('src').replace('/200/', '/600/') for i in photos]
	# for photo in photos:
	# 	print(photo.get('src').replace('/200/', '/600/'))

	return info_full


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
	# loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(loop)
	# loop.run_until_complete(get_all_links_async(13))

	# print(all_links_async[0])
	# c = 1
	# print(all_links[c])

	# print(get_game_name(all_links[c]))

	# for i in get_game_name(all_links[c]):
	# 	print(i)
	# temp_publishers()
	# publishers_unique = []
	# for i in all_links:
	# 	t = get_game_info(i)
	# 	for j in t:
	# 		print(f"{i} = {t}")
	# 		publishers_unique.append(j)

	# a = set(publishers_unique)
	# print('[')
	# for i in list(a):
	# 	print(f'\"{i}\",')
	# print(']')
	# get_publisher_info()
	platforms, score, genres, date, publishers, age = [], 'null', [], {}, [], 'null'
	t = get_game_info('https://rawg.io/games/grand-theft-auto-san-andreas')
	for i in t:
		all_info_tags = i.find('div', class_='game__meta-title').text
		curr_info = i.find('div', class_='game__meta-text')
		match (all_info_tags):
			case 'Platforms':
				platforms = curr_info.text.split(', ')
			case 'Metascore':
				score = curr_info.text
			case 'Genre':
				genres = curr_info.text.split(', ')
			case 'Release date':
				release_date = curr_info.text.split(', ')
				date = {
					"date": str(date[0]),
					"year": int(date[1])
				}
			case 'Developer':
				...
			case 'Publisher':
				...
			case 'Age rating':
				...
	print(platforms)
	print(score)
		# print('\n\n')

	# for i in ['Akella', 'Capcom']:
	# 	get_publisher_info(i)
	



if __name__ == '__main__':
	main()