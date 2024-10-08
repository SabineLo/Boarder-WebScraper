#Goal is to scrape data from boarder line for a month and then use react pluz django to show it
#but first break it down to small parts
#get the data save it and show it on plotlib and other python extension libraries
#Improving this
#Able to learn from last one and instead we are doing this
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
#works for tables
#IT WORKKSSS YESSSSSSSSS :DDDD YIPEEE
options = Options()

driver = webdriver.Chrome(options=options)

def click_ready_lane_tab(driver):
    """Click the 'Ready Lane' tab."""
    try:
        ready_lane = WebDriverWait(driver, 75).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="test2"]/li[2]/a'))
        )
        print("Clicking the 'Ready Lane' tab...")
        ready_lane.click()

        # Wait for the content to load
        time.sleep(20)  # Optional: wait a bit longer for the content to fully load

    except Exception as e:
        print(f"An error occurred while clicking the 'Ready Lane' tab: {e}")

def locate_table(driver):
    # Navigate to the URL
    driver.get('https://bwt.cbp.gov/details/09250401/POV')

    click_ready_lane_tab(driver)
    ready_table = WebDriverWait(driver,75).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="test2"]/li[2]/a'))
        )
 
    ready_table.click()

    time.sleep(20)
    try:
        # Wait for the table body to load after switching to the Ready Lane tab
        tbody = WebDriverWait(driver, 75).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sectionB"]/div/table'))
        )

        print("Ready Lane table located successfully.")

        data = []
        for tr in tbody.find_elements(By.XPATH, './/tr'):
            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
            if row:  # Check if row is not empty
                data.append(row)
        print(data)

        # Save data to CSV
        with open('borderData.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Today (min)', 'Average (min)'])
            writer.writerows(data)
        print("Data saved to borderData.csv.")

    except Exception as e:
        print(f"An error occurred while locating the table: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after use


if __name__ == '__main__':
    locate_table(driver)

