import requests
from requests.models import HTTPError

class OpenSourceParser:
    """
    Used to parse Open Source websites for TEAL contracts
    Currently supports Github and Gitlab
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def source_from_github_file_url(self, github_file_url: str) -> str:
        """Return the source code text given a standard Github file URL"""
        if github_file_url.contains("https://raw.githubusercontent.com"):
            resp = requests.get(github_file_url)
            if resp.status_code != 200:
                raise HTTPError
            return resp.text()
        removed_blob_url = github_file_url.replace("blob/", "")
        with_raw_base_url = removed_blob_url.replace("https://github.com", "https://raw.githubusercontent.com")
        resp = requests.get(with_raw_base_url)
        if resp.status_code != 200:
            raise HTTPError
        # TODO: just return text content?
        return resp.text()

    def source_from_gitlab_file_url(self, gitlab_file_url: str) -> str:
        pass
