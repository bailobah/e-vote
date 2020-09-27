# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.db.models import Avg, Sum, F

from election.models import Minute, MinuteDetails, PollingStation
from locality.models import Allocation


@login_required(login_url="/login/")
def index(request):

    if request.user.is_superuser == True :

        nbr_registrants = Minute.objects.all().aggregate(Sum('nbr_registrants'))
        nbr_voters = Minute.objects.all().aggregate(Sum('nbr_voters'))
        nbr_invalids_ballots = Minute.objects.all().aggregate(Sum('nbr_invalids_ballots'))
        nbr_votes_cast = Minute.objects.all().aggregate(Sum('nbr_votes_cast'))
        votes_by_party = MinuteDetails.objects.all().annotate(name=F('political_party__name')).values('name').order_by(
            '-nbr_votes_obtained').annotate(nbr_votes_obtained=Sum('nbr_votes_obtained'))
        nbr_pvs_collected = Minute.objects.count()

    elif request.user.is_staff == True :

        nbr_registrants = Minute.objects.filter(user=request.user).aggregate(Sum('nbr_registrants'))
        nbr_voters = Minute.objects.filter(user=request.user).aggregate(Sum('nbr_voters'))
        nbr_invalids_ballots = Minute.objects.filter(user=request.user).aggregate(Sum('nbr_invalids_ballots'))
        nbr_votes_cast = Minute.objects.filter(user=request.user).aggregate(Sum('nbr_votes_cast'))
        minutes = Minute.objects.filter(user=request.user).values('id')
        votes_by_party = MinuteDetails.objects.filter(minute__in=minutes).annotate(name=F('political_party__name')).values(
            'name').order_by('-nbr_votes_obtained').annotate(nbr_votes_obtained=Sum('nbr_votes_obtained'))
        nbr_pvs_collected = Minute.objects.filter(user=request.user).count()

    elif request.user.is_superviser == True :
        locality_ids = Allocation.objects.filter(user=request.user).values('locality_id')
        polling_station_ids = PollingStation.objects.filter(locality__in=locality_ids).filter(is_active=False).values('id')
        nbr_registrants = Minute.objects.filter(polling__in=polling_station_ids).aggregate(Sum('nbr_registrants'))
        nbr_voters = Minute.objects.filter(polling__in=polling_station_ids).aggregate(Sum('nbr_voters'))
        nbr_invalids_ballots = Minute.objects.filter(polling__in=polling_station_ids).aggregate(Sum('nbr_invalids_ballots'))
        nbr_votes_cast = Minute.objects.filter(polling__in=polling_station_ids).aggregate(Sum('nbr_votes_cast'))
        minutes = Minute.objects.filter(polling__in=polling_station_ids).values('id')
        votes_by_party = MinuteDetails.objects.filter(minute__in=minutes).annotate(name=F('political_party__name')).values(
            'name').order_by('-nbr_votes_obtained').annotate(nbr_votes_obtained=Sum('nbr_votes_obtained'))
        nbr_pvs_collected = Minute.objects.filter(polling__in=polling_station_ids).count()
    else:
        nbr_registrants = None
        nbr_voters = None
        nbr_invalids_ballots = None
        nbr_votes_cast = None
        votes_by_party = None
        nbr_pvs_collected = None
    context = {
        'nbr_registrants' : nbr_registrants,
        'nbr_voters' : nbr_voters,
        'nbr_invalids_ballots' : nbr_invalids_ballots,
        'nbr_votes_cast' : nbr_votes_cast,
        'votes_by_party': votes_by_party,
        'nbr_pvs_collected':nbr_pvs_collected
    }
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

