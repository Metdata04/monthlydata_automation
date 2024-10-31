import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

webpage_url = 'https://meteo.gov.lk/index.php?lang=en'

def get_monthly_pdf_link(webpage_url):
    try:
        # Get the current year
        current_year = str(datetime.now().year)  # Convert the year to string for use as an ID

        response = requests.get(webpage_url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <div> with id equal to the current year
        year_div = soup.find('div', {'id': current_year})
        if year_div:
            # Look for <a> tags within this <div>, possibly nested within <p>, <span>, etc.
            monthly_link = year_div.find('a', href=True)
            if monthly_link:
                pdf_url = monthly_link['href']
                if not pdf_url.startswith('http'):
                    pdf_url = requests.compat.urljoin(webpage_url, pdf_url)
                return pdf_url

        print(f"PDF link for the year {current_year} not found.")
        return None

    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return None

def download_pdf(pdf_url, local_filename):
    try:
        response = requests.get(pdf_url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)

        with open(local_filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded PDF: {local_filename}")

    except requests.RequestException as e:
        print(f"An error occurred while downloading the PDF: {e}")

def main():
    pdf_url = get_monthly_pdf_link(webpage_url)
    
    if pdf_url:
        # Get the current year and month in YYYY-MM format
        date_string = datetime.now().strftime('%Y-%m')
        # Use the date in the filename for the monthly report
        pdf_filename = f'monthlydata/monthly_climate_update_{date_string}.pdf'
        download_pdf(pdf_url, pdf_filename)
    else:
        print("Monthly PDF link not found on the page.")

if __name__ == "__main__":
    main()
