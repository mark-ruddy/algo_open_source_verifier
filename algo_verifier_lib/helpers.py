from dotenv import dotenv_values
from .algo_api_client import AlgoApiClient, AlgoAppBytecode
from .open_source_parser import OpenSourceParser

def teal_and_app_id_matches(approval_url: str, clear_state_url: str, app_id: str) -> bool:
    """The most straightforward case - 2 TEAL source code URLs are provided with an application ID to compare against"""

    parser = OpenSourceParser()
    approval_source = parser.source_from_any(approval_url)
    clear_state_source = parser.source_from_any(clear_state_url)

    # TODO: For now pulling purestake link and all from local env
    # Need to find strategy for how a user would provide this
    # Should be as simple as just having this function ask for an api_key and the link right? Since this is the main current endpoint and I can create other library endpoints for pyteal etc.
    # Maybe for now this app could just rely on my key since its not gonna have a lot of traffic, and in future an api key solution could be discovered - forcing users to provide an API key and link would put many off using the app
    envvars = dotenv_values(".env")
    client = AlgoApiClient("https://mainnet-algorand.api.purestake.io/ps2", envvars["PURESTAKE_API_KEY"])
    matches = client.compare_teal_to_app(approval_source, clear_state_source, app_id)
    return matches
