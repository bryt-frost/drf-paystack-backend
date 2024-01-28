from django.db import models
import secrets


# Create your models here.
class Payment(models.Model):
    """Model definition for Payment."""

    PAYMENT_CHANNELS = [
        ("mobile_money", "mobile_money"),
    ]

    email = models.EmailField(max_length=100)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=16, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(
        max_length=50, choices=PAYMENT_CHANNELS, default=PAYMENT_CHANNELS[0]
    )
    verified = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Payment."""

        ordering = ["-date_created"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(16)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def __str__(self):
        """Unicode representation of Payments."""
        return "{}".format(self.amount)  # TODO
