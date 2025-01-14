from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

def process_search_results(driver, group_name, state,company_code):
    try:
        #Kiểm tra xem có hàng nào trong bảng không
        rows = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[2]/div[2]/table/tbody/tr')
        if not rows:
            print("No rows found in the table.")
            return

        # Chọn "Show: 100" từ dropdown
        show_100_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt25:filingTable:j_id2"]'))
        )
        show_100_dropdown.click()
        show_100_dropdown_opt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt25:filingTable:j_id2"]/option[@value="100"]'))
        )
        show_100_dropdown_opt.click()
        time.sleep(2)  # Đợi trang tải lại

        # Nhấp vào "Filing Type" để sắp xếp theo loại
        filing_type_header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[2]/div[2]/table/thead/tr/th[5]/span[1]'))
        )
        filing_type_header.click()
        time.sleep(2)  # Đợi trang tải lại

        # Lặp qua các hàng trong bảng
        current_row = 1
        while True:
            try:
                # Xác định XPath của hàng hiện tại
                row_xpath = f'/html/body/div[2]/div/div/div[2]/form/div[2]/div[2]/table/tbody/tr[{current_row}]'
                row = driver.find_element(By.XPATH, row_xpath)
                filing_type = row.find_element(By.XPATH, './td[5]').text  # Giả định cột thứ 5 là Filing Type

                if "rate" in filing_type.lower():
                    row.click()
                    time.sleep(2)  # Đợi trang tải lại

                    # Nhấn nút "Download ZIP"
                    download_zip_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/form/div[2]/div/button/span'))
                    )
                    download_zip_button.click()
                    time.sleep(2)  # Đợi tải xuống hoàn tất
                    
                    # Tạo cấu trúc thư mục
                    group_folder = os.path.join("Auto", group_name)
                    state_folder = os.path.join(group_folder, state)
                    company_folder = os.path.join(state_folder, str(company_code))
                    os.makedirs(company_folder, exist_ok=True)
                    
                    # Di chuyển tệp đã tải xuống vào thư mục tương ứng
                    download_dir = r"C:\Users\Ha My\Downloads"
                    #output_dir = r"C:\Users\Ha My\.vscode\scraping\insurance_scraper\data\output"
                    for file_name in os.listdir(download_dir):
                        if file_name.endswith(".zip"):
                            #print(f"Moving file {file_name} to {output_dir}")
                            #shutil.move(os.path.join(download_dir, file_name), os.path.join(output_dir, file_name))
                            print(f"Moving file {file_name} to {company_folder}")
                            shutil.move(os.path.join(download_dir, file_name), os.path.join(company_folder, file_name))
                    # Quay lại trang kết quả tìm kiếm
                    driver.back()
                    time.sleep(3)  # Đợi trang tải lại

                # Chuyển sang dòng kế tiếp
                current_row += 1

            except Exception as e:
                print(f"Error processing row {current_row}: {e}")
                break  # Thoát khỏi vòng lặp nếu không còn hàng nào để xử lý

    except Exception as e:
        print(f"An error occurred: {e}")