from datetime import timedelta
from algorand_verifier_lib import teal_urls_match_app_id
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .forms import AlgoSourceVerifyForm
from .models import VerifiedContract

def index(request):
    if request.method == "POST":
        form = AlgoSourceVerifyForm(request.POST)
        if form.is_valid():
            matches = teal_urls_match_app_id(form.cleaned_data["approval_url"], form.cleaned_data["clear_state_url"], form.cleaned_data["app_id"])
            if matches:
                messages.success(request, f"Application ID {form.cleaned_data['app_id']} matches the provided source code URLs")
            else:
                messages.warning(request, f"Application ID {form.cleaned_data['app_id']} does NOT match the provided source code URLs")

            # If this key is present, then the user pressed the "Verify and Submit" button
            if "verify_submit" in request.POST and matches:
                ip = get_client_ip(request)
                new_verified_contract = VerifiedContract(
                        contract_type="TEAL", 
                        approval_url=form.cleaned_data["approval_url"],
                        clear_state_url=form.cleaned_data["clear_state_url"],
                        app_id=form.cleaned_data["app_id"],
                        submitter_ip=ip,
                )

                # Basic spam protection, prevent the same IP from submitting the same contract to the list within a short timeframe
                within_five_mins = timezone.now() - timedelta(minutes=5)
                recent_identical_exists = VerifiedContract.objects.filter(
                        created__gte=within_five_mins, 
                        approval_url=form.cleaned_data["approval_url"],
                        clear_state_url=form.cleaned_data["clear_state_url"],
                        app_id=form.cleaned_data["app_id"],
                        submitter_ip=ip,
                )
                if recent_identical_exists:
                        messages.warning(request, f"An identical submission for Application ID {form.cleaned_data['app_id']} has been made in the last 5 minutes. Please wait before submitting to list.")
                else:
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

# See: https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
