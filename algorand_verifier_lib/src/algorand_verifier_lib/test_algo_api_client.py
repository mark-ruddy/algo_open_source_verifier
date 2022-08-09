import os
import pytest
from dotenv import load_dotenv, find_dotenv
from requests import HTTPError
from .algo_api_client import *

TINYMAN_AMM_APP_ID = "552635992"

def setup_purestake_algo_client() -> AlgoApiClient:
    load_dotenv()
    return AlgoApiClient("https://mainnet-algorand.api.purestake.io/ps2", os.getenv("PURESTAKE_API_KEY"))

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
    # Test against the tinyman AMM v1.1 application: https://algoexplorer.io/application/552635992
    # NOTE: Expected bytecode here will need to be updated on any changes to this application
    app_bytecode = client.get_algo_app_bytecode(TINYMAN_AMM_APP_ID)
    assert app_bytecode.approval == "BCAHAAHoB+UHBf///////////wHAhD0mDQFvAWUBcAJhMQJhMgJsdARzd2FwBG1pbnQBdAJjMQJwMQJjMgJwMjEZgQQSMRkhBBIRMRmBAhIRQATxMRkjEjEbIhIQQATjNhoAgAZjcmVhdGUSQATUMRkjEjYaAIAJYm9vdHN0cmFwEhBAA/MzAhIzAggINTQiK2I1ZSI0ZXAARDUBIicEYjVmNGZAABEiYCJ4CTEBCDMACAk1AkIACCI0ZnAARDUCIicFYjVnKDRlFlA1byI0b2I1PSg0ZhZQNXAiNHBiNT4oNGcWUDVxIjRxYjU/IipiNUA0ATQ9CTVHNAI0Pgk1SDEAKVA0ZRZQNXkxAClQNGYWUDV6MQApUDRnFlA1ezYaAIAGcmVkZWVtEkAAWjYaAIAEZmVlcxJAABw2GgAnBhI2GgAnBxIRNhoAgARidXJuEhFAAG0ANGdJRDMCERJEMwISRDMCFDIJEkQ0PzMCEgk1PzRAMwISCTVAIio0QGYiNHE0P2YjQzMCFDMCBzMCECMSTTYcARJENDREIigzAhEWUEpiNDQJZiMxAClQMwIRFlBKYjQ0CUlBAANmI0NIaCNDMgciJwhiCUk1+kEARiInCWIiJwpiNPodTEAANx4hBSMeHzX7SEhIIicLYiInDGI0+h1MQAAdHiEFIx4fNfxISEgiJwk0+2YiJws0/GYiJwgyB2YzAxIzAwgINTU2HAExABNENGdBACIiNGdwAEQ1BiIcNAYJND8INQQ2GgAnBhJAASA0ZzMEERJENhoAJwcSQABVNhwBMwQAEkQzBBI0Rx00BCMdH0hITEhJNRA0NAk1yTMEEjRIHTQEIx0fSEhMSEk1ETQ1CTXKNBA0ERBENEc0EAk1UTRINBEJNVI0BDMEEgk1U0ICCjYcATMCABJENEc0NAg1UTRINDUINVI0BCISQAAuNDQ0BB00RyMdH0hITEg0NTQEHTRIIx0fSEhMSEoNTUk0BAg1UzMEEgk1y0IBvyInBTMEEUk1Z2YoNGcWUDVxIjRncABERDRnNGUTRDRnNGYTRDMEEiQISR018DQ0NDUdNfFKDEAACBJENPA08Q5EMwQSJAgjCEkdNfA0NDQ1HTXxSg1AAAgSRDTwNPENRCQ1PzQEMwQSJAgINVNCAU82HAEzAgASRDMCETRlEjMDETRmEhBJNWRAABkzAhE0ZhIzAxE0ZRIQRDRINRI0RzUTQgAINEc1EjRINRM2GgGAAmZpEkAAWjYaAYACZm8SRDQ1JAs0Eh00EzQ1CSUdH0hITEgjCEk1FSINNDU0EwwQRDQ0NBUJNGRBABM1yTRHNBUINVE0SDQ1CTVSQgBnNco0SDQVCDVSNEc0NQk1UUIAVDQ0STUVJQs0Ex00EiQLNDQlCx4fSEhMSEk1FCINNBQ0EwwQRDQUNDUJNGRBABM1yjRHNDQINVE0SDQUCTVSQgATNck0RzQUCTVRNEg0NAg1UkIAADQVIQQLNAQdgaCcATQSHR9ISExISTUqNAQINVNCADsiKzYaARdJNWVmIicENhoCF0k1ZmY0ZXEDRIABLVCABEFMR080ZkEABkg0ZnEDRFAzAiZJFYEPTFISQyIqNEA0KghmIjRxND80Kgg0ywhmIjRvND00yQhmIjRwND40yghmIoACczE0UWYigAJzMjRSZiInCjRSIQYdNFEjHR9ISExIZiInDDRRIQYdNFIjHR9ISExIZiKAA2lsdDRTZjTLQQAJIzR7SmI0ywhmNMlBAAkjNHlKYjTJCGY0ykEACSM0ekpiNMoIZiNDI0MiQw=="
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
    int %
    INVALID
    $$£$£%
    wrongopcode22343
    return
    """
    # When invalid TEAL is provided a HTTPError should be raised by compile_teal
    with pytest.raises(HTTPError):
        client.compile_teal(sample_teal.strip())

def test_compare_teal_to_app():
    client = setup_purestake_algo_client()
    # NOTE: Similarly to get_algo_app_bytecode test, this TEAL will need to be updated for any changes to the deployed tinyman AMM v1.1 app
    test_code_dir = os.path.dirname(__file__)
    tinyman_amm_approval_file = open(os.path.join(test_code_dir, "test_content/tinyman_amm_v1.1_approval.teal"))
    tinyman_amm_approval = tinyman_amm_approval_file.read()
    tinyman_amm_clear_state = """
    #pragma version 4
    pushint 1
    """
    teal_matches = client.compare_teal_to_app(tinyman_amm_approval.strip(), tinyman_amm_clear_state.strip(), TINYMAN_AMM_APP_ID)
    assert teal_matches == True

def test_compare_teal_to_app_not_match():
    client = setup_purestake_algo_client()
    # NOTE: At this time the clear_state specified here is correct for the tinyman AMM v1.1, and the approval is specified incorrectly deliberately
    # If either do not match the on-chain values, False is expected to be returned
    tinyman_amm_incorrect_approval = """
    #pragma version 4
    int 1
    """
    tinyman_amm_clear_state = """
    #pragma version 4
    int 1
    """
    teal_not_match = client.compare_teal_to_app(tinyman_amm_incorrect_approval.strip(), tinyman_amm_clear_state.strip(), TINYMAN_AMM_APP_ID)
    assert teal_not_match == False
