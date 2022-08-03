from .algo_api_client import AlgoApiClient, AlgoAppBytecode
from .open_source_parser import OpenSourceParser

def teal_and_app_id_matches(approval_url: str, clear_state_url: str, app_id: str) -> bool:
    """
    The most straightforward case - 2 TEAL file URLs are provided with an application ID to compare against
    Use the parser to get the source code
    """

    # TODO: for now only github is supported
    if not approval_url.contains("github.com") or not clear_state_url.contains("github.com"):
        return False
    parser = OpenSourceParser("https://github.com")
    approval_source = parser.source_from_github_file_url(approval_url)
    clear_state_source = parser.source_from_github_file_url(clear_state_url)

    # TODO: should be valid purestake client, maybe caller should be able to choose the client?
    # Probably need to get API key from envvars
    client = AlgoApiClient("https://purestake.io", "TODO")
    matches = client.compare_teal_to_app(approval_source, clear_state_source, app_id)
    return matches
