from django.db.models import TextChoices


class SubscriptionOperations(TextChoices):
    NEW = "NEW", "Товар куплен"
    UNIPASS_SUBSCRIPTION = "UNIPASS_SUBSCRIPTION", "Разовое посещение"
    UNICLASS_SUBSCRIPTION = "UNICLASS_SUBSCRIPTION", "Подписка на курс"
    FREEZE = "FREEZE", "Заморозка абонемента"


class FreezeRequestDesicion(TextChoices):
    NOT_PROCESSED = "NOT_PROCESSED", "Не обработан"
    ACCEPTED = "ACCEPTED", "Принят"
    REJECTED = "REJECTED", "Отклонен"


class SubscriptionStatuses(TextChoices):
    ACTIVE = "ACTIVE", "Активна"
    FROZEN = "FROZEN", "Заморожена"
    INACTIVE = "INACTIVE", "Неактивна"
