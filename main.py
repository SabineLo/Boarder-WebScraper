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
from selenium.webdriver.chrome.service import Service
import csv
from datetime import datetime
import time
import schedule

#works for tables
#IT WORKKSSS YESSSSSSSSS :DDDD YIPEEE
chrome_options = Options()


driver_service = Service('path/to/chromedriver')  # Adjust the path as necessary
driver = webdriver.Chrome(options=chrome_options)

def click_ready_lane_tab(driver):
    """Click the 'Ready Lane' tab.//*[@id="test2"]/li[2]/a"""
    try:
        ready_lane = WebDriverWait(driver, 90).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="test"]/li[2]/a'))
        )
        print("Clicking the 'Ready Lane' tab...")
        ready_lane.click()

        # Wait for the content to load
        time.sleep(30)  

    except Exception as e:
        print(f"An error occurred while clicking the 'Ready Lane' tab: {e}")

def locate_table(driver):
    # Navigate to the URL
    driver.get('https://bwt.cbp.gov/details/09250401/POV')

    click_ready_lane_tab(driver)
    ready_table = WebDriverWait(driver,90).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="test2"]/li[2]/a'))
        )
 
    ready_table.click()

    time.sleep(30)
    try:
        # Wait for the table body to load after switching to the Ready Lane tab
        tbody = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sectionB"]/div/table'))
        )

        print("Ready Lane table located successfully.")

        data = []
        for tr in tbody.find_elements(By.XPATH, './/tr'):
            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
            if row:  # Check if row is not empty
                row.insert(0,datetime.now().strftime('%Y-%m-%d'))
                data.append(row)

        print(data)

        # Save data to CSV make it save every time it is
        with open('borderData.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell()== 0: #if the file is empty/no header
                writer.writerow(['Date','Time', 'Today (min)', 'Average (min)'])
            writer.writerows(data)
        print("Data saved to borderData.csv.")

    except Exception as e:
        print(f"An error occurred while locating the table: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after use


#Need to implement pandas
#First make it run every hour, 2nd save the data, from first day save all the info,
#graph the data from the first two days

#Get data from telemundo and mix it together 2nd step
#Purpose to discover best time to cross discover what time is highest make infrences, why its higher because weekend or something

def runs_my_script():
    try:
        locate_table(driver)
    except Exception as e:
        print(f"An error occured {e}")


if __name__ == '__main__':
    #Makes it so its runs every hour me thinks
    #if not work then just do manually 
    schedule.every().day.at("23:10").do(runs_my_script)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Script STOPPED BY ME")

#You can manually stop the script by interrupting it (Ctrl + C in the terminal).
#restarts at 12 so should do 11:57