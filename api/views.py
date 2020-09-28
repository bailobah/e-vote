import requests
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView

from election.models import PollingStation, PollingStationSerializer, MinuteSerializer, Minute, GetMinuteSerializer
from locality.models import Allocation
from political_party.models import PoliticalPartySerializer, PoliticalParty
from users.models import UserSerializer
import logging
log = logging.getLogger(__name__)

class PollingList(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        localitys = Allocation.objects.filter(user=request.user).values('locality_id')
        polling = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        serializer = PollingStationSerializer(polling, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data, 'political_party':PoliticalPartySerializer(PoliticalParty.objects.filter(is_active=True), many=True).data}, safe=False, status=status.HTTP_200_OK)

class PollingDetails(APIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    model = Minute

    def post(self, request):
        self.request.POST._mutable = True
        self.request.data['user'] = self.request.user.id
        serializer = MinuteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({'message':'ok'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        """List Transactions"""
        minute = Minute.objects.all()
        serializer = GetMinuteSerializer(instance=minute, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):

        minute = get_object_or_404(Minute, pk=pk )
        serializer = MinuteSerializer(instance=minute, data=request.data,many=True)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            #validated_data = dict(list(serializer.validated_data.items()))
            serializer.save()
            JsonResponse({'message':'ok'}, safe=False, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return JsonResponse({'error': 'Please provide both username and password'},
                                status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'error': 'Invalid Credentials'},
                                status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key},
                            status=HTTP_200_OK)


def inbound_sms(request):
    log.debug('==========================')
    data = json.loads(request.body)
    print(data['emetteur'])

    return JsonResponse({'':''},status=HTTP_200_OK)