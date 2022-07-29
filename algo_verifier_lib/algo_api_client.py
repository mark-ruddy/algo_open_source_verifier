import requests
from requests.models import HTTPError

class AlgoAppBytecode:
    """
    Represents an Algorand Applications on-chain bytecode for an approval and clear_state program
    """
    def __init__(self, approval: str, clear_state: str) -> None:
        self.approval = approval
        self.clear_state = clear_state

class AlgoApiClient:
    """
    API client for interacting with an Algorand node or API server e.g. PureStake
    Currently is focused on TEAL/PyTeal source code comparisons with on-chain applications bytecode
    If an API key is provided, it will be passed to HTTP/S calls as query parameter 'api-key', otherwise no API key parameter will be passed
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def format_api_call(self, endpoint: str, args: str) -> str:
        """Format HTTP/S URL with mandatory endpoint and optional query parameter API key and arguments"""
        if args:
            url = f"{self.base_url}/{endpoint}?{args}"
        else:
            url = f"{self.base_url}/{endpoint}"
        return url

    def api_call_with_key(self, endpoint: str, args: str, verb: str, payload: dict) -> requests.Response:
        """Helper method to make an API call with key"""
        url = self.format_api_call(endpoint, args)
        api_key = {"x-api-key", self.api_key}
        if verb == "GET":
            resp = requests.get(url, headers=api_key)
        elif verb == "POST":
            if payload:
                resp = requests.post(url, headers=api_key, json=payload)
            else:
                resp = requests.post(url, headers=api_key)
        if resp.status_code != 200:
            raise HTTPError
        return resp

    def get_algo_app_bytecode(self, app_id: str) -> AlgoAppBytecode:
        """Makes a call to the /v2/applications/{app_id} endpoint. Parses out and returns the approval and clear_state program bytecode"""
        resp = self.api_call_with_key(f"v2/applications/{app_id}", None, "GET", None)
        resp_json = resp.json()
        approval_bytecode = resp_json['approval']
        clear_state_bytecode = resp_json['clear_state']
        return AlgoAppBytecode(approval_bytecode, clear_state_bytecode)

    def compile_teal(self, teal: str) -> str:
        """Given TEAL source code make a call to the /v2/teal/compile endpoint and return the compiled bytecode"""
        payload = {"teal": teal}
        resp = self.api_call_with_key("v2/teal/compile", None, "POST", payload)
        return resp.text()

    def compare_teal_to_app(self, teal_approval: str, teal_clear_state: str, app_id: str) -> bool:
        """
        Compile the TEAL source code to get the bytecode for approval and clear_state
        Make a request to receive the bytecode that matches the application ID
        Compare the compiled bytecode to the bytecode of that application ID's
        """
        approval_bytecode = self.compile_teal(teal_approval)
        clear_state_bytecode = self.compile_teal(teal_clear_state)
        expected_app_bytecode = self.get_algo_app_bytecode(app_id)

        if expected_app_bytecode.approval != approval_bytecode:
            return False

        if expected_app_bytecode.clear_state != clear_state_bytecode:
            return False
        return True
