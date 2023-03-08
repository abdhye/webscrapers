import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import os


def scrape_amazon_results(search_term, region='in', num_pages=1):
    """
    Scrapes Amazon search results based on user input and saves the data to a CSV file.

    Args:
    - search_term (str): The term to search for on amazon.
    - region (str): The amazon region to search (default: 'in').
    - num_pages (int): The number of search result pages to scrape (default: 1).

    Returns:
    - None
    """

    # Input validation
    if search_term == ' ':
        print("Error: Please enter a search term.")
        scrape_amazon_results(input("Enter your search: ").replace(' ', '+'))

    data = []

    for page in range(1, num_pages + 1):
        url = f'https://www.amazon.{region}/s?k={search_term}&page={page}&ref=nb_sb_noss'
        # print(url)
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        try:
            time.sleep(5)
            listings = soup.find_all(
                'div', {'data-component-type': 's-search-result'})
            if not listings:
                raise ValueError(
                    f"No search results found for '{search_term}'")

            page_data = [{'Title': list.find('span', {'class': 'a-size-medium'}).text.strip() if list.find('span', {'class': 'a-size-medium'}) else 'No title found',
                          'Price': list.find('span', {'class': 'a-price-whole'}).text.strip() if list.find('span', {'class': 'a-price-whole'}) else 'No price found',
                          'Rating': list.find('span', {'class': 'a-icon-alt'}).text.strip() if list.find('span', {'class': 'a-icon-alt'}) else 'No ratings found',
                          'Image URL': list.find('img', {'class': 's-image'}).get('src') if list.find('img', {'class': 's-image'}) else 'No image found'}
                         for list in listings]

            data.extend(page_data)

            print(
                f"Scraped {len(data)} search results for '{search_term}' from amazon.{region}")

        except Exception as e:
            print(
                f"Error scraping search results for '{search_term}' from amazon.{region}: {str(e)}")

    df = pd.DataFrame(data)

    # put your path here
    csv_filepath = f'C:/Users/abdul/Downloads/{search_term}.csv'

    df.to_csv(csv_filepath, index=False)

    os.startfile(csv_filepath)


scrape_amazon_results(input("Enter your search: ").replace(' ', '+'))
