import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.ajax.ca/en/black-owned-business-ajax-directory.aspx#{}'
site = url.format('Education')
response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_='datatable')

# Define the header names for the output dataframe
headers = ['Business Name', 'Address', 'Phone', 'Email', 'Website']

# Initialize a dictionary to store the data for each header
data_dict = {header: [] for header in headers}

# Loop over each table and extract data
for table in tables:
    rows = []
    for tr in table.find_all('tr')[1:]:
        cells = []
        for td in tr.find_all('td'):
            text = td.text.strip()
            cells.append(text)
        rows.append(cells)
    table_df = pd.DataFrame(rows, columns=headers)
    for header in headers:
        data_dict[header].extend(table_df[header].tolist())

# Create the final dataframe from the dictionary
df = pd.DataFrame(data_dict)

# Save the dataframe to an Excel file
df.to_excel('output.xlsx', index=False)
