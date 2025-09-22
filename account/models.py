from django.db import models
from django.contrib.auth.models import User


class ValidationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='نام کاربر',
                                related_name='profile_user')
    code = models.IntegerField()
    updated_time = models.DateTimeField(auto_now=True)
    UNSEND = 0
    SEND = 1
    the_choices = (
        (UNSEND, 'unsend'),
        (SEND, 'send'),
    )
    send_email_status = models.IntegerField(choices=the_choices, default=0)

    def __str__(self):
        return str(self.code)
