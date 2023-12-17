from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import re
import pandas as pd
import json
from datetime import datetime
import uuid
import logging
import time


def get_nr_reviews(nr_reviews_text):
    # Extract the number of reviews from the given text
    match = re.search(r'\(([\d,]+)\)', nr_reviews_text)
    return int(match.group(1).replace(',', '')) if match else 0


def scrape_hotel_info(hotel_link):
    # Scrape hotel information from the given hotel link
    logging.info(f"Scraping hotel info from {hotel_link}")
    
    response = requests.get(hotel_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    hotel_name_tag = soup.find('h2', class_='pp-header__title')
    hotel_name = hotel_name_tag.get_text(strip=True) if hotel_name_tag else 'N/A'

    address_tag = soup.find('span', class_='hp_address_subtitle')
    address = address_tag.get_text(strip=True) if address_tag else 'N/A'

    nr_reviews_text = soup.find_all('li', class_='d37611a2e0')[13].get_text(strip=True) # 13 is for the nr reviews element
    nr_reviews = get_nr_reviews(nr_reviews_text) if nr_reviews_text else 0

    overall_score = float(soup.find("div", class_="a3b8729ab1 d86cee9b25").get_text(strip=True).split()[0])
    
    return hotel_name, address, nr_reviews, overall_score


def get_review_title(review):
    # Get the title of the review
    try:
        title_tag = review.find('h3', class_='c-review-block__title c-review__title--ltr')
        return title_tag.get_text(strip=True)
    except:
        return 'N/A'


def get_review_date(review):
    # Get the date of the review
    try:
        review_date =  review.find('span', class_='c-review-block__date').get_text(strip=True)
        review_date = datetime.strptime(review_date, '%B %Y').strftime('%m-%Y')
    except:
        review_date = 'N/A'
    return review_date


def get_reviewer_country(review):
    # Get the country of the reviewer
    try:
        return review.find('span', class_='bui-avatar-block__subtitle').get_text(strip=True)
    except:
        return "N/A"


def get_room_type(review):
    # Get the room type of the review
    try:
        return review.find('div', {'data-component': 'ugcs/shared/room-info'}).find('div', {"class": "bui-list__body"}).get_text(strip=True)
    except:
        return "N/A"

def get_party_size(review):
    # Get the party size of the review
    try:
        party_size_tag = review.find('ul', class_='bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row')
        party_size = party_size_tag.find('div', class_='bui-list__body').get_text(strip=True) if party_size_tag else 'N/A'
    except:
        party_size = "N/A"
        
    return party_size


def get_nr_nigths(review):
    # Get the number of nights stayed in the hotel
    try:
        nr_nights_text = review.find('ul', {"class":'bui-list bui-list--text bui-list--icon bui_font_caption c-review-block__row c-review-block__stay-date'}).find('div', class_='bui-list__body').get_text(strip=True)
        nr_nights_match = re.search(r'(\d+)\s+night', nr_nights_text)
        nr_nights = int(nr_nights_match.group(1)) if nr_nights_match else 0
    except:
        nr_nights = "N/A"
        
    return nr_nights


def get_date_stay(review):
    # Get the date of stay 
    date_stay_text = review.find('span', class_='c-review-block__date').get_text(strip=True)
    try:
        date_stay = datetime.strptime(date_stay_text, '%B %Y').strftime('%m-%Y')
    except ValueError:
        date_stay = 'N/A'

    return date_stay


def get_review_score(review):
    # Get the score of the review
    try:
        return review.find('div', class_='bui-review-score c-score').find('div', class_='bui-review-score__badge').get_text(strip=True)
    except:
        return "N/A"

def get_review_great(review):
    # Get the "great" part of the review
    review_great_tag = review.find('svg', class_='bk-icon -iconset-review_great c-review__icon')
    if review_great_tag:
        review_poor_text_tag = review_great_tag.find_next('span', class_='c-review__body')
        if review_poor_text_tag:
            return review_poor_text_tag.get_text(strip=True)
    return 'N/A'


def get_review_poor(review):
    # Get the "poor" part of the review
    review_poor_tag = review.find('svg', class_='bk-icon -iconset-review_poor c-review__icon')
    if review_poor_tag:
        review_poor_text_tag = review_poor_tag.find_next('span', class_='c-review__body')
        if review_poor_text_tag:
            return review_poor_text_tag.get_text(strip=True)
    return 'N/A'


def get_hotel_response_bool(review):
    # Check if the hotel has responded to the review
    try:
        return bool(review.find('div', class_='c-review-block__response__title'))
    except:
        return "N/A"

def scrape_hotel_reviews(hotel_link):
    # Scrape hotel reviews from the given hotel link
    logging.info(f"Scraping hotel reviews from {hotel_link}")

    hotel_link = hotel_link + "#tab-reviews"

    driver = webdriver.Chrome()
    driver.get(hotel_link)
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews_data = []

    page_nr = 0

    while True:

        logging.info(f"Page {page_nr}")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_blocks = soup.find_all('div', class_='c-review-block')

        for review in review_blocks:
        
            review_title = get_review_title(review)
            review_date = get_review_date(review)
            reviewer_country = get_reviewer_country(review)
            room_type = get_room_type(review)
            party_size = get_party_size(review)
            nr_nights = get_nr_nigths(review)
            date_stay = get_date_stay(review)
            review_score = get_review_score(review)

            review_great = get_review_great(review)
            review_poor = get_review_poor(review)

            hotel_response_bool = get_hotel_response_bool(review)
            # hotel_response_text = review.find('div', class_='hotel-response-text-class').get_text(strip=True) if hotel_response_bool else ''

            reviews_data.append({
                'review_title': review_title,
                'review_date': review_date,
                'reviewer_country': reviewer_country,
                'room_type': room_type,
                'party_size': party_size,
                'nr_nights': nr_nights,
                'date_stay': date_stay,
                'review_score': review_score,
                'review_great': review_great,
                'review_poor': review_poor,
                'hotel_response_bool': hotel_response_bool,
                # 'hotel_response_text': hotel_response_text
            })

        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, "a.pagenext")
            driver.execute_script("arguments[0].click();", next_page_button)
            page_nr += 1
            time.sleep(1)  # Wait for page to load
        except NoSuchElementException:
            break  # Break the loop if "next page" button is not found


    driver.quit()

    return reviews_data


def create_csv(reviews_data, hotel_name, scraping_date, random_id):
    # Create a CSV file for the scraped reviews data
    logging.info(f"Creating CSV file for hotel: {hotel_name}")
    df = pd.DataFrame(reviews_data)
    filename = f"{random_id}_{hotel_name}_{scraping_date}.csv"
    df.to_csv(filename, index=False)


def create_json(hotel_info, scraping_date, random_id):
    # Create a JSON file for the hotel information
    logging.info(f"Creating JSON file for hotel: {hotel_info['hotel_name']}")
    filename = f"{random_id}_{hotel_info['hotel_name']}_{scraping_date}.json"
    with open(filename, 'w') as f:
        json.dump(hotel_info, f)


def main():
    # Main function to execute the scraping process
    
    logging.basicConfig(level=logging.INFO)
    
    with open('hotel_links.txt', 'r') as file:
        hotel_links = [line.strip() for line in file.readlines()]

    scraping_date = datetime.now().strftime('%d-%m-%Y_%H-%M')
    random_id = str(uuid.uuid4())

    for link in hotel_links:
        hotel_name, address, nr_reviews, overall_score = scrape_hotel_info(link)
        reviews_data = scrape_hotel_reviews(link)
        create_csv(reviews_data, hotel_name, scraping_date, random_id)
        hotel_info = {
            'hotel_name': hotel_name,
            'hotel_link': link,
            'address': address,
            'scraping_date': scraping_date,
            'nr_reviews': nr_reviews,
            'overall_score': overall_score
        }
        create_json(hotel_info, scraping_date, random_id)

if __name__ == "__main__":
    main()
