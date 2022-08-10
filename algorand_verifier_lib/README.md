# Algorand Verifier Library
Python library for verifying on-chain Algorand applications with source code.

## Usage
### Using helper functions with PureStake API
In the most general case, the simplest way to use hte library is to use functions from `helpers.py` with the PureStake API.  

First set the PURESTAKE_API_KEY envvar either on your environment or in a `.env` file in the working directory for your app:
```
export PURESTAKE_API_KEY=<YOUR_API_KEY>
echo PURESTAKE_API_KEY=<YOUR_API_KEY> >> .env
```

Then in Python code:
```
from algorand_verifier_lib import teal_urls_match_app_id

app_id = "552635992"
matches = teal_urls_match_app_id(https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal", "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_clear_state.teal", app_id)
if matches:
  print(f"The on-chain algorand application ID {app_id} matches the provided source code")
else:
  print(f"The on-chain algorand application ID {app_id} does NOT match the provided source code")
```

### Using AlgoApiClient With Custom API Endpoints
If your use-case requires more control, such as using a custom API endpoint for an Algorand node running on your local machine etc.

Against an API that requires an API key to be set:
```
from algorand_verifier_lib import AlgoApiClient

parser = OpenSourceParser()
approval_source = parser.source_from_any("https://github.com/approval_teal")
clear_state_source = parser.source_from_any("https://github.com/clear_state_teal")

app_id = "552635992"
client = AlgoApiClient("https://mainnet.api", "<YOUR_API_KEY>")
matches = client.compare_teal_to_app(approval_source, clear_state_source, app_id)
if matches:
  print("Successful match")
```

If you're using an API that doesn't require an API key, initialise the AlgoApiClient with an empty key:
```
client = AlgoApiClient("https://mainnet.api", "")
```

## Technical Design
The library is based on 3 parts with different responsibilities:

- `algo_api_client.py` contains the logic for interacting with the Algorand API endpoints and some of the lower-level verification logic e.g. `compare_teal_to_app`. Should be used directly when extra control is required such as setting the API base URL(e.g. https://mainnet-api.com, https://testnet-api.com) or making custom API calls.
- `open_source_parser.py` is responsible for parsing out source code from given URLs, for example converting a normal Github link to a raw link containing only the source code text that can then be downloaded by the library.
- `helpers.py` provides endpoint, most-general case usage functions that combine both `algo_api_client.py` and `open_source_parser.py`. It is for when the caller does not require much control such as `teal_urls_match_app_id`, which will use the PureStake API on the Algorand mainnet to verify a TEAL contract. The Django `webapp` in this repo only uses functions from `helpers.py` currently as it doesn't require any special API settings etc.

## Documentation
Create a virtualenv and install the normal requirements, and also `pdoc`:
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install pdoc
```

In the `algorand_verifier_lib` directory the src code files can be referenced to generate the documentation:
```
pdoc src/algorand_verifier_lib/*
```

This will open your browser at `localhost:8080` with the libraries documentation visible.
