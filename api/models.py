from django.db import models

# Create your models here.


class asset_transport_request(models.Model):
    user_req=models.CharField(max_length=10)
    from_req=models.CharField(max_length=150)
    to_req=models.CharField(max_length=150)
    date_time_req=models.DateTimeField()
    is_flex_req=models.BooleanField(default=False)
    quantity_req=models.IntegerField()
    asset_type=models.CharField(max_length=20)
    asset_type_sensitivity=models.CharField(max_length=20)
    deliver=models.CharField(max_length=150)
    status=models.IntegerField(default=0)
    class Meta:
        ordering = ['date_time_req']
    
    
    
    


class rider_request(models.Model):
    user_rider=models.CharField(max_length=10)
    from_rider=models.CharField(max_length=150)
    to_rider=models.CharField(max_length=150)
    date_time_rider=models.DateTimeField()
    is_flex_rider=models.BooleanField(default=False)
    medium_rider=models.CharField(max_length=20)
    quantity_rider=models.IntegerField()