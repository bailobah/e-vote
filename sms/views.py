from django.shortcuts import render

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string
from sms.forms import RejectedSmsForm
from api.models import RejectedSms

def save_sms_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sms = PoliticalParty.objects.all().order_by('-id')
            data['html_sms_list'] = render_to_string('sms/list.html', {
                'sms': sms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

def sms_list(request):

    sms = RejectedSms.objects.all().order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(sms, 20)
    try:
        sms = paginator.page(page)
    except PageNotAnInteger:
        sms = paginator.page(1)
    except EmptyPage:
        sms = paginator.page(paginator.num_pages)

    return render(request, 'sms/ui-sms.html', {'sms': sms})

def sms_delete(request, pk):
    sms = get_object_or_404(RejectedSms, pk=pk)
    data = dict()
    if request.method == 'POST':
        sms.delete()
        data['form_is_valid'] = True
        sms = RejectedSms.objects.all().order_by('-id')
        data['html_sms_list'] = render_to_string('sms/list.html', {
            'sms': sms
        })
    else:
        context = {'sms': political_party}
        data['html_form'] = render_to_string('sms/delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def sms_create(request):
    data = dict()

    if request.method == 'POST':
        form = RejectedSmsForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = PoliticalPartyForm()

    context = {'form': form}
    data['html_form'] = render_to_string('sms/create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

def sms_update(request, pk):
    sms = get_object_or_404(RejectedSms, pk=pk)

    if request.method == 'POST':
        form = RejectedSmsForm(request.POST, instance=sms)
    else:
        form = RejectedSmsForm(instance=sms)
    return save_sms_form(request, form, 'sms/update.html')