
from django.contrib.auth import authenticate
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from api.models import GetMinuteSmsSerializer, MinuteSms, MinuteDetailsSms
from election.models import PollingStation, PollingStationSerializer, MinuteSerializer, Minute, GetMinuteSerializer, \
    Election
from locality.models import Allocation
from political_party.models import PoliticalPartySerializer, PoliticalParty
from users.models import UserSerializer, User
import phonenumbers
import logging
log = logging.getLogger('django')

class PollingList(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        localitys = Allocation.objects.filter(user=request.user).values('locality_id')
        polling = PollingStation.objects.filter(locality__in=localitys)#.filter(is_active=True)
        serializer = PollingStationSerializer(polling, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data, 'political_party':PoliticalPartySerializer(PoliticalParty.objects.filter(is_active=True), many=True).data}, safe=False, status=status.HTTP_200_OK)

class PollingDetail(APIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    model = Minute

    def get(self, request):

        minute = MinuteSms.objects.filter(polling=self.request.data['polling'])

        serializer = GetMinuteSmsSerializer(instance=minute, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data}, safe=False, status=status.HTTP_200_OK)


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
        minute = Minute.objects.filter(user=request.user)
        serializer = GetMinuteSerializer(instance=minute, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data}, safe=False, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):

        minute = Minute.objects.get(pk=pk )
        serializer = GetMinuteSerializer(instance=minute, data=request.data,many=True)
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

    phone_number = phonenumbers.parse(request.GET.get("emetteur"), "FR")

    try:
        user = User.objects.get(phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", ""))
    except User.DoesNotExist:
        return None

    sms = {k.lower(): v for k, v in (x.split(':') for x in request.GET.get("message").split(",")) }
    numero_polling = sms.pop("bv", None)
    nbr_voters = sms.pop("votant", None)
    nbr_invalids_ballots = sms.pop("bn", None)
    election = get_object_or_404(Election, pk=1)

    if numero_polling != None :
        try:
            polling = PollingStation.objects.filter(numero=numero_polling).first()

            minute = MinuteSms.objects.create(election=election,
                                          polling=polling,
                                          user=user,
                                          nbr_registrants=polling.nbr_registrants,
                                          nbr_voters= nbr_voters,
                                          nbr_invalids_ballots=nbr_invalids_ballots,
                                          nbr_votes_cast= int(nbr_voters) - int(nbr_invalids_ballots),
                                          )

            for party, votes_obtained in sms.items():
                print(party)
                print(votes_obtained)
                try:
                    political_party = PoliticalParty.objects.filter(name=party).first()
                    if political_party != None :
                        print(political_party.id)
                        minute_detail =MinuteDetailsSms.objects.create(minute=minute,
                                                                       political_party=political_party,
                                                                       nbr_votes_obtained=votes_obtained)
                except PoliticalParty.DoesNotExist :
                    None
        except PollingStation.DoesNotExist:
            None

    return JsonResponse({'':''}, status=HTTP_200_OK)