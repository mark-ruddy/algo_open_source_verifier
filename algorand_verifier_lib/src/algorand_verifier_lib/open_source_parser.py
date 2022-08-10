import requests

class OpenSourceParser:
    """
    Used to parse Open Source websites for TEAL contracts.
    Currently supports Github and Gitlab.
    """
    GITHUB_BASE_URL = "https://github.com"
    GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com"
    GITLAB_BASE_URL = "https://gitlab.com"

    def source_from_any(self, url: str) -> str:
        """
        Helper method that simplifies using this parser for URLs that aren't guaranteed to be on a certain hoster e.g. Github.
        Attempts to make a request against either Github or Gitlab by interpreting the URL.
        If neither a Github or Gitlab URL is identified, make a request against the URL with no parsing - could be useful for source code on miscellaneous webservers etc.
        """
        if self.GITHUB_BASE_URL in url or self.GITHUB_RAW_BASE_URL in url:
            return self.source_from_github_file_url(url)
        elif self.GITHUB_BASE_URL in url:
            return self.source_from_gitlab_file_url(url)
        else:
            resp = requests.get(url)
            resp.raise_for_status()
            return resp.text

    def source_from_github_file_url(self, github_file_url: str) -> str:
        """Return the source code text given a standard Github file URL"""
        # If the provided URL already contains the raw base URL, attempt to download file with no URL parsing
        if self.GITHUB_RAW_BASE_URL in github_file_url:
            resp = requests.get(github_file_url)
            resp.raise_for_status()
            return resp.text
        # Remove blob/ from the URL path and change the base URL to raw
        removed_blob_url = github_file_url.replace("blob/", "")
        raw_github_file_url = removed_blob_url.replace(self.GITHUB_BASE_URL, self.GITHUB_RAW_BASE_URL)
        resp = requests.get(raw_github_file_url)
        resp.raise_for_status()
        return resp.text

    def source_from_gitlab_file_url(self, gitlab_file_url: str) -> str:
        """Return the source code text given a standard Gitlab file URL""" 
        raw_gitlab_file_url = gitlab_file_url.replace("blob", "raw")
        resp = requests.get(raw_gitlab_file_url)
        resp.raise_for_status()
        return resp.text
