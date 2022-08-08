from django.db import models

class VerifiedContract(models.Model):
    objects = models.Manager()
    contract_type = models.CharField(max_length=64)
    approval_url = models.CharField(max_length=65536)
    clear_state_url = models.CharField(max_length=65536)
    app_id = models.CharField(max_length=9)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title
