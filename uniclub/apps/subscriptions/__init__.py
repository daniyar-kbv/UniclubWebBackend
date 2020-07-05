from django.db.models import TextChoices


class SubscriptionOperations(TextChoices):
    NEW = "NEW", "Товар куплен"
    UNIPASS_SUBSCRIPTION = "UNIPASS_SUBSCRIPTION", "Разовое посещение"
    UNICLASS_SUBSCRIPTION = "UNICLASS_SUBSCRIPTION", "Подписка на курс"
    FREEZE = "FREEZE", "Заморозка абонемента"
    DEFROST = "DEFROST", "Разморозка абонемента"


class FreezeRequestDesicion(TextChoices):
    NOT_PROCESSED = "NOT_PROCESSED", "Не обработан"
    ACCEPTED = "ACCEPTED", "Принят"
    REJECTED = "REJECTED", "Отклонен"
