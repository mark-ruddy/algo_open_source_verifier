import os
from dotenv import load_dotenv, find_dotenv
from .algo_api_client import AlgoApiClient
from .open_source_parser import OpenSourceParser

def teal_urls_match_app_id(approval_url: str, clear_state_url: str, app_id: str) -> bool:
    """
    The most straightforward case - 2 TEAL source code URLs are provided with an application ID to compare against.
    Uses the Purestake API on the Algorand mainnet, ensure the PURESTAKE_API_KEY environment variable is set
    """
    parser = OpenSourceParser()
    approval_source = parser.source_from_any(approval_url)
    clear_state_source = parser.source_from_any(clear_state_url)

    load_dotenv()
    client = AlgoApiClient("https://mainnet-algorand.api.purestake.io/ps2", os.getenv("PURESTAKE_API_KEY"))
    matches = client.compare_teal_to_app(approval_source, clear_state_source, app_id)
    return matches
