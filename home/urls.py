from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about", about, name="about"),
    path("shares", shares, name="shares"),
    path("shares/cooparation", cooparation, name="cooparation"),
    path("shares/saving", saving, name="saving"),
    path("shares/paper", paper, name="paper"),
    path("shares/methanol", methanol, name="methanol"),
    path("shares/towers", towers, name="towers"),
    path("shares/methanol", methanol, name="methanol"),
    path("shares/aircraft", aircraft, name="aircraft"),
    path("shares/water", water, name="water"),
    path("shares/paper_shares", paper_shares, name="paper_shares"),
    path("shares/methanol_shares", methanol_shares, name="methanol_shares"),
    path("shares/waterring_shares", waterring_shares, name="waterring_shares"),
    path("shares/towers_shares", towers_shares, name="towers_shares"),
    path("shares/aircraft_shares", aircraft_shares, name="aircraft_shares"),
    path("contact_us", contact_us, name="contact_us"),
    path("share/payment/<int:share_id>", share_payment, name="share_payment"),
    path("share/details/<int:share_id>", share_details, name="share_details"),
    path("test/", test),
]
