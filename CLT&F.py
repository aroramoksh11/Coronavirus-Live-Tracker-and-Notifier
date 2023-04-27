import requests
from bs4
import BeautifulSoup
from plyer
import notification
import time

# Set the URL of the website to scrape
url = 'https://www.worldometers.info'

# Set the refresh time interval in seconds
refresh_interval = 1800  # 30 minutes

# Scrape the website and parse the HTML using BeautifulSoup
def scrape_website():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# Extract the relevant information from the website
def extract_info(soup):
    table = soup.find('table', {'id': 'main_table_countries_today'})
    rows = table.tbody.find_all('tr')
    countries = {}
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            country_name = cols[1].text.strip()
            total_cases = cols[2].text.strip()
            total_deaths = cols[4].text.strip()
            total_recovered = cols[6].text.strip()
            active_cases = cols[8].text.strip()
            countries[country_name] = {
                'Total Cases': total_cases,
                'Total Deaths': total_deaths,
                'Total Recovered': total_recovered,
                'Active Cases': active_cases
            }
    return countries

# Notify the user with the latest information
def notify_user(countries):
    for country, data in countries.items():
        message = f"{country}: {data['Total Cases']} cases, {data['Total Deaths']} deaths, {data['Active Cases']} active cases"
        notification.notify(
            title='Coronavirus Live Tracker',
            message=message,
            timeout=10
        )

# Run the live tracker and notifier
if __name__ == '__main__':
    while True:
        soup = scrape_website()
        countries = extract_info(soup)
        notify_user(countries)
        time.sleep(refresh_interval)
