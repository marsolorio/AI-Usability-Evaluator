import requests
from bs4 import BeautifulSoup

def evaluate_website(url):
    try:
        # Fetch the website content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Evaluate headers
        h1_tags = len(soup.find_all('h1'))
        h2_tags = len(soup.find_all('h2'))

        # Find images missing alt text
        images = soup.find_all('img')
        missing_alt = [img['src'] for img in images if not img.get('alt')]

        # Return evaluation results
        return {
            "url": url,
            "h1_tags": h1_tags,
            "h2_tags": h2_tags,
            "missing_alt": missing_alt
        }
    except Exception as e:
        return {
            "url": url,
            "h1_tags": 0,
            "h2_tags": 0,
            "missing_alt": [],
            "error": str(e)
        }
