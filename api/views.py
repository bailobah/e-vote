from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status, decorators
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from election.models import PollingStation, PollingStationSerializer, MinuteSerializer
from locality.models import Allocation
from users.models import UserSerializer

class PollingList(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        localitys = Allocation.objects.filter(user=request.user).values('locality_id')
        polling = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        serializer = PollingStationSerializer(polling, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data}, safe=False, status=status.HTTP_200_OK)

class PollingDetails(APIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = MinuteSerializer(data=request.data,context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({'message':'ok'}, status=status.HTTP_201_CREATED)
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