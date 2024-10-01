import csv
import time
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

def normalize_location(input_str):
    return unidecode(input_str).lower()
    
#Enter your credentials
username = ''
password = ''

#This is how your link should be like the example is given here.
search_url = 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%22338922%22%5D&keywords=software%20productivity%20strategists%20inc&origin=FACETED_SEARCH&sid=KGY'

parsed_url = urlparse(search_url)
query_params = parse_qs(parsed_url.query)
company_name = query_params.get('keywords', [''])[0] 
company_name = company_name.strip().lower().replace(' ', '_')

#Give the path to your chromedriver file
path = ''  

description_to_filter = input("Enter the description to filter by (or type 'no' or 'n' to skip description filtering): ").strip().lower()
location_to_filter = normalize_location(input("Enter the location to filter by (or type 'no' or 'n' to skip location filtering): ").strip().lower())

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

try:
    driver.get('https://www.linkedin.com/login')

    # Enter username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username_field.send_keys(username)

    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

   
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'global-nav-search'))
    )
    driver.get(search_url)

    # Wait for the main content to load
    main_content = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'main'))
    )

    # Prepare CSV file for writing
    csv_filename = f"{company_name}_linkedin_data.csv"
    csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'Description', 'Location'])

    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()

    while True:
        # Extract data for each person
        results = main_content.find_elements(By.CSS_SELECTOR, 'li.reusable-search__result-container')
        for result in results:
            try:
                name_element = result.find_element(By.CSS_SELECTOR, 'a.app-aware-link span[aria-hidden="true"]')
                name = name_element.text
            except:
                name = 'N/A'
            
            try:
                location_element = result.find_element(By.CSS_SELECTOR, 'div.entity-result__secondary-subtitle')
                location = normalize_location(location_element.text)
            except:
                location = 'N/A'
            
            try:
                description_element = result.find_element(By.CSS_SELECTOR, 'div.entity-result__primary-subtitle')
                description = description_element.text
            except:
                description = 'N/A'
            
            # Apply filters
            if (description_to_filter == 'no' or description_to_filter == 'n' or description_to_filter in description.lower()) and (location_to_filter == 'no' or location_to_filter == 'n' or location_to_filter in location):
                # Write data to CSV
                csv_writer.writerow([name, description, location])
                print(f'Name: {name}, Description: {description}, Location: {location}')

        # Click on the next button
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view.artdeco-pagination__button.artdeco-pagination__button--next'))
            )
            next_button.click()
        except:
            break

        time.sleep(5)  
        actions.send_keys(Keys.END).perform()

        main_content = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'main'))
        )

    # Close CSV file
    csv_file.close()

finally:
    driver.quit()
