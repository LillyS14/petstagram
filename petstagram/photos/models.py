from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from .validators import validate_file_size


UserModel = get_user_model()

# Create your models here.
class Photo(models.Model):
    # photo = models.ImageField(upload_to="images", validators=[validate_file_size])
    photo = CloudinaryField("image")
    description = models.TextField(max_length=300, validators=[MinLengthValidator(10)], blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    tagged_pets = models.ManyToManyField("pets.Pet", related_name="photos", blank=True)
    date_of_publication = models.DateField(auto_now=True)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="photos")

    class Meta:
        ordering = ["-date_of_publication", "-pk"]
