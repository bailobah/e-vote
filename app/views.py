# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.db.models import Avg, Sum

from election.models import Minute


@login_required(login_url="/login/")
def index(request):
    nbr_registrants = Minute.objects.all().aggregate(Sum('nbr_registrants'))
    nbr_voters = Minute.objects.all().aggregate(Sum('nbr_voters'))
    nbr_invalids_ballots = Minute.objects.all().aggregate(Sum('nbr_invalids_ballots'))
    nbr_votes_cast = Minute.objects.all().aggregate(Sum('nbr_votes_cast'))

    context = {
        'nbr_registrants' : nbr_registrants,
        'nbr_voters' : nbr_voters,
        'nbr_invalids_ballots' : nbr_invalids_ballots,
        'nbr_votes_cast' : nbr_votes_cast
    }
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
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
