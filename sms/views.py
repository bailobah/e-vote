from django.shortcuts import render

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string
from sms.forms import RejectedSmsForm
from api.models import RejectedSms



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

# def sms_mode_delete(request, pk):
#     sms = get_object_or_404(RejectedSms, pk=pk)
#     print(sms)
#     data = dict()
#     if request.method == 'POST':
#         sms.is_active = False
#         sms.save()
#         data['form_is_valid'] = True
#         sms = RejectedSms.objects.all().order_by('-id')
#         data['html_sms_list'] = render_to_string('sms/list.html', {
#             'sms': sms
#         })
#     else:
#         context = {'sms': sms}
#         data['html_form'] = render_to_string('sms/delete.html',
#             context,
#             request=request,
#         )
#     return JsonResponse(data)

