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


class FreezeDuration(TextChoices):
    THREE_DAYS = 'THREE_DAYS', 'На 3 дня'
    ONE_WEEK = 'ONE_WEEK', 'На неделю'
    TWO_WEEKS = 'TWO_WEEKS', 'На 2 недели'


class SubscriptionStatuses(TextChoices):
    ACTIVE = "ACTIVE", "Активна"
    FROZEN = "FROZEN", "Заморожена"
    INACTIVE = "INACTIVE", "Неактивна"
