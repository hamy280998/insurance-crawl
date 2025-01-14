import pandas as pd

# Đọc file input.csv
company_data = pd.read_csv("C:/Users/Ha My/.vscode/scraping/insurance_scraper/data/input/input.csv", encoding="latin1")
print("Company Data:")
print(company_data.head())  # Kiểm tra dữ liệu

# Đọc file serff-states.csv
state_urls = pd.read_csv("C:/Users/Ha My/.vscode/scraping/insurance_scraper/data/input/states.csv", names=["URL"], encoding="latin1")
state_urls["state"] = state_urls["URL"].apply(lambda x: x.split("/")[-1])  # Tách mã bang từ URL
print("State URLs:")
print(state_urls.head())  # Kiểm tra dữ liệu

