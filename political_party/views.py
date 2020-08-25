from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string
from political_party.forms import PoliticalPartyForm
from political_party.models import PoliticalParty

def save_political_party_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            political_partys = PoliticalParty.objects.all()
            data['html_political_party_list'] = render_to_string('political_party/partial_political_party_list.html', {
                'political_partys': political_partys
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

def political_party_list(request):

    political_partys = PoliticalParty.objects.all()
    return render(request, 'political_party/ui-political_party.html', {'political_partys': political_partys})

def political_party_delete(request, pk):
    political_party = get_object_or_404(PoliticalParty, pk=pk)
    data = dict()
    if request.method == 'POST':
        political_party.delete()
        data['form_is_valid'] = True
        political_partys = PoliticalParty.objects.all()
        data['html_political_party_list'] = render_to_string('political_party/partial_political_party_list.html', {
            'political_partys': political_partys
        })
    else:
        context = {'political_party': political_party}
        data['html_form'] = render_to_string('political_party/partial_political_party_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def political_party_create(request):
    data = dict()

    if request.method == 'POST':
        form = PoliticalPartyForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = PoliticalPartyForm()

    context = {'form': form}
    data['html_form'] = render_to_string('political_party/partial_political_party_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

def political_party_update(request, pk):
    political_party = get_object_or_404(PoliticalParty, pk=pk)

    if request.method == 'POST':
        form = PoliticalPartyForm(request.POST, instance=political_party)
    else:
        form = PoliticalPartyForm(instance=political_party)
    return save_political_party_form(request, form, 'political_party/partial_political_party_update.html')