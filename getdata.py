import requests
import pandas as pd

# URL of the page containing the table
url = 'https://www.nj.gov/njsp/info/fatalacc/index.shtml'

# Fetch the webpage
response = requests.get(url)

# Use pandas to read the table
tables = pd.read_html(response.text)

# Assuming the first table on the page is the one you want
df = tables[0]

# Save the DataFrame to a CSV file
df.to_csv('fatal_crash_statistics_2024.csv', index=False)

print("CSV file has been created successfully.")