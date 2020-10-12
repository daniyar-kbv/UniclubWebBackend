from .models import Club

from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app


@celery_app.task(
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=2,
    retry_kwargs={"max_retries": 5},
    ignore_result=True
)
def remove_new(club_id):
    try:
        club = Club.objects.get(id=club_id)
    except:
        return
    club.is_new = False
    club.save()

