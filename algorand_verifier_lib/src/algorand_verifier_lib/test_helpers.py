from .helpers import teal_urls_match_app_id
from .test_algo_api_client import TINYMAN_AMM_APP_ID

TINYMAN_STAKING_APP_ID = "649588853"

def test_teal_urls_match_app_id_tinyman_amm():
    matches = teal_urls_match_app_id("https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal", "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_clear_state.teal", TINYMAN_AMM_APP_ID)
    assert matches == True

def test_teal_urls_match_app_id_tinyman_amm_incorrect_approval():
    # Link to clear_state program both times, approval will not be correct
    matches = teal_urls_match_app_id("https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_clear_state.teal", "https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_clear_state.teal", TINYMAN_AMM_APP_ID)
    assert matches == False

def test_teal_urls_match_app_id_tinyman_amm_incorrect_app_id():
    # Link to the correct AMM source code but provide the application ID for the Staking contract instead
    matches = teal_urls_match_app_id("https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal", "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_clear_state.teal", TINYMAN_STAKING_APP_ID)
    assert matches == False
