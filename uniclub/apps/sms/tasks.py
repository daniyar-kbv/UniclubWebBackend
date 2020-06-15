import requests
from django.conf import settings

from .models import SMSMessage


def send_sms_task(recipients: str, message: str, message_id: str):
    response = requests.post(
        settings.KAZINFO_URL,
        {
            "action": "sendmessage",
            "username": settings.KAZINFO_USERNAME,
            "password": settings.KAZINFO_PASSWORD,
            "recipient": recipients,
            "messagedata": message,
            "originator": "uniclub",
            "messageType": "SMS:TEXT",
        },
        timeout=(10, 30),
    )
    data = response.json()
    if "error" in data:
        instance = SMSMessage.objects.get(uuid=message_id)
        instance.error_description = data["error"]
        instance.error_code = data.get("error_code")
        instance.save(update_fields=["error_description", "error_code"])
    return data
