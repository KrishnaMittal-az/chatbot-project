import requests
from bs4 import BeautifulSoup
import re

# Function to fetch and parse website content, then search for patterns
def scrape_website_for_pattern(url, pattern):
    try:
        # Fetch the web page content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the visible text from the page
        page_text = soup.get_text()

        # Compile the regular expression pattern
        regex = re.compile(pattern, re.IGNORECASE)

        # Search for the pattern in the text
        matches = regex.findall(page_text)

        # Return the result
        if matches:
            return f"Found {len(matches)} occurrences of the pattern on the website: {matches}"
        else:
            return f"No matches for the pattern found on the website."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the website: {e}"

# Example usage
url = "https://www.example.com"
pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"  # Pattern to match email addresses
result = scrape_website_for_pattern(url, pattern)
print(result)