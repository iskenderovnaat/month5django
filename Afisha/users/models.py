import random
from django.db import models
from django.contrib.auth.models import User

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))


print(ConfirmationCode.generate_code())