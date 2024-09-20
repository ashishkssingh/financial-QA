import json
import logging
import os
from typing import Any
from urllib.parse import urlencode, urljoin
import requests

logger = logging.getLogger("src.api_call")

FMP_API_KEY = os.environ.get("FMP_API_KEY")


def convert_json_output_to_dict(json_output):
    # Step 1: Remove the Markdown formatting
    json_str = json_output.strip("```json\n").strip("```")

    # Step 2: Load the string into a Python dictionary
    return json.loads(json_str)


def add_ticker_to_url(url: str, ticker: str, ticker_flag: bool) -> str:
    """Adds a ticker to the URL if it's not already present and the `ticker_flag` is True.

    Args:
        url: The base URL.
        ticker: The ticker symbol to add.
        ticker_flag: A boolean indicating whether to add the ticker.

    Returns:
        The updated URL with the ticker added if necessary.
    """
    return_url = ""
    if ticker_flag and ticker not in url:
        return_url = urljoin(url, ticker)
    return_url = url
    logger.info("Request URL: %s", return_url)
    return return_url


def get_financial_data(response_data) -> dict[str, Any]:

    response_data["path_parameters"]["apikey"] = FMP_API_KEY

    # Extract URL, path parameters, and query parameters
    base_url = response_data["url_without_ticker_symbol_or_query_params"]
    path_params = response_data["path_parameters"]
    query_params = response_data["query_params"]

    # Combine URL with path parameters (if any)
    # Here, you can modify the base URL with path parameters if needed
    # In this example, there are no path parameters to add.

    url = add_ticker_to_url(
        url=base_url,
        ticker=response_data["ticker_symbol"],
        ticker_flag=response_data["use_ticker_or_not"],
    )

    # Construct the final URL with query parameters
    final_url = f"{url}?{urlencode(path_params)}"

    logger.info("Request URL :%s", final_url)

    # Make the API call
    response = requests.get(final_url, params=query_params)

    # Return the response (you can also return response.json() if you want the JSON data)
    return json.loads(response.text)
