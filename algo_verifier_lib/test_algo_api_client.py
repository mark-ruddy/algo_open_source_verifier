from .algo_api_client import *

def setup_algo_client_with_key() -> AlgoApiClient:
    return AlgoApiClient("https://test.api", "myKey123")

def setup_algo_client_no_key() -> AlgoApiClient:
    return AlgoApiClient("https://test.api", None)

def test_format_api_call_with_key():
    client = setup_algo_client_with_key()
    url = client.format_api_call("v2/teal/compile", "date=2022-06-07")
    assert url == "https://test.api/v2/teal/compile?api-key=myKey123&date=2022-06-07"

def test_format_api_call_no_key():
    client = setup_algo_client_no_key()
    url = client.format_api_call("v2/teal/compile", "date=2022-06-07")
    assert url == "https://test.api/v2/teal/compile?date=2022-06-07"

def test_format_api_call_with_key_no_args():
    client = setup_algo_client_with_key()
    url = client.format_api_call("v2/teal/compile", None)
    assert url == "https://test.api/v2/teal/compile?api-key=myKey123"
