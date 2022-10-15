#from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from api.models import asset_transport_request,rider_request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import datetime
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

#This view is for creating new asset request for requester
@api_view(['POST'])
def asset_req(request,*args,**kwargs):
    try:
        a=json.loads(request.body)
        print(a)
        format="%Y-%m-%d %H:%M:%S"
        if a["asset_type"].upper() not in valid_asset_type:
            return Response({"message":a['asset_type']+" is not valid assest type"})
        if a["sensitivity"].upper() not in valid_sensitivity:
            return Response({"message":a['sensitivity']+" is not valid sensitivity"})
        asset_transport_request.objects.create(user_req=a["user"],from_req=a["from"],to_req=a["to"],date_time_req=datetime.datetime.strptime(a['date_time'],format),is_flex_req=a["is_flex"],quantity_req=a["quantity"],asset_type=a["asset_type"],asset_type_sensitivity=a["sensitivity"],deliver=a['deliver'])
    except Exception as e:
        print(e)
        return Response({"message":"data not valid"})
    data={"message":"request successfully added"}
    data['data']=a
    return Response(data)


#This view is for creating new ride information request by rider
@api_view(['POST'])
def rider_req(request,*args,**kwargs):
    try:
        a=json.loads(request.body)
        print(a)
        format="%Y-%m-%d %H:%M:%S"
        if a["medium"].upper() not in valid_travel_mediums:
            return Response({"message":a['medium']+" is not valid travel medium"},status=500)
        rider_request.objects.create(user_rider=a["user"],from_rider=a["from"],to_rider=a["to"],date_time_rider=datetime.datetime.strptime(a['date_time'],format),is_flex_rider=a["is_flex"],quantity_rider=a["quantity"],medium_rider=a["medium"])
    except:
        return Response({"message":"data not valid"},status=500)
    data={"message":"request successfully added"}
    data['data']=a

    return Response(data)

#This view is for viewing request sent by a requester
@api_view(['GET'])
def asset_req_get(request,*args,**kwargs):
    try:
        a=json.loads(request.body)
        print(a)
        user=a['user']
    except:
        return Response({"message":"Invalid parameter"},status=500)

    data=asset_transport_request.objects.filter(user_req=user)
    try:
        data=data.filter(asset_type=a['asset_type'].upper())
    except:
        pass

    if not data:
        return Response({"message":"Either no request for this user or no request with this filter"},status=500)
    res={"message":"success","data":[]}
    res1=[]
    for x in data:
        b=model_to_dict(x)
        #print(str(b['date_time_req']).replace('+00:00',''))
        format="%Y-%m-%d %H:%M:%S"
        dt=datetime.datetime.strptime((str(b['date_time_req'])).replace('+00:00',''),format)
        if (dt-datetime.datetime.now()).total_seconds()<0 and b['status']==0:
            b['status']="Expired"
            print(dt-datetime.datetime.now())
            #print(b['date_time_req']-datetime.datetime.now())
            pass
        elif b['status']==0:
            b['status']="Pending"
        else:
            b['status']="Confirmed"
        try:
            if a['status'].lower()==b['status'].lower():
                res1.append(b)
        except:
            res1.append(b)
    if len(res1)==0:
        return Response({"message":"Either no request for this user or no request with this filter"},status=500)
    res1=sorted(res1, key=lambda i: i['date_time_req'])
    res['data']=res1
    return Response(res)


#This view is for  viewing match with rider
@api_view(['GET'])
def match(request,*args,**kwargs):
    try:
        a=json.loads(request.body)
        print(a)
        id_req=a['id']
    except:
        return Response({"message":"Invalid parameter"},status=500)
    try:
        page=a['page']
    except:
        page=0
    res={"message":"success","data":[]}
    res1=[]
    try:
        data=asset_transport_request.objects.get(id=id_req)
    except:
        return Response({"message":"No matching request"},status=500)

    data=model_to_dict(data)
    data=rider_request.objects.filter(from_rider=data['from_req'],to_rider=data['to_req'],date_time_rider=data['date_time_req'])[page*5:page*5+5]
    print(data)
    for x in data:
        b=model_to_dict(x)
        res1.append(b)
    if len(res1)==0:
        return Response({"message":"No matching request"},status=500)
    res['data']=res1
    return Response(res)

#this view is for selecting a rider out of match
@api_view(['POST'])
def rider_select(request,*args,**kwargs):
    try:
        a=json.loads(request.body)
        print(a)
        id_req=a['id']
        id_select=a['select_id']
    except:
        return Response({"message":"Invalid parameter"},status=500)
    try:
        data=asset_transport_request.objects.get(id=id_req)
    except:
        return Response({"message":"invalid id sent"},status=500)
    try:
        data1=rider_request.objects.get(id=id_select)
    except:
        return Response({"message":"invalid sender id sent"},status=500)
    data.status=id_select
    data.save()
    return Response({"message":"success","data":a})