from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name


class Kitten(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kittens", verbose_name="владелец")
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        null=True,
        related_name="kittens",
        verbose_name="порода"
    )
    color = models.CharField(max_length=50, verbose_name="цвет")
    age_months = models.PositiveIntegerField(verbose_name="возраст в месяцах")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return f"{self.breed.name} - {self.color}"

