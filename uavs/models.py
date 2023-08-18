from django.db import models
from users.models import User
from utils.models import BaseModel


class UAVCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "uav_categories"
        ordering = ["-created_at"]


class UAV(BaseModel):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    weight = models.FloatField()
    category = models.ManyToManyField(UAVCategory, related_name="uavs")
    is_rental = models.BooleanField(default=True)

    class Meta:
        db_table = "uavs"
        ordering = ["-created_at"]


class RentedUAV(BaseModel):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE, related_name="rented_uavs")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rented_uavs")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = "rented_uavs"
        ordering = ["-created_at"]
