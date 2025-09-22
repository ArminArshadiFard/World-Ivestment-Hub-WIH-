from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .forms import RegisterForms, LoginForms
from django.contrib.auth.models import User
from account.models import ValidationCode
# from .forms import CaptchaTestForm
from home.models import Share
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import random


# def some_view(request):
#     if request.POST:
#         form = CaptchaTestForm(request.POST)
#
#         # Validate the form: the captcha field will automatically
#         # check the input
#         if form.is_valid():
#             human = True
#     else:
#         form = CaptchaTestForm()
#
#     return render(request, 'home/captcha.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    login_forms = LoginForms(request.POST or None)
    if login_forms.is_valid():
        email = login_forms.cleaned_data.get('email')
        password = login_forms.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        not_verify = User.objects.filter(username=email).first()
        if user is not None:
            if not not_verify.is_active:
                new_code = random.randint(11111, 99999)
                user_profile = ValidationCode.objects.get(user=not_verify)
                user_profile.code = new_code
                user_profile.send_email_status = 0
                user_profile.save()
                return redirect(reverse("email_validation") + "?" + "value=" + str(not_verify.id))
            else:
                login(request, user)
                if request.GET.get("next"):
                    return HttpResponseRedirect(request.GET.get("next"))
                msg = "login"
                return redirect('/' + "?" + "msg=" + str(msg))
        else:
            login_forms.add_error('email', 'Password or email is wrong')
    context = {
        "login_form": login_forms
    }
    return render(request, "account/login.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_forms = RegisterForms(request.POST or None)
    context = {
        "register_form": register_forms
    }
    if register_forms.is_valid():
        name = register_forms.cleaned_data.get('name')
        password = register_forms.cleaned_data.get('password')
        email = register_forms.cleaned_data.get('email')
        obj = User.objects.create_user(username=email, password=password, first_name=name, is_active=False)
        obj.save()
        code = random.randint(11111, 99999)
        vs = ValidationCode(code=code, user_id=obj.id)
        vs.save()
        return redirect(reverse("email_validation") + "?" + "value=" + str(obj.id))
    return render(request, "account/register.html", context)


def email_validation(request):
    user_id = request.GET.get("value", None)
    the_user = User.objects.get(id=user_id)
    code = the_user.profile_user.code
    error = request.GET.get("error")
    context = {"error": error}
    if the_user.is_active:
        return render(request, "home/404.html")
    if request.POST:
        if "caller" in request.POST:
            code = random.randint(11111, 99999)
            x = ValidationCode.objects.filter(user_id=user_id)[0]
            x.code = code
            x.send_email_status = 0
            x.save()
            return redirect("/account/email_validation?value=" + str(the_user.id))
        else:
            if str(code) == request.POST.get("code") and request.POST.get("code").isdigit():
                the_user.is_active = True
                the_user.save()
                login(request, the_user)
                msg = "registration"
                return redirect("/" + "?" + "msg=" + str(msg))
            else:
                context.update({"not_valid": "The validation code is not right"})
                return redirect(
                    reverse("email_validation") + "?" + "value=" + str(
                        the_user.id) + "&" + "error=" + "The code is not valid")
    return render(request, "account/email_validation.html", context)


@login_required(login_url="/account/login")
def logout_view(request):
    logout(request)
    msg = "logout"
    return redirect('/' + "?" + "msg=" + str(msg))


@login_required(login_url="/account/login")
def profile(request):
    msg = request.GET.get("msg")
    user_shares = Share.objects.filter(user=request.user).order_by("-time")
    context = {
        "user_shares": user_shares,
        "msg": msg
    }
    return render(request, "account/profile.html", context)


@login_required(login_url="/account/login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            update_session_auth_hash(request, user)
            msg = "change_password"
            return redirect(reverse("profile") + "?" + "msg=" + str(msg))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "account/change_password.html", {"form": form})
