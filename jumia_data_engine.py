	
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import logging

# Configure professional logging for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JumiaPriceScraper:
	"""
	Expert-level Scraper for Jumia Kenya (Smartphones Category).
	Features: Price cleaning, anti-bot delays, metadata extraction, and incremental saving.
	"""
	def __init__(self):
		self.base_url = "https://www.jumia.co.ke/smartphones/"
		self.products = []
		self.session = requests.Session()
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
			"Accept-Language": "en-US,en;q=0.9",
			"Referer": "https://www.google.com/",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
		}

	def clean_price(self, price_str):
		"""Convert 'KSh 15,000' string to integer."""
		if not price_str: return 0
		return int(re.sub(r'[^\d]', '', price_str))

	def scrape_page(self, page_num):
		"""Scrapes a single page of results."""
		url = f"{self.base_url}?page={page_num}#catalog-listing"
		try:
			response = self.session.get(url, headers=self.headers, timeout=20)
			if response.status_code != 200:
				logging.error(f"Page {page_num} unreachable. Status: {response.status_code}")
				return False

			soup = BeautifulSoup(response.text, 'html.parser')
			# Select each product card
			items = soup.find_all('article', class_='prd _fb col c-prd')

			if not items:
				logging.warning(f"No products found on page {page_num}.")
				return False

			for item in items:
				try:
					name = item.find('h3', class_='name').text.strip()
					brand = name.split()[0] # Heuristic for brand extraction
					
					# Prices logic
					current_price_raw = item.find('div', class_='prc').text.strip()
					current_price = self.clean_price(current_price_raw)
					
					old_price_elem = item.find('div', class_='old')
					old_price = self.clean_price(old_price_elem.text.strip()) if old_price_elem else current_price
					
					# Discount calculation
					discount_elem = item.find('div', class_='bdg _dsct _sm')
					discount = discount_elem.text.strip() if discount_elem else "0%"
					
					# Ratings and Reviews
					rating_elem = item.find('div', class_='stars _s')
					rating = rating_elem.text.split()[0] if rating_elem else "0"
					
					reviews_elem = item.find('div', class_='rev')
					reviews_count = re.sub(r'[^\d]', '', reviews_elem.text) if reviews_elem else "0"
					
					link = "https://www.jumia.co.ke" + item.find('a', class_='core')['href']

					self.products.append({
						"Product Name": name,
						"Brand": brand,
						"Current Price": current_price,
						"Old Price": old_price,
						"Discount": discount,
						"Rating": float(rating),
						"Reviews": int(reviews_count),
						"Product Link": link
					})
				except Exception:
					continue # Skip if critical info is missing
			
			return True
		except Exception as e:
			logging.error(f"Request error on page {page_num}: {e}")
			return False

	def run(self, target=3000):
		"""Pagination loop with incremental saving."""
		page = 1
		while len(self.products) < target:
			logging.info(f"Scraping Jumia Page {page} | Items: {len(self.products)}...")
			
			success = self.scrape_page(page)
			if not success:
				logging.warning("Stopping extraction due to page error.")
				break
			
			# --- INCREMENTAL SAVE ---
			# Save progress after every single page
			self.export_data()
			logging.info(f"Progress saved to CSV at page {page}")
			
			page += 1
			# Strategic Random Delay (Jittering)
			time.sleep(random.uniform(2, 5))
		
		logging.info("Extraction session finished.")

	def export_data(self):
		"""Deduplication and CSV export."""
		if not self.products:
			return
			
		df = pd.DataFrame(self.products)
		# Drop duplicates to keep only unique product/price combinations
		df = df.drop_duplicates(subset=['Product Name', 'Current Price'])
		df.to_csv("jumia_kenya_prices.csv", index=False)

if __name__ == "__main__":
	scraper = JumiaPriceScraper()
	scraper.run(target = 3000)

