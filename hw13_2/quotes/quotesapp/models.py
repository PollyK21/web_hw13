from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    fullname = models.CharField(max_length=250)
    born_date = models.CharField(max_length=250)
    born_location = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return f"{self.fullname}"


class Quotes(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"
