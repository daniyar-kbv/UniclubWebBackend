import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
from django.conf import settings

from uniclub import celery_app

from .models import SMSMessage


@celery_app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True
)
def send_sms_task(recipients: str, message: str, message_id: str):
    # response = requests.post(
    #     settings.KAZINFO_URL,
    #     {
    #         "action": "sendmessage",
    #         "username": settings.KAZINFO_USERNAME,
    #         "password": settings.KAZINFO_PASSWORD,
    #         "recipient": recipients,
    #         "messagedata": message,
    #         "originator": "uniclub",
    #         "messageType": "SMS:TEXT",
    #     },
    #     timeout=(10, 30),
    # )
    try:
        data = response.json()
        if "error" in data:
            instance = SMSMessage.objects.get(uuid=message_id)
            instance.error_description = data["error"]
            instance.error_code = data.get("error_code")
            instance.save(update_fields=["error_description", "error_code"])
        return data
    except Exception as exc:
        print(f"exception while trying send otp: {exc}")
        # return response.content
        return "successfully send sms"
