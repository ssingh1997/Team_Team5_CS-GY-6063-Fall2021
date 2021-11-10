from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


class Food_Avail(models.Model):
    food_available = models.IntegerField()
    description = models.TextField(blank=True)
    available_till = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def allow_only_one_instance(self, instance):
        if len(Food_Avail.objects.filter(author=instance.author)) > 0:
            raise ValidationError("User has already created food availibility post!")