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

class RiderMatchSerializers(serializers.ModelSerializer):
    class Meta:
        model=rider_request
        fields='__all__'

class AssetReqGetSerializer(serializers.Serializer):
    asset_type=serializers.CharField(max_length=200,required=False)
    status=serializers.CharField(max_length=200,required=False)
    def validate_asset_type(self,data):
        if data not in {'LAPTOP', 'TRAVEL_BAG', 'PACKAGE'}:
            raise serializers.ValidationError("Valid assest type are LAPTOP,TRAVEL_BAG or PACKAGE")
        return data

    def validate_status(self,data):
        if data not in {'Pending', 'Expired', 'Confirmed'}:
            raise serializers.ValidationError("Valid status are 'Pending', 'Expired', 'Confirmed'")
        return data

class MatchSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    page=serializers.IntegerField(required=False,default=1)
    def validate_page(self,data):
        if data<=0:
            raise serializers.ValidationError("Page number cannot be greater less than or equal to zero")
        return data

class SelectSerializer(serializers.Serializer):
    ride_id=serializers.IntegerField()
    request_id=serializers.IntegerField()



            