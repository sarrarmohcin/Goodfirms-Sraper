from curl_cffi import requests
"""
This script scrapes company information from the GoodFirms website based on specified categories, services, and industries.
Modules:
    - curl_cffi.requests: For making HTTP requests.
    - bs4.BeautifulSoup: For parsing HTML content.
    - json: For handling JSON data.
    - urllib.parse: For parsing URLs and query parameters.
    - random: For generating random delays between requests.
    - time: For adding delays between requests.
    - pandas: For data manipulation and storage.
    - argparse: For parsing command-line arguments.
Global Variables:
    - categories: A list of dictionaries containing category IDs, names, and URLs.
    - services: A list of dictionaries containing service IDs, names, values, and data names.
    - industries: A list of dictionaries containing industry IDs, names, values, and data names.
    - headers: A dictionary containing HTTP headers for the requests.
Functions:
    - get_companies(session, page, category_id, service_id=None, industry_id=None):
        Fetches a list of companies from GoodFirms based on the specified category, service, and industry.
        Args:
            session: A requests.Session object for making HTTP requests.
            page: The page number to scrape.
            category_id: The ID of the category to scrape.
            service_id: (Optional) The ID of the service to filter by.
            industry_id: (Optional) The ID of the industry to filter by.
        Returns:
            A list of dictionaries containing company names and URLs.
    - get_info(company):
        Fetches detailed information about a specific company.
        Args:
            company: A dictionary containing the company's name and URL.
        Returns:
            A dictionary containing the company's name, URL, description, social profiles, address, and contacts.
Command-Line Arguments:
    - category_id: The ID of the category to scrape. Refer to the 'categories' list for valid IDs.
    - --service_id: (Optional) The ID of the service to filter by. Refer to the 'services' list for valid IDs.
    - --industry_id: (Optional) The ID of the industry to filter by. Refer to the 'industries' list for valid IDs.
Usage:
    Run the script with the required category_id and optional service_id and industry_id to scrape company data.
    Example:
        python scraper.py 1 --service_id 1 --industry_id 1
Notes:
    - The script uses random delays between requests to avoid being flagged as a bot.
    - Ensure that the 'categories', 'services', and 'industries' lists are up-to-date with the GoodFirms website.
"""
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, parse_qs
import random
import time
import pandas as pd
import argparse

categories = [
    {'id': 1, 'name': 'Mobile App Development', 'url': '/directory/platform/app-development'},
    {'id': 2, 'name': 'Web Development', 'url': '/directory/cms/top-website-development-companies'},
    {'id': 3, 'name': 'Software Development', 'url': '/directory/languages/top-software-development-companies'},
    {'id': 4, 'name': 'E-commerce Development', 'url': '/ecommerce-development-companies'},
    {'id': 5, 'name': 'Digital Marketing', 'url': '/directory/marketing-services/top-digital-marketing-companies'},
    {'id': 6, 'name': 'Web Designing (UI/UX)', 'url': '/directory/platforms/top-web-design-companies'},
    {'id': 7, 'name': 'IT Services', 'url': '/it-services'}
]

services = [
    {'id': 1, 'name': 'services[0]', 'value': '1', 'data-name': 'Mobile App Development'},
    {'id': 2, 'name': 'services[1]', 'value': '2', 'data-name': 'Web Development'},
    {'id': 3, 'name': 'services[2]', 'value': '3', 'data-name': 'Software Development'},
    {'id': 4, 'name': 'services[3]', 'value': '5', 'data-name': 'Web Design'},
    {'id': 5, 'name': 'services[4]', 'value': '7', 'data-name': 'Testing Services'},
    {'id': 6, 'name': 'services[5]', 'value': '8', 'data-name': 'Maintenance & Support'},
    {'id': 7, 'name': 'services[6]', 'value': '10', 'data-name': 'IT Services'},
    {'id': 8, 'name': 'services[7]', 'value': '11', 'data-name': 'Big Data & BI'},
    {'id': 9, 'name': 'services[8]', 'value': '12', 'data-name': 'Cloud Computing Services'},
    {'id': 10, 'name': 'services[9]', 'value': '13', 'data-name': 'Digital Marketing'},
    {'id': 11, 'name': 'services[10]', 'value': '14', 'data-name': 'Direct Marketing'},
    {'id': 12, 'name': 'services[11]', 'value': '16', 'data-name': 'Game Development'},
    {'id': 13, 'name': 'services[12]', 'value': '17', 'data-name': 'Bot Development'},
    {'id': 14, 'name': 'services[13]', 'value': '18', 'data-name': 'Blockchain Development'},
    {'id': 15, 'name': 'services[14]', 'value': '19', 'data-name': 'AR & VR Development'},
    {'id': 16, 'name': 'services[15]', 'value': '20', 'data-name': 'IoT Development'},
    {'id': 17, 'name': 'services[16]', 'value': '21', 'data-name': 'Artificial Intelligence'},
    {'id': 18, 'name': 'services[17]', 'value': '22', 'data-name': 'Business Services'},
    {'id': 19, 'name': 'services[18]', 'value': '23', 'data-name': 'BPO Services'},
    {'id': 20, 'name': 'services[19]', 'value': '24', 'data-name': 'Admin Services'},
    {'id': 21, 'name': 'services[20]', 'value': '25', 'data-name': 'Writing Services'},
    {'id': 22, 'name': 'services[21]', 'value': '26', 'data-name': 'Law Firms'},
    {'id': 23, 'name': 'services[22]', 'value': '27', 'data-name': 'Engineering Services'},
    {'id': 24, 'name': 'services[23]', 'value': '28', 'data-name': 'Animation & Multimedia'},
    {'id': 25, 'name': 'services[24]', 'value': '29', 'data-name': 'Translation Services'},
    {'id': 26, 'name': 'services[25]', 'value': '30', 'data-name': 'Implementation Services'},
    {'id': 27, 'name': 'services[26]', 'value': '31', 'data-name': 'DevOps'},
    {'id': 28, 'name': 'services[27]', 'value': '33', 'data-name': 'Robotic Process Automation'},
    {'id': 29, 'name': 'services[28]', 'value': '34', 'data-name': 'Advertising'},
    {'id': 30, 'name': 'services[29]', 'value': '35', 'data-name': 'Web Hosting'},
    {'id': 31, 'name': 'services[30]', 'value': '36', 'data-name': 'Supply Chain & Logistics'},
    {'id': 32, 'name': 'services[31]', 'value': '37', 'data-name': 'Progressive Web App'},
    {'id': 33, 'name': 'services[32]', 'value': '39', 'data-name': 'Real Estate'},
    {'id': 34, 'name': 'services[33]', 'value': '41', 'data-name': 'RPO Services'},
    {'id': 35, 'name': 'services[34]', 'value': '46', 'data-name': 'Metaverse Development'},
    {'id': 36, 'name': 'services[35]', 'value': '47', 'data-name': 'Web3'},
    {'id': 37, 'name': 'services[36]', 'value': '49', 'data-name': 'Low Code/No Code'}
]

industries = [
    {'id': 1, 'name': 'industry[0]', 'value': '1', 'data-name': 'Advertising & Marketing'},
    {'id': 2, 'name': 'industry[1]', 'value': '2', 'data-name': 'Automotive'},
    {'id': 3, 'name': 'industry[2]', 'value': '3', 'data-name': 'Art, Entertainment & Music'},
    {'id': 4, 'name': 'industry[3]', 'value': '4', 'data-name': 'Business Services'},
    {'id': 5, 'name': 'industry[4]', 'value': '5', 'data-name': 'Consumer Products'},
    {'id': 6, 'name': 'industry[5]', 'value': '6', 'data-name': 'Education'},
    {'id': 7, 'name': 'industry[6]', 'value': '7', 'data-name': 'Financial & Payments'},
    {'id': 8, 'name': 'industry[7]', 'value': '8', 'data-name': 'Gaming'},
    {'id': 9, 'name': 'industry[8]', 'value': '9', 'data-name': 'Gambling'},
    {'id': 10, 'name': 'industry[9]', 'value': '10', 'data-name': 'Government'},
    {'id': 11, 'name': 'industry[10]', 'value': '11', 'data-name': 'Healthcare & Medical'},
    {'id': 12, 'name': 'industry[11]', 'value': '12', 'data-name': 'Hospitality'},
    {'id': 13, 'name': 'industry[12]', 'value': '13', 'data-name': 'Information Technology'},
    {'id': 14, 'name': 'industry[13]', 'value': '14', 'data-name': 'Telecommunication'},
    {'id': 15, 'name': 'industry[14]', 'value': '15', 'data-name': 'Designing'},
    {'id': 16, 'name': 'industry[15]', 'value': '16', 'data-name': 'Legal & Compliance'},
    {'id': 17, 'name': 'industry[16]', 'value': '17', 'data-name': 'Manufacturing'},
    {'id': 18, 'name': 'industry[17]', 'value': '18', 'data-name': 'Media'},
    {'id': 19, 'name': 'industry[18]', 'value': '19', 'data-name': 'Real Estate'},
    {'id': 20, 'name': 'industry[19]', 'value': '20', 'data-name': 'NGOs'},
    {'id': 21, 'name': 'industry[20]', 'value': '21', 'data-name': 'Transportation & Logistics'},
    {'id': 22, 'name': 'industry[21]', 'value': '22', 'data-name': 'Utilities'},
    {'id': 23, 'name': 'industry[22]', 'value': '23', 'data-name': 'Retail'},
    {'id': 24, 'name': 'industry[23]', 'value': '24', 'data-name': 'Other Industries'},
    {'id': 25, 'name': 'industry[24]', 'value': '25', 'data-name': 'E-commerce'},
    {'id': 26, 'name': 'industry[25]', 'value': '26', 'data-name': 'Travel & Lifestyle'},
    {'id': 27, 'name': 'industry[26]', 'value': '27', 'data-name': 'Social'},
    {'id': 28, 'name': 'industry[27]', 'value': '28', 'data-name': 'Startups'},
    {'id': 29, 'name': 'industry[28]', 'value': '29', 'data-name': 'Enterprise'},
    {'id': 30, 'name': 'industry[29]', 'value': '30', 'data-name': 'Productivity'},
    {'id': 31, 'name': 'industry[30]', 'value': '31', 'data-name': 'Banking'},
    {'id': 32, 'name': 'industry[31]', 'value': '32', 'data-name': 'Insurance'},
    {'id': 33, 'name': 'industry[32]', 'value': '33', 'data-name': 'Public Sector'},
    {'id': 34, 'name': 'industry[33]', 'value': '34', 'data-name': 'Industrial'},
    {'id': 35, 'name': 'industry[34]', 'value': '35', 'data-name': 'Food & Beverages'},
    {'id': 36, 'name': 'industry[35]', 'value': '36', 'data-name': 'Agriculture'},
    {'id': 37, 'name': 'industry[36]', 'value': '39', 'data-name': 'Oil & Energy'},
    {'id': 38, 'name': 'industry[37]', 'value': '40', 'data-name': 'Defense & Aerospace'},
    {'id': 39, 'name': 'industry[38]', 'value': '41', 'data-name': 'Neo-banks'},
    {'id': 40, 'name': 'industry[39]', 'value': '42', 'data-name': 'Cryptocurrency'}
]


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.goodfirms.co/ecommerce-development-companies',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}


def get_companies(session, page, category_id, service_id = None, industry_id = None):
    
    params = {'page': str(page)}
    
    if service_id:
        params[services[service_id - 1]['name']] = services[service_id - 1]['value']
    
    if industry_id:
        params[industries[industry_id - 1]['name']] = industries[industry_id - 1]['value']


    try:
        

        response = session.get(
            f'https://www.goodfirms.co{categories[category_id - 1]["url"]}',
            params=params,
        )
        response.raise_for_status()
        
        # check the end

        parsed_url = urlparse(response.url)
        response_params = parse_qs(parsed_url.query)
        response_page = response_params.get('page', ['1'])[0]
  
        if int(response_page) != page:
            print(f"Expected page {page} but got {response_page}. No more results.")
            return []

        # get items
        soup = BeautifulSoup(response.content, 'html.parser')
        script = soup.select_one('script[type="application/ld+json"]')

        data = json.loads(script.string)

        graph_data = data['@graph']
        items = graph_data[1]['itemListElement']

        results = []
        for item in items:

            results.append({
                'name': item['item']['name'],
                'url': item['item']['url']
            })
            
        return results
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
def get_info(company):
    try:
        
        response = session.get(
            company["url"]
        )
        response.raise_for_status()
        
        # get items
        soup = BeautifulSoup(response.content, 'html.parser')
        script = soup.select_one('script[type="application/ld+json"]')
        
        data = json.loads(script.string)
        
        graph_data = data['@graph'][0]
        
        name = graph_data.get('name', '')
        url = graph_data.get('url', '')
        description = graph_data.get('description', '')
        social_profiles = graph_data.get('sameAs', [])
        address = graph_data.get('address', {})
        contacts = graph_data.get('contactPoint', [])
        
        return {
            'name': name,
            'url': url,
            'description': description,
            'social_profiles': social_profiles,
            'address': address,
            'contacts': contacts
        }
        
    except Exception as e:
        print(f"An error occurred while getting info for {company['name']}: {e}")
        return None
    
    
if __name__ == "__main__":
    # Define arguments
    
    parser = argparse.ArgumentParser(description="Scrape companies from GoodFirms based on category, service, and industry.")
    parser.add_argument("--category_id", type=int, help="The ID of the category to scrape. Refer to the 'categories' list for valid IDs.")
    parser.add_argument("--limit", type=int, help="The limit of companies extracted", default=None)
    parser.add_argument("--service_id", type=int, help="The ID of the service to filter by. Refer to the 'services' list for valid IDs.", default=None)
    parser.add_argument("--industry_id", type=int, help="The ID of the industry to filter by. Refer to the 'industries' list for valid IDs.", default=None)

    args = parser.parse_args()

    # create session
    session = requests.Session()
    session.impersonate = "chrome120"
    session.headers.update(headers)
    data = []
    for page in range(1):
        results = get_companies(session=session, page=page, category_id=args.category_id, service_id=args.service_id, industry_id=args.industry_id)
        if not results:
            print("No more results, stopping.")
            break
        data.extend(results)
        print(f"Page {page} scraped, total companies: {len(data)}")
        
        # check limit
        if args.limit and len(data) >= args.limit:
            data = data[:args.limit]
            print(f"Limit of {args.limit} reached, stopping.")
            break
        
        time.sleep(random.uniform(2, 5))
    
    # get info for each company
    infos = []
    for company in data[:4]:
        info = get_info(company)
        if info:
            infos.append(info)
            print(f"Info for {company['name']} retrieved successfully.")
            
        time.sleep(random.uniform(2, 5))
        
    # store data in a dataframe
    df = pd.DataFrame(infos)
    df.to_csv('goodfirms_companies.csv', index=False)