
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.db.models import Q
import re

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from api.models import GetMinuteSmsSerializer, MinuteSms, MinuteDetailsSms, RejectedSms
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
        polling = PollingStation.objects.filter(locality__in=localitys).filter(is_active=True)
        serializer = PollingStationSerializer(polling, many=True)
        return JsonResponse({'data': serializer.data, 'user': UserSerializer(request.user).data, 'political_party':PoliticalPartySerializer(PoliticalParty.objects.filter(is_active=True), many=True).data}, safe=False, status=status.HTTP_200_OK)

class PollingDetail(APIView):

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    model = Minute

    def post(self, request):

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
        polling = self.request.data['polling']
        if Minute.objects.filter(polling=polling).exists():
            return JsonResponse({'message':f'Le pv correspondant au bureau N° ({polling}) a déja été crée'}, status=status.HTTP_205_RESET_CONTENT)

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

    phone_number = phonenumbers.parse(request.GET.get("emetteur"), "GN")

    log.info(request)

    if request.GET.get("numero") == '33755532031' :
        sender_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ", "")
        delegate_phone = ''

        grammar = r"(?P<key>[A-Za-z]*).(?P<value>[0-9]+)"

        sms = { k: int(v) for k, v in re.findall(grammar, request.GET.get("message").lower().replace('x', '')) }

        log.info("The value of sms is %s", sms)

        if bool(sms) :

            message = ''
            try :
                numero_polling = sms.pop("bv", None)
                nbr_voters = sms.pop("votant")
                nbr_invalids_ballots = int(sms.pop("bn"))
            except KeyError:
                message += 'BV ou VOTANT ou BN sont abscents dans le message envoyé, '

            if nbr_voters - nbr_invalids_ballots !=  sum(sms.values()) :
                message += f'La somme des voies des partis ({sum(sms.values())}) est different du nombre de votants ({nbr_voters}), '

            if len(sms) != PoliticalParty.objects.filter(is_active=True).count() :
                message += f'Le nombre de partis fourni ({len(sms)}) est différent ({PoliticalParty.objects.filter(is_active=True).count()}), '

            election = get_object_or_404(Election, pk=1)

            if numero_polling != None :
                try:
                    polling = PollingStation.objects.filter(numero=int(numero_polling),is_active=True).first()
                    log.info("entry and locality existing")
                    log.info("The value of polling is %s", polling)

                    if polling == None :
                        message += f'Le pv associé a ce bureau de vote ({numero_polling}) est innexistant ou a déjà été traité, '

                    if not MinuteSms.objects.filter(polling=polling).exists() and polling != None and Allocation.objects.filter(locality_id=polling.locality_id).exists():
                        log.info("The value of locality_id is %s",  polling.locality_id)
                        allocation = Allocation.objects.filter(locality_id=polling.locality_id).first()

                        user = User.objects.filter(pk=allocation.user.id).first()
                        log.info("The value of user is %s", user)
                        delegate_phone = user.phone_number
                        if message != '' :
                            minute = MinuteSms.objects.create(election=election,
                                                          polling=polling,
                                                          user=user,
                                                          nbr_registrants=polling.nbr_registrants,
                                                          nbr_voters= nbr_voters,
                                                          nbr_invalids_ballots=nbr_invalids_ballots,
                                                          nbr_votes_cast= nbr_voters - nbr_invalids_ballots,
                                                          )
                            log.info("The value of minute is %s", minute)
                            for party, votes_obtained in sms.items():

                                try:
                                    political_party = PoliticalParty.objects.filter(name=party, is_active=True).first()
                                    if political_party != None :
                                        MinuteDetailsSms.objects.create(minute=minute, political_party=political_party, nbr_votes_obtained = votes_obtained)
                                    else :
                                        message += f'Le parti ({party.upper()}) est inconnu, '
                                        rej = RejectedSms.objects.create(sms=request.GET.get("message"),sender_phone=sender_phone,
                                                                        errorMessage=message, delegate_phone=delegate_phone, is_active=True)
                                        log.info("The value of rej is %s", rej)

                                except PoliticalParty.DoesNotExist :
                                    message += f', Le parti ({party.upper()}) est inconnu'
                                    rej = RejectedSms.objects.create(sms=request.GET.get("message"), sender_phone=sender_phone, errorMessage=message,
                                                                    delegate_phone=delegate_phone, is_active=True)
                                    log.info("The value of rej is %s", rej)
                        else :
                            rej = RejectedSms.objects.create(sms=request.GET.get("message"),sender_phone=sender_phone,errorMessage=message,delegate_phone = delegate_phone, is_active=True)
                            log.info("The value of rej is %s", rej)
                    else :
                        message += f'Le bureau de vote ({numero_polling}) a déjà été traité, '
                        rej = RejectedSms.objects.create(sms=request.GET.get("message"), sender_phone=sender_phone,errorMessage=message, delegate_phone=delegate_phone, is_active=True)
                        log.info("The value of rej is %s", rej)
                except PollingStation.DoesNotExist:
                    message  += f'Le bureau de vote ({numero_polling}) fourni est innexistant, '
                    rej = RejectedSms.objects.create(sms=request.GET.get("message"), sender_phone=sender_phone,errorMessage=message, delegate_phone=delegate_phone, is_active=True)
                    log.info("The value of rej is %s", rej)

            else :
                message += f'Le bureau de vote ({numero_polling}) fourni est innexistant, '
                rej = RejectedSms.objects.create(sms=request.GET.get("message"),
                                                sender_phone=sender_phone, errorMessage=message, delegate_phone=delegate_phone, is_active=True)
                log.info("The value of rej is %s", rej)
        else:
            message = f'Le format du message est invalid, '
            rej = RejectedSms.objects.create(sms=request.GET.get("message"),
                                             sender_phone=sender_phone, errorMessage=message, delegate_phone=delegate_phone, is_active=True)
            log.info("The value of rej is %s", rej)
            log.info("The value of sms is %s", request.GET.get("message"))

    return JsonResponse({'':''}, status=HTTP_200_OK)