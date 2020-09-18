from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from locality_type.forms import LocalityTypeForm
from locality_type.models import LocalityType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string

name = 'locality_type'
def save_locality_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            data['html_list'] = render_to_string(f'{name}/list.html', {
                name + 's' : LocalityType.objects.all()
            })
        else:
            data['form_is_valid'] = False
    data['html_form'] = render_to_string(template_name, {'form': form}, request=request)
    return JsonResponse(data)

def locality_type_list(request):
    locality_list = LocalityType.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(locality_list, 20)
    try:
        locality_tpes = paginator.page(page)
    except PageNotAnInteger:
        locality_tpes = paginator.page(1)
    except EmptyPage:
        locality_tpes = paginator.page(paginator.num_pages)
    return render(request, f'{name}/ui-{name}.html', { name + 's' : locality_tpes})

def locality_type_delete(request, pk):
    locality_type = get_object_or_404(LocalityType, pk=pk)
    data = dict()
    if request.method == 'POST':
        locality_type.delete()
        data['form_is_valid'] = True

        data['html_list'] = render_to_string(f'{name}/list.html', {
            name + 's' : LocalityType.objects.all()
        })
    else:
        context = { name: locality_type}
        data['html_form'] = render_to_string(f'{name}/delete.html',
                                             context ,
                                             request=request,
)
    return JsonResponse(data)

def locality_type_create(request):
    data = dict()

    if request.method == 'POST':
        form = LocalityTypeForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = LocalityTypeForm()

    data['html_form'] = render_to_string(f'{name}/create.html',
                                         {'form': form},
                                         request=request
                                         )
    return JsonResponse(data)

def locality_type_update(request, pk):
    locality_type = get_object_or_404(LocalityType, pk=pk)

    if request.method == 'POST':
        form = LocalityTypeForm(request.POST, instance=locality_type)
    else:
        form = LocalityTypeForm(instance=locality_type)
    return save_locality_type_form(request, form, f'{name}/update.html')