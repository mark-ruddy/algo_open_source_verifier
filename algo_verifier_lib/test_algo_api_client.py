from .algo_api_client import *

def setup_algo_client_purestake() -> AlgoApiClient:
    # TODO: this should take envvars for real api key, and real purestake API https location
    return AlgoApiClient("https://purestake.com", "real_key")

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

def test_get_algo_app_bytecode():
    client = setup_algo_client_purestake()
    # TODO: use a real app ID to compare against, tinyman etc.
    app_bytecode = client.get_algo_app_bytecode("real_app_id")
    assert app_bytecode.approval == "TODO"
    assert app_bytecode.clear_state == "TODO"

def test_compile_teal():
    client = setup_algo_client_purestake()
    sample_teal = """
    #pragma version 5
    int 1
    return
    """
    compiled_bytecode = client.compile_teal(sample_teal)
    # TODO: what bytecode should be returned
    assert len(compiled_bytecode) > 1

def test_compile_teal_invalid():
    client = setup_algo_client_purestake()
    sample_teal = """
    #pragma version 5
    int 1
    INVALID
    return
    """
    compiled_bytecode = client.compile_teal(sample_teal)
    # TODO: assert on the error

def test_compare_teal_to_app():
    client = setup_algo_client_purestake()
    # TODO: should be successful match
    teal_matches = client.compare_teal_to_app("TODO", "TODO", "TODO")
    assert teal_matches == True

def test_compare_teal_to_app_not_match():
    client = setup_algo_client_purestake()
    # TODO: should be valid teal etc, but should not match
    teal_not_match = client.compare_teal_to_app("TODO", "TODO", "TODO")
    assert teal_not_match == False
