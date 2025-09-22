from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
import requests
import json
from .models import *
from home.forms import ContactForms


# url = "https://api.bitrah.ir/api/v1/order/submit/wr"
#
# payload = json.dumps({
#     "merchantId": "62b45724ea84459da8215689bb7d07a3",
#     "orderId": "1‬‬",
#     "rialValue": 40000,
#     "callbackUrl": "https://wi-hub.com/",
#     "webhookUrl": "https://wi-hub.com/order/bitrahTransactionStatus/?smId=",
#     "coin": "TRX"
# })
# headers = {
#     'Authentication': 'bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzc3dhbjE5NzMiLCJBdXRoZW50aWNhdGlvbiI6Ik9SREVSX1dSSVRFLE1FUkNIQU5UX1BBTkVMX1dSSVRFLE1FUkNIQU5UX1BBTkVMX0NPTU1BTkQsTUVSQ0hBTlRfUEFORUxfUkVBRCxPUkRFUl9SRUFELE9SREVSX0NPTU1BTkQiLCJpYXQiOjE2NzIzMTQwNjIsImV4cCI6MTY3MjQwMDQ2Mn0.y1g8fTzG9qUABehpwgOrhndE-3SKPRiCyyhRvkkRNRc',
#     'Accept-Language': '/fa-IR',
#     'Content-Type': 'application/json',
#     'username': 'sswan1973'
# }


def home(request):
    msg = request.GET.get("msg", None)
    context = {"msg": msg}
    return render(request, "home/home.html", context)


def test(request):
    return render(request, "home/test.html")


def about(request):
    return render(request, "home/about.html")


def shares(request):
    return render(request, "home/shares.html")


def cooparation(request):
    return render(request, "home/cooparation.html")


@login_required(login_url="/account/login")
def saving(request):
    if request.POST:
        amount = request.POST.get("saving")
        obj = Share(type=6, user=request.user, number=amount)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    else:
        return render(request, "home/saving.html")


@login_required(login_url="/account/login")
def paper_shares(request):
    if request.POST:
        number = request.POST.get("number")
        obj = Share(type=1, user=request.user, number=number)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    return render(request, "home/paper_shares.html")


@login_required(login_url="/account/login")
def methanol_shares(request):
    if request.POST:
        number = request.POST.get("number")
        obj = Share(type=5, user=request.user, number=number)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    return render(request, "home/methanol_shares.html")


@login_required(login_url="/account/login")
def waterring_shares(request):
    if request.POST:
        number = request.POST.get("number")
        obj = Share(type=3, user=request.user, number=number)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    return render(request, "home/waterring_shares.html")


@login_required(login_url="/account/login")
def towers_shares(request):
    if request.POST:
        number = request.POST.get("number")
        obj = Share(type=4, user=request.user, number=number)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    return render(request, "home/towers_shares.html")


@login_required(login_url="/account/login")
def aircraft_shares(request):
    if request.POST:
        # response = requests.request("POST", url, headers=headers, data=payload)
        # redirect = response.json()["data"]['redirectUrl']
        number = request.POST.get("number")
        obj = Share(type=2, user=request.user, number=number)
        obj.save()
        msg = "register_done"
        return HttpResponseRedirect(reverse("share_payment", kwargs={'share_id': obj.id}) + "?" + "msg=" + str(msg))
    return render(request, "home/aircraft_shares.html")


def paper(request):
    if request.POST:
        return HttpResponseRedirect(reverse("paper_shares"))
    return render(request, "home/paper.html")


def methanol(request):
    if request.POST:
        return HttpResponseRedirect(reverse("methanol_shares"))
    return render(request, "home/methanol.html")


def towers(request):
    if request.POST:
        return HttpResponseRedirect(reverse("towers_shares"))
    return render(request, "home/towers.html")


def aircraft(request):
    if request.POST:
        return HttpResponseRedirect(reverse("aircraft_shares"))
    return render(request, "home/aircraft.html")


def water(request):
    if request.POST:
        return HttpResponseRedirect(reverse("waterring_shares"))
    return render(request, "home/water.html")


@login_required(login_url="/account/login")
def share_payment(request, share_id):
    msg = request.GET.get("msg")
    the_share = get_object_or_404(Share, pk=share_id)
    if the_share.user != request.user or the_share.payment:
        return render(request, "home/404.html")
    context = {
        "the_share": the_share,
        "msg": msg,
    }
    if request.POST:
        if request.POST.get("txid") == '':
            return redirect(reverse("share_payment", kwargs={"share_id": the_share.id}))
        else:
            the_share.txid = request.POST.get("txid")
            the_share.payment = True
            the_share.valid = 1
            the_share.save()
            msg = "transaction"
            return redirect(reverse("profile") + "?" + "msg=" + str(msg))
    return render(request, "home/share_payment.html", context)


@login_required(login_url="/account/login")
def share_details(request, share_id):
    the_share = get_object_or_404(Share, pk=share_id)
    if the_share.user != request.user:
        return render(request, "home/404.html")
    context = {
        "the_share": the_share
    }
    if request.POST:
        the_share.txid = request.POST.get("txid")
        the_share.payment = True
        the_share.valid = 1
        the_share.save()
        msg = "transaction"
        return redirect(reverse("profile") + "?" + "msg=" + str(msg))
    return render(request, "home/share_details.html", context)


def contact_us(request):
    contact_form = ContactForms(request.POST or None)
    msg = request.GET.get("msg")
    context = {
        "contact_form": contact_form,
        "msg": msg
    }
    if request.POST:
        if contact_form.is_valid():
            email = contact_form.cleaned_data.get('email')
            text = contact_form.cleaned_data.get('text')
            obj = Ticket(email=email, text=text)
            obj.save()
            msg = "contact_us"
            return redirect(reverse("contact_us") + "?" + "msg=" + str(msg))
    return render(request, "home/contact.html", context)


def error_500(request):
    return render(request, 'home/500.html', status=500)
