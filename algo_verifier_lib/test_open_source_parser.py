from open_source_parser import OpenSourceParser

def setup_open_source_parser_github() -> OpenSourceParser:
    return OpenSourceParser("https://github.com")

def setup_open_source_parser_gitlab() -> OpenSourceParser:
    return OpenSourceParser("https://gitlab.com")

def test_source_from_github_file_url():
    parser = setup_open_source_parser_github()
    source_code = parser.source_from_github_file_url("TODO")
    assert source_code == "TODO"

def test_source_from_gitlab_file_url():
    parser = setup_open_source_parser_gitlab()
    source_code = parser.source_from_gitlab_file_url("TODO")
    assert source_code == "TODO"
