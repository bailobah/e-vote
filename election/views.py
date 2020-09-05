from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from election.forms import ElectionForm, MinuteForm, MinuteFormFilterForm, MinuteUpdateForm
from election.models import Election, Minute


def save_election_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            elections = Election.objects.all()
            data['html_election_list'] = render_to_string('election/partial_election_list.html', {
                'elections': elections
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

def election_list(request):

    election_list = Election.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(election_list, 20)
    try:
        elections = paginator.page(page)
    except PageNotAnInteger:
        elections = paginator.page(1)
    except EmptyPage:
        elections = paginator.page(paginator.num_pages)
    return render(request, 'election/ui-election.html', {'elections': elections})

def election_delete(request, pk):
    election = get_object_or_404(Election, pk=pk)
    data = dict()
    if request.method == 'POST':
        election.delete()
        data['form_is_valid'] = True
        elections = Election.objects.all()
        data['html_election_list'] = render_to_string('election/partial_election_list.html', {
            'elections': elections
        })
    else:
        context = {'election': election}
        data['html_form'] = render_to_string('election/partial_election_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

def election_create(request):
    data = dict()

    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ElectionForm()

    context = {'form': form}
    data['html_form'] = render_to_string('election/partial_election_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

def election_update(request, pk):
    election = get_object_or_404(Election, pk=pk)

    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
    else:
        form = ElectionForm(instance=election)
    return save_election_form(request, form, 'election/partial_election_update.html')

def minute_list(request):

    data_list = Minute.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data_list, 20)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return render(request, 'minute/ui-minute.html', {'data': data})

def minute_delete(request, pk):

    minute = get_object_or_404(Minute, pk=pk)
    data = dict()
    if request.method == 'POST':
        minute.delete()
        data['form_is_valid'] = True

        data['html_list'] = render_to_string('minute/list.html', {
            'minutes' : Minute.objects.all()
        })
    else:
        context = { 'minute': minute}
        data['html_form'] = render_to_string('minute/delete.html',
                                             context ,
                                             request=request,)
    return JsonResponse(data)

def minute_create(request):
    data = dict()

    if request.method == 'POST':

        form = MinuteForm(request.POST, request.FILES)

        if form.is_valid():
            pv = form.save(commit=False)
            pv.user = request.user
            pv.election_id = 1
            pv.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = MinuteFormFilterForm(request.user)

    data['html_form'] = render_to_string('minute/create.html',
                                         {'form': form},
                                         request=request
                                         )
    return JsonResponse(data)

def save_minute_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            data['html_list'] = render_to_string('minute/list.html', {
                'minutes': Minute.objects.all()
            })
        else:
            data['form_is_valid'] = False
    data['html_form'] = render_to_string(template_name, {'form': form}, request=request)
    return JsonResponse(data)

def minute_update(request, pk):
    data = get_object_or_404(Minute, pk=pk)

    if request.method == 'POST':
        form = MinuteUpdateForm(request.POST, instance=data)
    else:
        form = MinuteUpdateForm(instance=data)
    return save_minute_form(request, form, 'minute/update.html')