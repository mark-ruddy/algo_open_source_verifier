from django import forms

OPEN_SOURCE_FILE_HINT = "Github, Gitlab, or any URL link to source code file"

class AlgoSourceVerifyForm(forms.Form):
    # NOTE: For now contract_type will not be included and this app will only support TEAL contracts
    # contract_type = forms.ChoiceField(label="Contract Source Code Type(WIP)", choices=[("TEAL", "TEAL"), ("PyTeal", "PyTeal"), ("Reach", "Reach")], widget=forms.Select(attrs={"class": "form-control"}))
    approval_url = forms.URLField(label="Approval TEAL Source Code URL", widget=forms.TextInput(attrs={"placeholder": OPEN_SOURCE_FILE_HINT, "class": "form-control"}))
    clear_state_url = forms.URLField(label="Clear State TEAL Source Code URL", widget=forms.TextInput(attrs={"placeholder": OPEN_SOURCE_FILE_HINT, "class": "form-control"}))
    # Algorand application IDs are always length 9
    app_id = forms.CharField(label="Algorand Application ID", max_length=9, min_length=9, widget=forms.TextInput(attrs={"placeholder": "On-Chain Application ID e.g. 552635992", "class": "form-control"}))
