from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
import time

# Path to the ChromeDriver
driver_path = '/Users/sabbirahmad/Desktop/chromedriver'

# Function to log messages to the console
def log(message):
    print(f"[LOG] {message}")

# Function to check if an element exists on the page
def element_exists(driver, by, value):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((by, value)))
        return True
    except:
        return False

# Function to click the confirm button on a confirmation popup
def click_confirm_button(driver):
    retries = 3
    while retries > 0:
        try:
            log("Waiting for confirmation popup")
            confirmation_popup = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "layui-layer-btn-"))
            )

            log("Found Confirm button on confirmation popup, clicking it")
            confirm_button = confirmation_popup.find_element(By.CLASS_NAME, "layui-layer-btn0")
            confirm_button.click()
            return
        except StaleElementReferenceException:
            log("Stale element reference exception, retrying")
            retries -= 1
            time.sleep(1)
    log("Failed to click Confirm button after retries")

# Function to wait for a given number of seconds with a countdown display
def wait_with_countdown(seconds):
    log(f"Waiting for {seconds // 60} minutes and {seconds % 60} seconds before next iteration")
    while seconds:
        mins, secs = divmod(seconds, 60)
        countdown = f"{mins:02d}:{secs:02d}"
        print(countdown, end='\r')
        # print(countdown, end='', flush=True)
        time.sleep(1)
        seconds -= 1
    print(" " * len(countdown), end='\r')  # Clear the line after countdown is complete

# Function to handle the confirmation popup after logging in
def handle_confirmation(driver):
    try:
        log("Checking for confirmation popup")
        confirmation_popup = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "layui-layer-btn-c"))
        )

        log("Found Confirm button on confirmation popup, clicking it")
        confirm_button = confirmation_popup.find_element(By.TAG_NAME, "a")
        confirm_button.click()
    except Exception as e:
        log(f"An error occurred while handling confirmation popup: {e}")

# Function to retrieve the countdown timer's minute value from the webpage
def get_countdown_minutes(driver):
    try:
        # Before taking the countdown time
        driver.refresh()
        time.sleep(3)

        countdown_timer = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#time i"))
        )
        countdown_text = countdown_timer.text
        minutes, _ = countdown_text.split(':')
        return int(minutes)
    except Exception as e:
        log(f"An error occurred while retrieving countdown timer: {e}")
        return None

def get_countdown_seconds(driver):
    try:
        countdown_timer = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#time i"))
        )
        countdown_text = countdown_timer.text
        _, seconds = countdown_text.split(':')
        return int(seconds)
    except Exception as e:
        log(f"An error occurred while retrieving countdown timer: {e}")
        return None

# Function to start the betting process
def start_betting(driver):
    try:
        # Login
        log("Navigating to the login page")
        url = 'https://www.luckyau.org/?a=login'
        driver.get(url)

        # Wait for the username input field
        log("Waiting for the login page to load")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        log("Login page loaded, entering username")
        username_input.send_keys("skmusarraf")  # Enter the provided username

        # Find the password input and enter the password
        log("Entering password")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("96979899")  # Enter the provided password

        # Submit the login form
        log("Submitting the login form")
        password_input.submit()

        # Handle confirmation popup after logging in
        handle_confirmation(driver)

        # Click on "5 of 11"
        log("Selecting '5 of 11' game")
        game_5_of_11 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@onclick, '?a=game&gameid=47')]"))
        )
        game_5_of_11.click()

        # Click on VIP1
        log("Selecting VIP1 room")
        vip1_room = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.jump_room"))
        )
        vip1_room.click()

        # Refresh the page before checking the countdown and take 3 sec sleep.
        
        # driver.refresh()
        # time.sleep(3)

        while True:
            log("Refreshing the page")
            driver.refresh()
            time.sleep(5)
            # Wait until the countdown timer shows 4 minutes
            log("Checking countdown timer")
            countdown_minutes = get_countdown_minutes(driver)
            countdown_seconds = get_countdown_seconds(driver)
            while countdown_minutes is not None and countdown_minutes != 4:
                log(f"Current countdown minute is {countdown_minutes}, {countdown_seconds} waiting for it to reach 4")
                if countdown_minutes > 4:
                    wait_time = countdown_seconds
                    log(f"Sleeping for {wait_time // 60} minutes and {wait_time % 60} seconds")
                    wait_with_countdown(wait_time)
                elif countdown_minutes < 4:
                    wait_time = (countdown_minutes * 60) + countdown_seconds + 57
                    log(f"Sleeping for {wait_time // 60} minutes and {wait_time % 60} seconds")
                    wait_with_countdown(wait_time)

                countdown_minutes = get_countdown_minutes(driver)

            log("Starting a new betting iteration")

            # Betting BIG
            log("Betting BIG")

            try:
                # Find the element corresponding to the BIG option
                big_option_div = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='tab n2 num']"))
                )
                big_option = big_option_div.find_element(By.CSS_SELECTOR, "a.C_1DA")

                # Click on the BIG option
                big_option.click()

                # Find the input field for the betting amount
                bet_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "money"))
                )

                # Enter the desired amount (e.g., '2')
                bet_amount = '2'
                bet_input.clear()
                bet_input.send_keys(bet_amount)

                # Find the bet button and click on it
                bet_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "send"))
                )
                bet_button.click()

                # Handle any confirmation popups, if necessary
                click_confirm_button(driver)
            except Exception as e:
                log(f"An error occurred while betting BIG: {e}")

            # Refresh the page before betting on SMALL
            log("Refreshing the page")
            driver.refresh()

            # Betting SMALL
            log("Betting SMALL")

            try:
                # Find the element corresponding to the SMALL option
                small_option_div = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='tab n2 num']"))
                )
                small_option = small_option_div.find_element(By.XPATH, "//i[contains(text(), 'SMALL')]")

                # Click on the SMALL option
                small_option.click()

                # Find the input field for the betting amount
                bet_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "money"))
                )

                # Enter the desired amount (e.g., '1')
                bet_amount = '1'
                bet_input.clear()
                bet_input.send_keys(bet_amount)

                # Find the bet button and click on it
                bet_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "send"))
                )
                bet_button.click()

                # Handle any confirmation popups, if necessary
                click_confirm_button(driver)
            except Exception as e:
                log(f"An error occurred while betting SMALL: {e}")

            log('-------------------------')
            # After completing betting, check the current time and wait current time + 57 seconds
            log("Checking countdown timer after betting")
            countdown_minutes = get_countdown_minutes(driver)
            countdown_seconds = get_countdown_seconds(driver)
            if countdown_minutes is not None:
                wait_time = countdown_minutes * 60 + countdown_seconds + 57
                log(f"Sleeping for {wait_time // 60} minutes and {wait_time % 60} seconds")
                wait_with_countdown(wait_time)

    except WebDriverException as e:
        if 'disconnected: not connected to DevTools' in str(e):
            log("Chrome disconnected, restarting the browser")
            return False
        else:
            log(f"An error occurred: {e}")
            driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging
            return False
    except Exception as e:
        log(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")  # Save a screenshot for debugging
        return False

    finally:
        # Close the browser after finishing the task
        log("Closing the browser")
        driver.quit()

    return True

# Initialize the Chrome driver using ChromeService
service = ChromeService(executable_path=driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
options.add_argument("--v=1")

while True:
    driver = webdriver.Chrome(service=service, options=options)
    success = start_betting(driver)
    if not success:
        log("Restarting the betting process")
        time.sleep(5)
    else:
        break
