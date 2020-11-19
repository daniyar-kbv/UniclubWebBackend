from datetime import timedelta
from typing import List, Tuple, Union

from django.db import transaction
from django.utils import timezone
from phonenumbers import PhoneNumber

from . import SMSType
from .exceptions import InvalidOTP
from .models import OTP, SMSMessage, SMSTemplate
from .tasks import send_sms_task


def send_sms(
    recipients: Union[str, List[str]],
    message: str = "",
    template_name: Union[str, Tuple[str, str]] = None,
    kwargs: dict = {},
    delta: timedelta = None,
):
    if not message:
        if not template_name:
            raise ValueError("Either content or template_name needs to be provided")
        message = SMSTemplate.objects.get(name=template_name).content
    message = message.format(**kwargs)
    if not isinstance(recipients, list):
        recipients = [recipients]
    recipients = ";".join(recipients)

    if delta:
        eta = timezone.now() + delta
    else:
        eta = None

    with transaction.atomic():
        sms = SMSMessage(recipients=recipients, content=message)
        sms.save()
        transaction.on_commit(
            lambda: send_sms_task.apply_async(
                eta=eta, args=[recipients, message, sms.uuid]
            )
        )


def send_otp(mobile_phone: PhoneNumber):
    # otp = OTP.generate(mobile_phone)
    otp = '1111'
    send_sms(
        recipients=str(mobile_phone), template_name=SMSType.OTP, kwargs={"otp": otp},
    )


def verify_otp(code: str, mobile_phone: PhoneNumber, save=False):
    otp = OTP.objects.active().filter(mobile_phone=mobile_phone).last()
    if not otp or otp.code != code:
        raise InvalidOTP

    if save:
        otp.verified = True
        otp.save(update_fields=["verified"])

    return True
