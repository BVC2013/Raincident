from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the page containing the table
url = 'https://www.nj.gov/njsp/info/fatalacc/index.shtml'
driver.get(url)

# Wait for the table to load
time.sleep(5)  # Adjust this if necessary

# Locate the table and extract data
table = driver.find_element("css selector", "table")  # Adjust the selector if needed
rows = table.find_elements("tag name", "tr")

# Extract headers
headers = [header.text for header in rows[0].find_elements("tag name", "th")]

# Extract rows
data = []
for row in rows[1:]:
    cols = row.find_elements("tag name", "td")
    data.append([col.text for col in cols])

# Create DataFrame
df = pd.DataFrame(data, columns=headers)

# Save to CSV
df.to_csv('fatal_crash_statistics_2024.csv', index=False)

# Clean up
driver.quit()

print("CSV file has been created successfully.")