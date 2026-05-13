# GoodFirms Scraper

This project is a web scraper designed to extract company information from the GoodFirms website based on specified categories, services, and industries. The scraper uses Python and various libraries to fetch and process data efficiently.

## Features

- Scrapes company data from GoodFirms based on categories, services, and industries.
- Supports filtering by category, service, and industry IDs.
- Handles pagination and ensures data integrity.
- Extracts detailed company information, including name, URL, description, social profiles, address, and contacts.
- Saves the scraped data into a CSV file for further analysis.

## Prerequisites

- Python 3.7 or higher
- Libraries:
  - `curl_cffi`
  - `bs4`
  - `pandas`
  - `argparse`

Install the required libraries using pip:

```bash
pip install curl_cffi beautifulsoup4 pandas
```
## Usage

Run the script with the required arguments to scrape data:

python [scraper.py](http://_vscodecontentref_/1) --category_id <CATEGORY_ID> [--service_id <SERVICE_ID>] [--industry_id <INDUSTRY_ID>] [--limit <LIMIT>]*

Arguments
- --category_id: (Required) The ID of the category to scrape. Refer to categories.json for valid IDs.
- --service_id: (Optional) The ID of the service to filter by. Refer to services.json for valid IDs.
- --industry_id: (Optional) The ID of the industry to filter by. Refer to industries.json for valid IDs.
- --limit: (Optional) The maximum number of companies to scrape.

Example
python [scraper.py](http://_vscodecontentref_/2) --category_id 1 --service_id 2 --industry_id 3 --limit 50

## Output

The script saves the scraped data into a CSV file named goodfirms_companies.csv in the current directory.
