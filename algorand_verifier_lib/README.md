# Algorand Verifier Library
Python library for verifying on-chain Algorand applications with source code. Available on PyPi at <https://pypi.org/project/algorand-verifier-lib/>

## Usage
Install using pip: `pip install algorand_verifier_lib`

### Using helper functions with PureStake API
In the most general case, the simplest way to use the library is to use functions from `helpers.py` with the PureStake API.  

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
from algorand_verifier_lib import AlgoApiClient, OpenSourceParser

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

## Testing
The tests for the library use the PureStake API and make real API calls so they can take some time, usually though no more than 10 seconds.  

The tests will run with Github Actions CI on every push, but it sometimes may be required to run the tests locally.  

Assuming you are in the `algorand_verifier_lib` lib directory that contains this `README.md`:
```
export PURESTAKE_API_KEY=<YOUR_API_KEY>

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python -m pytest src/algorand_verifier_lib
```

If any errors are encountered related to 403 HTTP authentication etc., ensure that the `PURESTAKE_API_KEY` envvar is correct.

## Releasing New Versions on PyPi
Update the new package version and any other info in `setup.py`  

Then run `python setup.py sdist` to produce a source code distributable under `dist/`  

Install Twine `pip install twine` and then the contents of the `dist/` directory can be uploaded, you must authenticate as the package owner: `twine upload dist/*`  

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

## Technical Design
The library is based on 3 parts with different responsibilities:

- `algo_api_client.py` contains the logic for interacting with the Algorand API endpoints and some of the lower-level verification logic e.g. `compare_teal_to_app`. Should be used directly when extra control is required such as setting the API base URL(e.g. https://mainnet-api.com, https://testnet-api.com) or making custom API calls.
- `open_source_parser.py` is responsible for parsing out source code from given URLs, for example converting a normal Github link to a raw link containing only the source code text that can then be downloaded by the library.
- `helpers.py` provides endpoint, most-general case usage functions that combine both `algo_api_client.py` and `open_source_parser.py`. It is for when the caller does not require much control such as `teal_urls_match_app_id`, which will use the PureStake API on the Algorand mainnet to verify a TEAL contract. The Django `webapp` in this repo only uses functions from `helpers.py` currently as it doesn't require any special API settings etc.

This will open your browser at `localhost:8080` with the libraries documentation visible.

### Why PyTeal and Reach is not Currently Supported
This verifier library works with TEAL only. Support for PyTeal and Reach contracts would be a definite nice-to-have though, for example the `OpenSourceParser` could convert a PyTeal contract to TEAL. Once it's converted to TEAL the normal source code verification logic could be used.  

List of reasons why this is not supported:
- There is no clear way to convert PyTeal/Reach contracts to TEAL in a generic form, that would work for ALL contracts source code. As discussed below there are some 'hacks' like finding the `approval_program()` function in PyTeal, but naming the function that is just a convention and will not be the same in all contracts.
- I believe to convert you would need to execute the PyTeal/Reach code, for example the verifier library could add some code to a PyTeal source code file that converts as demonstrated below(example code sourced from https://github.com/ChoiceCoin/Smart_Contracts):

```
if __name__ == "__main__":
  with open("compiled/"+ "vote_approval.teal", "w") as f:
      compiled = compileTeal(approval_program(), mode=Mode.Application, version=2)
      f.write(compiled)

  with open("compiled/"+"vote_clear_state.teal", "w") as f:
      compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=2)
      f.write(compiled)
```

A problem I have with this is that this introduces a RCE(Remote-Code-Execution) vulnerability to the library, a maliciously written Python source code file could be specified and get executed on the library side, which may be running in a webserver.

- The majority of open source Algorand contracts have a `compiled/` directory or equivalent with the TEAL even if the contract itself is written in PyTeal/Reach. This means that even without this functionality this library should still be able to verify the large majority of open source Algorand contracts.

Possibly a good solution could be found for converting these PyTeal/Reach contracts to TEAL reliably and safely, if this exists I will 100% implement it. I cannot find a solution currently so this functionality will not be included in this library at this time.
