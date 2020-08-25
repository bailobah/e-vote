from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string
from election.forms import ElectionForm
from election.models import Election

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

    elections = Election.objects.all()
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