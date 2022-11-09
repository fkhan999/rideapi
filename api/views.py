#from django.http import JsonResponse
from urllib import response
from django.forms.models import model_to_dict
import json
from api.models import asset_transport_request,rider_request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import datetime
from .serializers import *
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

valid_asset_type={'LAPTOP', 'TRAVEL_BAG', 'PACKAGE'}
valid_sensitivity={'HIGHLY_SENSITIVE', 'SENSITIVE', 'NORMAL'}
valid_travel_mediums={'BUS', 'CAR', 'TRAIN'}


#This view is for testing purposes
@api_view(['GET'])
def home(request,*args,**kwargs):
    b=request.body
    print(request.GET,b,dict(request.GET))
    try:
        b=json.loads(b)
    except:
        b={"msg-error":str(b)}
        pass
    b['headers']=dict(request.headers)
    b['data']=dict(request.GET)
    print(dict(request.GET))
    b['content_type']=request.content_type
    return Response(b)

@api_view(['POST'])
def createUser(request,*args,**kwargs):
    serializer=UserSerializers(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    serializer.save()
    return Response({"message":"User created succesfully"},status=200)

#This view is for creating new asset request for requester
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def asset_req(request,*args,**kwargs):
    request.data['user_req']=str(request.user)
    serializer=AssetSerializers(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    serializer.save()
    return Response({"message":"Request created succesfully with id "+str(serializer.data['id'])},status=200)


#This view is for creating new ride information request by rider
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def rider_req(request,*args,**kwargs):
    request.data['user_rider']=str(request.user)
    serializer=RiderSerializers(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    serializer.save()
    return Response({"message":"Request created succesfully with id "+str(serializer.data['id'])},status=200)


#This view is for viewing request sent by a requester
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def asset_req_get(request,*args,**kwargs):
    a=request.data
    serializer=AssetReqGetSerializer(data=a)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    data=asset_transport_request.objects.filter(user_req=str(request.user))
    try:
        data=data.filter(asset_type=serializer.data['asset_type'])
    except:
        pass
    serializer=AssetreqSerializers(data,many=True)
    try:
        if a['status']:
            result = filter(lambda x: x['current_status'] == a['status'], serializer.data)
    except:
        result=serializer.data
    return Response({"asset req":result,"message":"Requests successfully fetched"})
  


#This view is for  viewing match with rider
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def match(request,*args,**kwargs):
    serializer=MatchSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    try:
        data=asset_transport_request.objects.get(id=serializer.data['id'])
    except:
        return Response({"message":"No matching request"},status=404)
    data=model_to_dict(data)
    data=rider_request.objects.filter(from_rider=data['from_req'],to_rider=data['to_req'],date_time_rider=data['date_time_req'])[(serializer.data['page']-1)*5:serializer.data['page']*5]
    serializer=RiderMatchSerializers(data,many=True)
    if len(serializer.data)==0:
        return Response({"error":"No request on this page"},status=404)
    return Response({"Match req":serializer.data,"message":"Requests successfully fetched"})

#this view is for selecting a rider out of match
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def rider_select(request,*args,**kwargs):
    print(str(request.user))
    serializer=SelectSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors,"message":"Please provide correct data"},status=403)
    try:
        data=asset_transport_request.objects.get(user_req=str(request.user),id=serializer.data['request_id'])
    except:
        return Response({"message":"No record exists for requester id: "+str(serializer.data['request_id'])},status=404)
    try:
        rider_request.objects.get(id=serializer.data['ride_id'])
    except:
        return Response({"message":"No record exists for rider id: "+str(serializer.data['ride_id'])},status=404)
    data.status=serializer.data['ride_id']
    data.save()
    return Response({"message":"Request id "+str(serializer.data['request_id'])+" successfully matched with ride id "+str(serializer.data['ride_id'])},status=200)