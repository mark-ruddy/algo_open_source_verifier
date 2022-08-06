from .open_source_parser import OpenSourceParser

EXPECTED_LINUX_COCCI_CONF = """
[spatch]
\toptions = --timeout 200
\toptions = --use-gitgrep
"""

def test_source_from_github_file_url():
    parser = OpenSourceParser()
    source_code = parser.source_from_github_file_url("https://github.com/torvalds/linux/blob/master/.cocciconfig")
    assert source_code.strip() == EXPECTED_LINUX_COCCI_CONF.strip()

def test_source_from_gitlab_file_url():
    parser = OpenSourceParser()
    source_code = parser.source_from_gitlab_file_url("https://gitlab.com/linux-kernel/stable/-/blob/master/.cocciconfig")
    assert source_code.strip() == EXPECTED_LINUX_COCCI_CONF.strip()
