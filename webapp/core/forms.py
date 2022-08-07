from django import forms

OPEN_SOURCE_FILE_HINT = "Github, Gitlab, or any URL link to file"

"""
class AlgoSourceVerifyForm(forms.Form):
    contract_types = forms.ChoiceField(label="Contract Source Code Type(WIP)", choices=[("TEAL", "TEAL"), ("PyTeal", "PyTeal"), ("Reach", "Reach")], widget=forms.Select(attrs={"class": "form-control"}))
    approval_teal_url = forms.URLField(label="Approval TEAL Source Code URL", widget=forms.TextInput(attrs={"placeholder": OPEN_SOURCE_FILE_HINT, "class": "form-control"}))
    clear_state_url = forms.URLField(label="Clear State TEAL Source Code URL", widget=forms.TextInput(attrs={"placeholder": OPEN_SOURCE_FILE_HINT, "class": "form-control"}))
    # NOTE: Algorand application IDs are always length 9 afaik
    app_id = forms.CharField(label="Algorand Application ID", max_length=9, min_length=9, widget=forms.TextInput(attrs={"placeholder": "On-Chain Application ID e.g. 552635992", "class": "form-control"}))
"""

class AlgoSourceVerifyForm(forms.Form):
    contract_types = forms.ChoiceField(label="Contract Source Code Type(WIP)", choices=[("TEAL", "TEAL"), ("PyTeal", "PyTeal"), ("Reach", "Reach")])
    approval_teal_url = forms.URLField(label="Approval TEAL Source Code URL")
    clear_state_url = forms.URLField(label="Clear State TEAL Source Code URL")
    # NOTE: Algorand application IDs are always length 9 afaik
    app_id = forms.CharField(label="Algorand Application ID", max_length=9, min_length=9)
