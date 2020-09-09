from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from election.models import PollingStation, PollingStationSerializer
from locality.models import Allocation
from users.models import UserSerializer


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_data(request):

    localitys = Allocation.objects.filter(user=request.user).values('locality_id')
    polling = PollingStation.objects.filter(locality__in=localitys)#.filter(is_active=True)
    serializer = PollingStationSerializer(polling, many=True)
    return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data}, safe=False, status=status.HTTP_200_OK)


