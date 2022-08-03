from .helpers import teal_and_app_id_matches

def test_teal_and_app_id_matches():
    matches = teal_and_app_id_matches("TODO", "TODO", "TODO")
    assert matches == True
