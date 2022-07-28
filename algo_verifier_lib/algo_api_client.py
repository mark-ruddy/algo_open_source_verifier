class AlgoApiClient:
    """
    API client for interacting with an Algorand node or API server e.g. PureStake
    If an API key is provided, it will be passed to HTTP/S calls as query parameter 'api-key', otherwise no API key parameter will be passed
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def format_api_call(self, endpoint: str, args: str) -> str:
        """Format HTTP/S URL with mandatory endpoint and optional query parameter API key and arguments"""
        url = ""
        if self.api_key and args:
            url = f"{self.base_url}/{endpoint}?api-key={self.api_key}&{args}"
        elif self.api_key and not args:
            url = f"{self.base_url}/{endpoint}?api-key={self.api_key}"
        elif not self.api_key and args:
            url = f"{self.base_url}/{endpoint}?{args}"
        else:
            url = f"{self.base_url}/{endpoint}"
        return url
