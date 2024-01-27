from django.db import models

# Create your models here.
class Payment(models.Model):
    """Model definition for Payment."""

    email=models.EmailField()
    ref=models.CharField(max_length=50)
    amount=models.PositiveIntegerField()
    date_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Payment."""

        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        """Unicode representation of Payments."""
        return '{}'.format(self.amount ) # TODO
