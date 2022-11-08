from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import datetime

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self, data):
        user=User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()
        return user

class AssetSerializers(serializers.ModelSerializer):
    class Meta:
        model=asset_transport_request
        fields='__all__'
    def validate_asset_type(self,data):
        #print(data['asset_type'])
        if data not in {'LAPTOP', 'TRAVEL_BAG', 'PACKAGE'}:
            raise serializers.ValidationError("Valid assest type are LAPTOP,TRAVEL_BAG or PACKAGE")
        return data

    def validate_asset_type_sensitivity(self,data):
        if data not in {'HIGHLY_SENSITIVE', 'SENSITIVE', 'NORMAL'}:
            raise serializers.ValidationError("Valid sensitivity type are HIGHLY_SENSITIVE,SENSITIVE or NORMAL")
        return data

class AssetreqSerializers(serializers.ModelSerializer):
    class Meta:
        model=asset_transport_request
        fields='__all__'
    current_status=serializers.SerializerMethodField()
    def get_current_status(self,obj):
        #print(type(obj.status),type(obj.date_time_req))
        format="%Y-%m-%d %H:%M:%S"
        dt=datetime.datetime.strptime((str(obj.date_time_req)).replace('+00:00',''),format)
        if (dt-datetime.datetime.now()).total_seconds()<0 and obj.status==0:
            return "Expired"
        elif obj.status==0:
            return "Pending"
        else:
            return "Confirmed"


class RiderSerializers(serializers.ModelSerializer):
    class Meta:
        model=rider_request
        fields='__all__'
    def validate_medium_rider(self,data):
        if data not in {'BUS', 'CAR', 'TRAIN'}:
            raise serializers.ValidationError("Valid medium type are BUS, CAR or TRAIN")
        return data

            