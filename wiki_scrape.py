import requests
from bs4 import BeautifulSoup
import os


def scrape_wiki(searched):
    """
        Scrapes wikipedia search results based on user input and saves the data to a text file.

        Args:
        - searched (str): The term to search for on wikipedia.

        Returns:
        - None
        """

    if searched == ' ':
        print("Error: Please enter a search term.")
        scrape_wiki(input("Enter your search: ").replace(' ', '_'))

    url = f'https://en.wikipedia.org/wiki/{searched}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    try:
        soup = BeautifulSoup(content, 'html.parser')

        scraped = soup.find('div', {'id': 'mw-content-text'}).find_all('p')

        first_p = scraped[0].text
        second_p = scraped[1].text
        third_p = scraped[2].text

    except Exception as e:
        print(f"Error: {e}")
        return

    data = first_p + '\n' + second_p + '\n' + third_p

    # your path
    filename = f"C:/Users/abdul/Downloads/{searched}.txt"

    with open(filename, "w") as file:
        file.write(data)

    print(f"Output saved to {filename}.")

    os.startfile(filename)


scrape_wiki(input("Enter your search: ").replace(' ', '_'))
