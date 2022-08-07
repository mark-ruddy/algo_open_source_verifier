from algorand_verifier_lib import teal_urls_match_app_id
from django.shortcuts import HttpResponseRedirect, render
from django.contrib import messages
from .forms import AlgoSourceVerifyForm

def index(request):
    if request.method == "POST":
        form = AlgoSourceVerifyForm(request.POST)
        if form.is_valid():
            # TODO: parse the form, make the request to the library, get the result and pass it on the the verify_result handler
            # TODO: probably need to differentiate between TEAL, PyTEAL etc.
            print(form.cleaned_data["approval_teal_url"], form.cleaned_data["clear_state_url"], form.cleaned_data["app_id"])
            matches = teal_urls_match_app_id(form.cleaned_data["approval_teal_url"], form.cleaned_data["clear_state_url"], form.cleaned_data["app_id"])
            print(matches)
            if matches:
                messages.success(request, f"Application with ID {form.cleaned_data['app_id']} matches the provided source code URLs")
            else:
                messages.warning(request, f"Application with ID {form.cleaned_data['app_id']} does NOT match the provided source code URLs")

            # TODO: if this key is present, then the user pressed the "Verify and Submit" button
            if "verify_submit" in form.cleaned_data:
                pass
            return render(request, "index.html", {"form": form})
    else:
        form = AlgoSourceVerifyForm()
    return render(request, "index.html", {'form': form})

def verify_result(request):
    pass

def about(request):
    return render(request, "about.html", {})
