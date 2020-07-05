from django.db.models import TextChoices


class ProductType(TextChoices):
    UNICLASS = "UNICLASS", "UniClass"
    UNIPASS = "UNIPASS", "UniPass"
