import requests
from bs4 import BeautifulSoup
import csv
import os

# Define headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Initialize list to hold data
data = []

# Loop through pages
for page_num in range(1, 11):
    url = f'https://www.realtor.com/realestateagents/los-angeles_ca/pg-{page_num}'
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        # Find and extract agent names and companies
        agent_names = soup.find_all('div', class_='agent-name')
        companies = soup.find_all('div', class_='agent-group')

        # Extract experience information
        experience_divs = soup.find_all('div', class_='base__StyledType-rui__sc-108xfm0-0 gwFmbS')
        experience_texts = [div.find('span', class_='jsx-3873707352 bold-text').get_text(strip=True) for div in experience_divs if div.find('span', class_='jsx-3873707352 bold-text')]

        # Extract activity range information
        activity_range_divs = soup.find_all('div', class_='jsx-3873707352 agent-detail-item')
        activity_ranges = [div.find('span', class_='jsx-3873707352 bold-text').get_text(strip=True) for div in activity_range_divs if 'Activity range:' in div.get_text()]

        # Extract listed house information
        listed_house_divs = soup.find_all('div', class_='jsx-3873707352 agent-detail-item')
        listed_houses = [div.find('span', class_='jsx-3873707352 bold-text').get_text(strip=True) for div in listed_house_divs if 'Listed a house:' in div.get_text()]

        # Debug: Print the number of each type of information found
      

        # Pair agent names, companies, experiences, activity ranges, and listed houses
        for agent_name, company in zip(agent_names, companies):
            agent_text = ' '.join(agent_name.stripped_strings)
            company_text = ' '.join(company.stripped_strings)
            # Extract information or default to 'N/A'
            experience_text = experience_texts.pop(0) if experience_texts else 'N/A'
            activity_range_text = activity_ranges.pop(0) if activity_ranges else 'N/A'
            listed_house_text = listed_houses.pop(0) if listed_houses else 'N/A'
            data.append([agent_text, company_text, experience_text, activity_range_text, listed_house_text])
    else:
        print(f"Failed to retrieve the webpage. Status code: {r.status_code}")

# Write data to CSV file
output_file = os.path.expanduser('agents_data.csv')  # Change file path as needed
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Agent Name', 'Company', 'Experience', 'Activity Range', 'Listed House'])  # Write header
        writer.writerows(data)
    print(f"Data written to {output_file} successfully.")
except PermissionError as e:
    print(f"PermissionError: {e}")
