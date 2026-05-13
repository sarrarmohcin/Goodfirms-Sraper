# GoodFirms Scraper

## About the Project

This project is a web scraper designed to extract company information from the GoodFirms website based on specified categories, services, and industries. It leverages Python and various libraries to fetch and process data efficiently.

### Key Features

- Extracts company data based on categories, services, and industries.
- Supports filtering by category, service, and industry IDs.
- Handles pagination and ensures data accuracy.
- Retrieves detailed company information, including name, URL, description, social profiles, address, and contacts.
- Outputs the scraped data into a CSV file for easy analysis.

### Prerequisites

- Python 3.7 or higher
- Required libraries:
    - `curl_cffi`
    - `bs4`
    - `pandas`

Install the dependencies using pip:

```bash
pip install curl_cffi beautifulsoup4 pandas
```

### How to Use

Run the script with the necessary arguments to scrape data:

```bash
python scraper.py --category_id <CATEGORY_ID> [--service_id <SERVICE_ID>] [--industry_id <INDUSTRY_ID>] [--limit <LIMIT>]
```

#### Arguments
- `--category_id`: (Required) The ID of the category to scrape. Refer to `categories.json` for valid IDs.
- `--service_id`: (Optional) The ID of the service to filter by. Refer to `services.json` for valid IDs.
- `--industry_id`: (Optional) The ID of the industry to filter by. Refer to `industries.json` for valid IDs.
- `--limit`: (Optional) The maximum number of companies to scrape.

#### Example
```bash
python scraper.py --category_id 1 --service_id 2 --industry_id 3 --limit 50
```

### Output

The scraped data is saved into a CSV file named `goodfirms_companies.csv` in the current directory.

### Additional Notes
- The script introduces random delays between requests to avoid detection as a bot.
- Ensure that the `categories.json`, `services.json`, and `industries.json` files are updated to reflect the latest data from the GoodFirms website.