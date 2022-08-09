from algorand_verifier_lib import teal_urls_match_app_id
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import AlgoSourceVerifyForm
from .models import VerifiedContract

def index(request):
    if request.method == "POST":
        form = AlgoSourceVerifyForm(request.POST)
        if form.is_valid():
            # TODO: parse the form, make the request to the library, get the result and pass it on the the verify_result handler
            # TODO: probably need to differentiate between TEAL, PyTEAL etc.
            matches = teal_urls_match_app_id(form.cleaned_data["approval_url"], form.cleaned_data["clear_state_url"], form.cleaned_data["app_id"])
            if matches:
                messages.success(request, f"Application ID {form.cleaned_data['app_id']} matches the provided source code URLs")
            else:
                messages.warning(request, f"Application ID {form.cleaned_data['app_id']} does NOT match the provided source code URLs")

            # TODO: if this key is present, then the user pressed the "Verify and Submit" button
            if "verify_submit" in request.POST and matches:
                new_verified_contract = VerifiedContract(
                        contract_type=form.cleaned_data["contract_type"], 
                        approval_url=form.cleaned_data["approval_url"],
                        clear_state_url=form.cleaned_data["clear_state_url"],
                        app_id=form.cleaned_data["app_id"],
                )
                new_verified_contract.save()
                messages.success(request, f"Application ID {form.cleaned_data['app_id']} submitted to list of verified contracts")
    else:
        form = AlgoSourceVerifyForm()

    verified_contract_object_list = VerifiedContract.objects.all()
    paginator = Paginator(verified_contract_object_list, 5)
    page = request.GET.get('page')
    try:
        verified_contracts = paginator.page(page)
    except PageNotAnInteger:
        verified_contracts = paginator.page(1)
    except EmptyPage:
        verified_contracts = paginator.page(paginator.num_pages)

    return render(request, "index.html", {
        "form": form,
        "verified_contracts": verified_contracts,
    })
