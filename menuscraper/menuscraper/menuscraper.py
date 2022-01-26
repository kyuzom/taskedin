#!/usr/bin/env python
'''
Meal menu scraper.
Find your favorite food at the best price.
'''
import sys
import abc
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

class _MenuScraperBasic(metaclass=abc.ABCMeta):
	'''
	Basic menu parser object.
	'''
	def __init__(self):
		self.meals = dict()
		self.weekdays = list()

	@abc.abstractmethod
	def parse(self):
		pass

	def get_weekday(self, day: int) -> str:
		'''
		Get back human readable weekday name.
		@param day: [int] Number of day
		@return Weekday name or empty str
		'''
		try:
			return self.weekdays[day-1]
		except IndexError:
			return ''

	def collect(self, html_doc: str):
		'''
		Collect information from the given html document.
		@param html_doc: [str] Html doc
		'''
		soup = BeautifulSoup(html_doc, 'html.parser')
		# meals
		self.meals.clear()
		menu = soup.find(id='etlap')
		price_rgx = re.compile('^\d+')
		for meal in menu.find_all(class_='menu-cell-text-row uk-text-break'):
			meal_name = meal.text.strip()
			self.meals[meal_name] = {
				'price': 0,
				'type': '',
				'year': '',
				'week': '',
				'day': 255,
				'code': '',
			}
			meal_info = meal.parent
			# meal price
			meal_price = meal_info.find(class_='menu-cell-text-row menu-price-field')
			if meal_price and meal_price.text:
				meal_price_re = price_rgx.search(meal_price.text)
				if meal_price_re:
					self.meals[meal_name]['price'] = int(meal_price_re.group())
			# meal info
			meal_info = meal_info.find(class_='menu-info-button menu-info-button-hover')
			if meal_info:
				self.meals[meal_name]['type'] = meal_info.attrs.get('tipus', '')
				self.meals[meal_name]['year'] = meal_info.attrs.get('ev', '')
				self.meals[meal_name]['week'] = meal_info.attrs.get('het', '')
				self.meals[meal_name]['day'] = int(meal_info.attrs.get('nap', 255))
				self.meals[meal_name]['code'] = meal_info.attrs.get('kod', '')
		# weekdays
		self.weekdays = [day.text[:day.text.index('|')] for day in menu.find_all(class_='menu-days-active')[:5]]

	def find(self, name: str=None, sort_by: str=None, group_by: str=None) -> dict:
		'''
		Filter on meals based on given requirements.
		@param name: [str] Name of the meal
		@param sort_by: [str] Sort meals by this info
		@param group_by: [str] Group meals by this info
		@return Meals that fit for the requirements
		'''
		found_meals = OrderedDict()
		for meal_name, meal_info in self.meals.items():
			if (not name) or (name in meal_name):
				found_meals[meal_name] = meal_info
		if sort_by:
			found_meals = OrderedDict((k,v) for k,v in sorted(found_meals.items(), key=lambda x: x[1][sort_by]))
		if group_by:
			grouped_meals = OrderedDict()
			for k,v in sorted(found_meals.items(), key=lambda x: x[1][group_by]):
				group_by_name = self.get_weekday(v[group_by]) if group_by == 'day' else v[group_by]
				if group_by_name not in grouped_meals:
					grouped_meals[group_by_name] = OrderedDict()
				grouped_meals[group_by_name][k] = v
			found_meals = grouped_meals
		return found_meals

class MenuScraperWeb(_MenuScraperBasic):
	'''
	Online menu parser object.
	Traverse through menu, collect meals and filter by the given requirements.
	'''
	def __init__(self, html_url: str):
		super(MenuScraperWeb, self).__init__()
		self.html_url = html_url

	def parse(self):
		'''
		Parse online html document.
		'''
		self.meals.clear()
		response = requests.get(self.html_url)
		if response.status_code == 200:
			self.collect(response.content)

class MenuScraperLocal(_MenuScraperBasic):
	'''
	Local menu parser object.
	Traverse through menu, collect meals and filter by the given requirements.
	'''
	def __init__(self, html_doc: str):
		super(MenuScraperLocal, self).__init__()
		self.html_doc = html_doc

	def parse(self):
		'''
		Parse local html document.
		'''
		with open(self.html_doc, 'r') as fh:
			html_content = fh.read()
		self.collect(html_content)

class MenuScraperFactory():
	@staticmethod
	def Get(mstype: str) -> object:
		if mstype == 'web':
			return MenuScraperWeb
		if mstype == 'local':
			return MenuScraperLocal
		else:
			raise TypeError("Unknown MenuScraper type {}.".format(mstype))

if __name__ == '__main__':
	menuscraper = MenuScraperFactory.Get('local')(sys.argv[1])
	menuscraper.parse()
	found_meals = menuscraper.find(name='csirkemell', sort_by='price', group_by='day')
	#import pprint
	#pprint.pprint(found_meals, indent=4)
	# print task requirements
	from tabulate import tabulate
	table_meals = []
	for weekday in menuscraper.weekdays:
		if weekday in found_meals:
			for meal_name, meal_info in found_meals[weekday].items():
				table_meals.append([weekday, meal_name, meal_info['price']])
				break
		else:
			table_meals.append([weekday, '-', '-'])
	print(tabulate(table_meals, ['weekday', 'meal', 'price'], tablefmt='fancy_grid'))
