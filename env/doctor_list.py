import requests
from bs4 import BeautifulSoup
import re

# Define a dictionary of cookies to be sent with the request
cookies = {
    'infosoins': '1h96vv0spnngombasto3ge1bt3',
    'AmeliDirectPersist': '1701896503.42527.0000',
    'TS01b76c1f': '0139dce0d27d3d6b5f518eafb41db95e7b1af6a88d3492ac882b5fc95de0b80c4870825ce36cdc5756cb350f46d9da691e1dbcf188',
    'xtvrn': '$475098$',
    'arp_scroll_position': '100',
}

# Define a dictionary of headers to be sent with the request
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'infosoins=1h96vv0spnngombasto3ge1bt3; AmeliDirectPersist=1701896503.42527.0000; TS01b76c1f=0139dce0d27d3d6b5f518eafb41db95e7b1af6a88d3492ac882b5fc95de0b80c4870825ce36cdc5756cb350f46d9da691e1dbcf188; xtvrn=$475098$; arp_scroll_position=100',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'cp-extension-installed': 'Yes',
}

# Define the file path to save the scraped data
path = r"C:\Users\Baptiste\Documents\scrap_ameli_learning\doctor.csv"

# Define the starting page number for the URL
pageNumber = 1

# Loop 20 times to scrape information from different pages of the website
for url in range(20):
    # Generate the URL with the current page number
    url = f'http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-{pageNumber}-par_page-20-tri-aleatoire.html'

    # Make a GET request to the URL with the specified cookies and headers
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    # Increase the page number for the next iteration of the loop
    pageNumber + 1

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the elements with class 'item-professionnel-inner'
    doctors = soup.findAll('div', class_='item-professionnel-inner')

    # Loop through each element
    for doctor in doctors:
        # Extract the doctor's name
        name = doctor.find('h2').text.strip()

        # Check if there is a phone number available
        div = doctor.find('div', class_='item left tel')
        if div:
            number = div.text.strip()

        # Extract the doctor's address
        address_split = doctor.find('div', class_='item left adresse').text.strip()
        address = ', '.join(re.split(r'(\d+)', address_split))

        # Write the extracted information to a file
        with open(path, "a", encoding='utf-16-le') as writer:
            writer.write(f"{name}")
            writer.write(f";")
            writer.write(f"{number}")
            writer.write(f";")
            writer.write(f"{address}\n")