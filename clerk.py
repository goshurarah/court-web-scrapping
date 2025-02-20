import logging
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import winsound
import re 
import requests
import os 
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random

chrome_driver_path = 'chromedriver.exe'

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# # Run in headless mode
# chrome_options.add_argument("--headless")  # Add this line for headless mode
# chrome_options.add_argument("--disable-gpu")  # This is necessary for headless mode on Windows
# chrome_options.add_argument("--no-sandbox")  # For some environments, like CI/CD

chrome_options.add_argument(f"executable_path={chrome_driver_path}")
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("window.debugger = function() {};")

# Bypass detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
        Object.defineProperty(window, 'chrome', { get: () => ({ runtime: {} }) });
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) =>
            parameters.name === 'notifications' ? Promise.resolve({ state: 'granted' }) : originalQuery(parameters);
    """
})

try:
    # Open the website
    driver.get("https://clerkconnect.com/civilinquiry/ebr")
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")

    # Login process
    try:
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys("kris@purplehomessolutions.com")

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys("Nicole4588!")

        # Simulate pressing Enter key to submit the form
        password_field.send_keys(Keys.RETURN)
        print("Login submitted successfully.")
    except TimeoutException as e:
        raise

    # Handle the modal if the close button exists
    try:
        modal_close_button = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//button[@type="button" and @ng-click="close()"]'))
        )
        if modal_close_button:
            modal_close_button.click()
            print("Error Modal closed successfully.")
    except TimeoutException:
        print("Error Modal close button not found, continuing...")

    try:
        print("On apply filter page")
        # Select search type dropdown
        selectedSearchType = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@ng-model="controller.vm.selectedSearchType"]'))
        )
        selectedSearchType.click()
        suit_cause_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//option[text()="Suit Cause"]'))
        )
        suit_cause_option.click()
        screen = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bodyBorder")))
        screen.click()
        print("Search type selected")


        # Select suit cause dropdown
        selectedSuitCause = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//select[@ng-model="controller.vm.selectedSuitCause"]'))
        )
        selectedSuitCause.click()
        executory_process_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//option[text()="EP-Executory Process"]'))
        )
        executory_process_option.click()
        screen = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bodyBorder")))
        screen.click()
        print("Suit cause selected")

        # Select From and TO date
        from_date = "12/10/2024"
        to_date = "12/19/2024"

        # Wait and interact with the "From Date" input field
        from_date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//md-datepicker[@ng-model="controller.vm.fromDate"]//input'))
        )
        driver.execute_script("arguments[0].removeAttribute('readonly')", from_date_input)  # Remove 'readonly' if present
        from_date_input.clear()  # Clear existing value
        from_date_input.send_keys(from_date)
        print(f"From Date: {from_date} selected")

        # Wait and interact with the "To Date" input field
        to_date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//md-datepicker[@ng-model="controller.vm.toDate"]//input'))
        )
        driver.execute_script("arguments[0].removeAttribute('readonly')", to_date_input)  # Remove 'readonly' if present
        to_date_input.clear()  # Clear existing value
        to_date_input.send_keys(to_date)
        print(f"To Date: {to_date} selected")

        # Wait for the "Search" button to become clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@ng-click="controller.search()"]'))
        )
        # Use ActionChains to hover and mimic human-like behavior
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(-5, 5), random.randint(-5, 5)).perform()  # Simulate slight jitters
        actions.send_keys(Keys.TAB).perform()  # Tab to focus on elements naturally
        actions.click(search_button).perform()
        print("Search button clicked")


        time.sleep(500)
       
    except TimeoutException as e:
        raise Exception("Error") from e

finally:
    print("Finally closed")
    driver.quit()