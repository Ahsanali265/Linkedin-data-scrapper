# Linkedin-data-scrapper
Scrape Company Employee Information Using Selenium

This Python script automates the process of logging into LinkedIn, searching for people associated with a specific company, and extracting their names, descriptions, and locations into a CSV file. It uses the Selenium library for web automation and the Unidecode library for normalizing text.


# Prerequisites
Python 
Selenium library
Unidecode library
Chrome browser
ChromeDriver (must have and must be compatible with your Chrome browser version)

# What the Script Does
The script navigates to the LinkedIn login page and logs in using the provided credentials.
It then navigates to a predefined search URL to look for people associated with a specific company.
The script scrolls through the search results, extracting the name, description, and location of each person.
It filters the extracted data based on the user inputs for description and location.
The filtered data is written to a CSV file named after the company.
The script handles pagination to ensure all search results are processed.
The CSV file is saved in the same directory as the script, and the WebDriver session is terminated.

# Notes
Ensure your LinkedIn account has access to the necessary search features.
Using automation tools on LinkedIn might violate LinkedIn's terms of service, so proceed with caution and consider the ethical implications.
Your account could be ban if you make too much request or you have to pass captcha 

# About Files
There are two files one is a script in which link is required and the other one you have two filters and other one is you have to give company name and its not gonna work sometime.


