from http import HTTPStatus
from django.test import TestCase

from .forms import AlgoSourceVerifyForm
from .models import VerifiedContract

class TestSubmitAlgoSourceVerifyForm(TestCase):
    def test_post_and_list(self):
        # This must POST a valid on-chain application to be added to the verified contracts list
        # It uses the same example from the library for an on-chain application - the tinyman AMM v1.1 application
        resp = self.client.post('', data = {
            "contract_type": "TEAL",
            "approval_url": "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal",
            "clear_state_url": "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_clear_state.teal",
             "app_id": "552635992",
             "verify_submit": "",
        })
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        # Check that the list of submitted contracts has been updated
        self.assertContains(resp, 'Verified Application ID <b><a href="https://algoexplorer.io/application/552635992">552635992</a></b>')

        contract_with_id = VerifiedContract.objects.get(app_id="552635992")
        self.assertEqual(contract_with_id.approval_url, "https://github.com/tinymanorg/tinyman-contracts-v1/blob/13acadd1a619d0fcafadd6f6c489a906bf347484/contracts/validator_approval.teal")


class TestAlgoSourceVerifyForm(TestCase):
    def test_valid_entry(self):
        # While the data here is not pointing to a valid Algorand application, it does meet the forms input requirements
        form = AlgoSourceVerifyForm(data = {
            "contract_type": "TEAL",
            "approval_url": "https://github.com/valid",
            "clear_state_url": "https://github.com/valid",
            "app_id": "123456789",
        })
        self.assertEqual(len(form.errors), 0)

    def test_invalid_entry(self):
        form = AlgoSourceVerifyForm(data = {
            "contract_type": "NON_EXISTANT_TYPE",
            "approval_url": "NOT_A_URL",
            "clear_state_url": "NOT_A_URL",
            "app_id": "123456789",
        })
        # In this case the only valid entry is the app_id, so 3 errors would be expected
        self.assertEqual(len(form.errors), 3)

class TestVerifiedContract(TestCase):
    def setUp(self):
        VerifiedContract.objects.create(contract_type="TEAL", approval_url="https://github.com/test", clear_state_url="https://github.com/test", app_id="123456789")

    def test_contract_exists(self):
        contract_with_id = VerifiedContract.objects.get(app_id="123456789")
        self.assertEqual(contract_with_id.contract_type, "TEAL")
