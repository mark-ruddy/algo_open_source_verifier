from dotenv import dotenv_values
from .algo_api_client import *

def setup_purestake_algo_client() -> AlgoApiClient:
    envvars = dotenv_values(".env")
    return AlgoApiClient("https://mainnet-algorand.api.purestake.io/ps2", envvars["PURESTAKE_API_KEY"])

def setup_sample_algo_client() -> AlgoApiClient:
    return AlgoApiClient("https://test.api", None)

def test_format_api_call_no_args():
    client = setup_sample_algo_client()
    url = client.format_api_call("v2/teal/compile", None)
    assert url == "https://test.api/v2/teal/compile"

def test_format_api_call_with_args():
    client = setup_sample_algo_client()
    url = client.format_api_call("v2/teal/compile", "date=2022-06-07&page=10")
    assert url == "https://test.api/v2/teal/compile?date=2022-06-07&page=10"

def test_get_algo_app_bytecode():
    client = setup_purestake_algo_client()
    # Test against the tinyman staking application: https://algoexplorer.io/application/649588853
    # Expected bytecode here will need to be updated on any changes to this application
    app_bytecode = client.get_algo_app_bytecode("649588853")
    assert app_bytecode.approval == "BSADAAEIJgcIZW5kX3RpbWUGYXNzZXRzBG1pbnMMdmVyaWZpY2F0aW9uCGJhbGFuY2UgAmlkD3Byb2dyYW1fY291bnRlcjEZIhJAAC8xGSMSQAAZMRmBAhJAAicxGYEEEkACITEZgQUSQAIfADYaAIAFc2V0dXASQAGZADYaAIAGY3JlYXRlEkAAijYaAIAGY29tbWl0EkAAfTYaAIAFY2xhaW0SQAEDNhoAgAZ1cGRhdGUSQAE8NhoAgA51cGRhdGVfcmV3YXJkcxJAAN82GgCADXVwZGF0ZV9hc3NldHMSQAD4NhoAgAtlbmRfcHJvZ3JhbRJAAPI2GgArEkAA9TYaAIALbG9nX2JhbGFuY2USQADvACNDIyhiMgcNRCMpYiJKJAtbNjAAEkAACiMISYEODERC/+tMSDUBIypiNAEkC1s1AjYaARdBAAg2GgEXNAIPRCI2MABwAERJFicETFCwNhoBFw9EgBN0aW55bWFuU3Rha2luZy92MTpiMQVRABMSRDEFVxMANQE0ASJbIycFYhJENAEkWzYwABJENAGBEFs2GgEXEkQjQyNDIoACcjE2GgFmIoACcjI2GgJmIoACcjM2GgNmIoACcjQ2GgRmIoACcjU2GgVmI0MiKTYaAWYiKjYaAmYjQyIoNhoBF2YjQyNDMgkxABJEIis2GgFmI0MiNjAAcABESUQWJwRMULAjQycGZCMINQEnBjQBZyInBTQBZiKAA3VybDYaAWYigA9yZXdhcmRfYXNzZXRfaWQ2GgIXZiKADXJld2FyZF9wZXJpb2Q2GgMXZiKACnN0YXJ0X3RpbWU2GgQXZiIoNhoFF2YiKTYaBmYiKjYaB2YjQyNDMgkxABJDMgkxABJDAA=="
    assert app_bytecode.clear_state == "BIEB"

def test_compile_teal():
    client = setup_purestake_algo_client()
    sample_teal = """
    #pragma version 5
    int 1
    return
    """
    compiled_bytecode = client.compile_teal(sample_teal.strip())
    assert compiled_bytecode == "BYEBQw=="

def test_compile_teal_invalid():
    client = setup_purestake_algo_client()
    sample_teal = """
    #pragma version 5
    int 1
    INVALID
    return
    """
    try:
        client.compile_teal(sample_teal.strip())
    except HTTPError:
        # Expected to hit HTTPError when making a call with invalid TEAL
        assert True
    assert False

def test_compare_teal_to_app():
    client = setup_purestake_algo_client()
    # TODO: should be successful match
    teal_matches = client.compare_teal_to_app("TODO", "TODO", "TODO")
    assert teal_matches == True

def test_compare_teal_to_app_not_match():
    client = setup_purestake_algo_client()
    # TODO: should be valid teal etc, but should not match
    teal_not_match = client.compare_teal_to_app("TODO", "TODO", "TODO")
    assert teal_not_match == False
