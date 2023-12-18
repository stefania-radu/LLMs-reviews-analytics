# Web-scraping from booking.com

Scrape info from booking.com for a list of hotels.

The .json and .csv files already contain the scraped data for The [Social Hub hotel](https://www.booking.com/hotel/nl/the-social-hub-groningen.en.html) in Groningen.

## Usage

1. Install the requirements from `requirements.txt`.
2. Write the link of the hotel for which you want to scrape data in `hotel_link.txt`. For more hotels, write each link on a new line. Only booking.com links are supported. 
Example link: https://www.booking.com/hotel/nl/the-social-hub-groningen.en.html
3. Run `python scrape_booking.py`.
4. The script will generate 2 files:
    - A .json file which contains overall information about the hotel:
        - hotel_name (string) = the name of the hotel
        - hotel_link (string) = the booking.com link for the hotel
        - address (string) = the address of the hotel
        - scraping_date (string) = the date + time of the scraping in the format dd-mm-yy_hh-mm
        - nr_reviews (int) = the total number of reviews
        - overall_score (float) = the overall score computed by booking.com

    - A .csv file which contains the reviews dataset. Each entry corresponds to one user.
        - review_title (string) = the title of the review
        - review_date (string) = the date when the review was posted
        - reviewer_country (string) - the country of the reviewer
        - room_type (string) = the type of room as defined by each hotel (example: Deluxe King Room)
        - party_size (string) = the type of group traveling (example: couple, family)
        - nr_nights (int) = the number of nights stayed in the hotel
        - date_stay (string) = the starting date of the stay in the hotel
        - review_score (float) = the score given by the reviewer
        - review_great (string) = the text of the positive review. If missing, then N/A.
        - review_poor (string) = The text of the negative review. If missing, then N/A.
        - hotel_response_bool (bool) = Whether or not the hotel has responded to the review.


*Disclaimer: We do not store any personal information about the users.* 