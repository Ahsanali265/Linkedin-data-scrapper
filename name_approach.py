from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from unidecode import unidecode

# LinkedIn credentials
username = 'ahsanasghar2024@gmail.com'
password = 'Ahsan2024@'

path = r'E:\chromedriver-win64\chromedriver.exe'  

company_name = input("Enter the company name to search for: ").strip().lower()
description_to_filter = input("Enter the description to filter by (or type 'no' or 'n' to skip description filtering): ").strip().lower()
location_to_filter = unidecode(input("Enter the location to filter by (or type 'no' or 'n' to skip location filtering): ").strip().lower())

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

    # Wait for login to complete
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, 'global-nav-search'))
    )

    search_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-global-typeahead__input'))
    )
    search_field.send_keys(company_name)
    search_field.send_keys(Keys.RETURN)

    # Wait for search results to load and select the company page
    company_page = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.app-aware-link span[aria-hidden="true"]'))
    )
    company_page.click()

    employees_section = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/search/results/people/?currentCompany"] span.t-normal.t-black--light.link-without-visited-state.link-without-hover-state'))
    )

    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)  

    actions = ActionChains(driver)
    actions.move_to_element(employees_section).perform()
    employees_section.click()

    # Wait for the main content to load
    main_content = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.reusable-search__entity-result-list.list-style-none'))
    )

    # Prepare CSV file for writing
    csv_filename = f"{company_name.replace(' ', '_')}_linkedin_data.csv"
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
                name_element = result.find_element(By.CSS_SELECTOR, 'a.app-aware-link')
                name = name_element.text
            except:
                name = 'N/A'
            
            try:
                description_element = result.find_element(By.CSS_SELECTOR, 'div.entity-result__primary-subtitle.t-14.t-black.t-normal')
                description = description_element.text
            except:
                description = 'N/A'
            
            try:
                location_element = result.find_element(By.CSS_SELECTOR, 'div.entity-result__secondary-subtitle.t-14.t-normal')
                location = unidecode(location_element.text)
            except:
                location = 'N/A'
            
            # Apply filters
            if (description_to_filter == 'no' or description_to_filter == 'n' or description_to_filter in description.lower()) and (location_to_filter == 'no' or location_to_filter == 'n' or location_to_filter in location.lower()):
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
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.reusable-search__entity-result-list.list-style-none'))
        )

    csv_file.close()

finally:
    driver.quit()
