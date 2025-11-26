# extract/utils/fetch.py
import requests
from time import sleep
from typing import Optional

DEFAULT_HEADERS = {
    "User-Agent": "job-scraper-bot/0.1 (+https://github.com/husseini2000/job-scraper)"
}

def fetch(url: str, headers: Optional[dict] = None, retries: int = 3, delay: int = 2) -> Optional[str]:
    """Fetch the content of a URL with optional retries.

    Args:
        url (str): The URL to fetch.
        headers (Optional[dict]): Optional HTTP headers to include in the request.
        retries (int): Number of retries in case of failure.
        delay (int): Delay in seconds between retries.

    Returns:
        Optional[str]: The content of the response if successful, None otherwise.
    """
    if headers is None:
        headers = DEFAULT_HEADERS

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            sleep(delay)

    print("All attempts to fetch the URL have failed.")
    return None
