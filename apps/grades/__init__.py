from django.db.models import TextChoices


class Levels(TextChoices):
    ALL = "ALL", "Все"
    BEGINNER = "BEGINNER", "Начальный"
    MIDDLE = "MIDDLE", "Средний"
    ADVANCED = "ADVANCED", "Продвинутый"
    MASTER = "MASTER", "Мастер"


class Intensities(TextChoices):
    ALL = "ALL", "Все"
    LOW = "LOW", "Низкая"
    MEDIUM = "MEDIUM", "Средняя"
    HIGH = "HIGH", "Высокая"


class Durations(TextChoices):
    PERIODIC = "PERIODIC", "Периодичный"
    LONG = "LONG", "Продолжительный"
