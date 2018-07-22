from bs4 import BeautifulSoup
import requests
import re
import json

def write_json_to_disk(filename, json_data):
	"""
	When called, write the json_data to a json file.
	"""
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile)

def scrape_blocktivity():
	"""
	A function to scrape blocktivity.
	Outputs to JSON.
	"""
	scraped_page = requests.get("https://blocktivity.info")
	if scraped_page.status_code == 200:
		soup = BeautifulSoup(scraped_page.text, 'html.parser')
		crypto_rows = soup.findAll('tr', attrs={'class': 'font_size_row'})

		blocktivity_summary = []
		for row in crypto_rows:
			crypto_columns = row.findAll('td')
			ranking = re.sub('<[^>]+?>', '', str(crypto_columns[0]))
			#logo = (str(crypto_columns[1]).split('cell">'))[1].split('</td')[0]
			name = re.sub('<[^>]+?>', '', str(crypto_columns[2])).split(' ⓘ')
			activity = re.sub('<[^>]+?>', '', str(crypto_columns[3])).strip('Op ')
			average_7d = re.sub('<[^>]+?>', '', str(crypto_columns[4])).strip('Op ')
			record = re.sub('<[^>]+?>', '', str(crypto_columns[5])).strip('Op ')
			market_cap = re.sub('<[^>]+?>', '', str(crypto_columns[6]))
			AVI = re.sub('<[^>]+?>', '', str(crypto_columns[7]))
			CUI = re.sub('<[^>]+?>', '', str(crypto_columns[8])).strip('ⓘ')

			blocktivity_summary.append({'rank': ranking, 'ticker': name[0], 'name': name[1], 'activity': activity, 'average_7d':average_7d, 'record': record, 'market_cap': market_cap, 'AVI': AVI, 'CUI':CUI})

		write_json_to_disk('blocktivity.json', blocktivity_summary) # Storing to disk

		return blocktivity_summary
	else:
		return None

print(scrape_blocktivity())
