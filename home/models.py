from django.db import models
from django.contrib.auth.models import User
from extensions.log_error_middleware import get_exact_exception_info


class Share(models.Model):
    PAPER = 1
    AIRPLANE = 2
    WATER = 3
    TOWERS = 4
    METHANOL = 5
    SAVING = 6
    type_choices = (
        (PAPER, 'paper'),
        (AIRPLANE, 'airplane'),
        (WATER, 'water'),
        (TOWERS, 'towers'),
        (METHANOL, 'methanol'),
        (SAVING, 'saving'),
    )
    UNDONE = 0
    PENDING = 1
    CONFIRMED = 2
    NOT_CONFIRMED = 3
    the_choices = (
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
        (NOT_CONFIRMED, 'not confirmed'),
        (UNDONE, "undone")
    )
    unconfirmed_reason = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=type_choices)
    number = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.BooleanField(default=False)
    valid = models.IntegerField(choices=the_choices, default=1)
    time = models.DateTimeField(auto_now_add=True)
    txid = models.CharField(max_length=200, null=True, blank=True)

    def total_price(self):
        return self.number * 100

    def __str__(self):
        return f"{self.user.username}={self.number}number of {self.get_type_display()}"


class Ticket(models.Model):
    email = models.EmailField()
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SystemExceptions(models.Model):
    date_created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    login_username = models.CharField("نام کاربری کاربر", max_length=50, null=True, blank=True)
    file_path = models.CharField("مسیر محل قرارگیری کد", max_length=250, null=True, blank=True)
    line_number = models.IntegerField("شماره خط", null=True, blank=True)
    exception_name = models.CharField("عنوان خطا", max_length=250, null=True, blank=True)
    exception_content = models.TextField("محتوای خطا")
    exact_info = models.TextField("اطلاعات دقیق خطا", null=True, blank=True)
    url = models.CharField("آدرس", max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "error_logs"
        verbose_name_plural = "error_logs"

    def __str__(self):
        return self.url

    @classmethod
    def create_log(cls, user, path, line, content, name=None, url=None, ip=None, is_deleted=False,
                   middleware=None):
        exception_log = cls(file_path=path, line_number=line, exception_name=name,
                            exception_content=content, url=url, )
        if user:
            if user.is_anonymous:
                exception_log.login_username = str(user)
            else:
                exception_log.login_username = user.username
                if ip:
                    exception_log.login_username += "\n" + str(ip)

        exception_log.exact_info = get_exact_exception_info()
        exception_log.save()
        return exception_log
