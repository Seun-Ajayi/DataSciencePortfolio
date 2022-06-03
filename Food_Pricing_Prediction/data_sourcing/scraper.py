import requests
import argparse
from bs4 import BeautifulSoup
import csv
import logging

logging.root.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='USD rates scraper')
    parser.add_argument(
        "--output_file_name",
        type=str,
        help="Name of output file",
    )

    parser.add_argument(
        '--years',
        nargs='+',
        help='year of the USD rates you need as a list'
    )

    return parser.parse_args()


def get_html_data(years):
    data = []
    for year in years:
        url = f"https://www.exchangerates.org.uk/USD-NGN-spot-exchange-rates-history-{year}.html"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        data.append(soup)
    return data


def get_currency_data(year):
    soup = get_html_data(year)

    currency = []
    curr_date = []

    for data in soup:
        conversion_data = data.find_all('td', attrs={'colspan': '5'})

        for store in conversion_data:
            rate = (store.text.split())[-1]
            get_year = store.text.split()
            year_data = get_year[-3] + ' ' + (get_year[-2])[0:-1]

            currency.append(rate)
            curr_date.append(year_data)
    return currency, curr_date


def scrape(output_file_name, year):
    logging.info("Writing to file...")

    with open(output_file_name, 'w') as csv_file:
        headers = ['Dollar Rate', 'Date']
        writer = csv.DictWriter(csv_file, delimiter='\t', fieldnames=headers)
        writer.writeheader()

        dollar_rate, date = get_currency_data(year)

        for (rate, curr_date) in zip(dollar_rate, date):
            writer.writerow({
                headers[0]: rate,
                headers[1]: curr_date,
            })
    logging.info(f"USD rates successfully written")

    logging.info(f"Scraping done.")


if __name__ == '__main__':
    logging.info("--------------------------------------")
    logging.info("Starting scraping...")
    logging.info("--------------------------------------")

    args = parse_args()

    scrape(args.output_file_name, args.years)
