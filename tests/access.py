import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl import process_search_results
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time

# Đường dẫn đến file states.csv và input.csv
states_csv_path = "C:/Users/Ha My/.vscode/scraping/insurance_scraper/data/input/states.csv"
input_csv_path = "C:/Users/Ha My/.vscode/scraping/insurance_scraper/data/input/input.csv"

# Thiết lập trình duyệt Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Khởi tạo WebDriver mà không cần chỉ định đường dẫn ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Đọc file input.csv
company_data = pd.read_csv(input_csv_path, encoding="latin1")
# Đọc file serff-states.csv
state_urls = pd.read_csv(states_csv_path, names=["URL"], encoding="latin1")
state_urls["state"] = state_urls["URL"].apply(lambda x: x.split("/")[-1])  # Tách mã bang từ URL

def access_url(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/a'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div/div/div/button[1]/span'))).click()

def fill_search_form(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="simpleSearch:businessType_label"]'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="simpleSearch:businessType_1"]'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/form/div[2]/span/div[4]/div/div/span/label'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/ul/li[6]/label'))).click()
    driver.find_element(By.XPATH, '//*[@id="simpleSearch:dispositionStartDate_input"]').send_keys("1/1/2019")

def search_company(driver, company_code):
    naic_company_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="simpleSearch:companyCode"]')))
    naic_company_code.clear()
    naic_company_code.send_keys(company_code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/form/div[2]/span/div[11]/div/div/button/span'))).click()

    
# Đọc file CSV và lặp qua từng đường dẫn
with open(states_csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Bỏ qua dòng tiêu đề nếu có

    for row in reader:
        if len(row) == 0:
            continue

        url = row[1]  # Giả định cột đầu tiên là URL
        state = row[0]  # Giả định cột đầu tiên là mã bang

        try:
            print(f"Accessing URL: {url}")
            access_url(driver, url)
            fill_search_form(driver)

            for index, company_row in company_data.iterrows():
                company_code = company_row[1]  # Giả định cột thứ 2 là company code
                group_name = company_row[0]  # Giả định cột thứ 1 là group name

                # Tạo cấu trúc thư mục
                group_folder = os.path.join("Auto", group_name)
                state_folder = os.path.join(group_folder, state)
                company_folder = os.path.join(state_folder, str(company_code))
                os.makedirs(company_folder, exist_ok=True)

                search_company(driver, company_code)
                time.sleep(3)
                process_search_results(driver, group_name, state, company_code)
                time.sleep(3)

                # Quay lại trang kết quả tìm kiếm
                driver.back()
                time.sleep(3)   

        except Exception as e:
            print(f"Error processing {url}: {e}")

driver.quit()