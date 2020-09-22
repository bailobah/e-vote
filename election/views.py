from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from election.forms import ElectionForm, MinuteForm, MinuteUpdateForm, MinuteDetailsFormset
from election.models import Election, Minute, PollingStation, MinuteDetails
from political_party.models import PoliticalParty


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


# def minute_create(request):
#     data = dict()
#     if request.method == 'POST':
#         form = MinuteDetailsFormset(request.POST, request.FILES)
#         details_instances = MinuteDetailsFormset(request.POST)
#
#         if form.is_valid():
#             pv = form.save(commit=False)
#             pv.user = request.user
#             pv.election_id = 1
#             pv.save()
#             station = PollingStation.objects.get(id=pv.polling_id)
#             station.is_active = False
#             station.save()
#             data['form_is_valid'] = True
#         else:
#             data['form_is_valid'] = False
#     else:
#         form = MinuteDetailsFormset(user= request.user)
#
#     data['html_form'] = render_to_string('minute/create.html',
#                                          {'form': form},
#                                          request=request
#                                          )
#     return JsonResponse(data)

def save_minute_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            minutes = Minute.objects.all()
            data['html_list'] = render_to_string('minute/list.html', {
                'minutes': minutes
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

def minute_detail(request, pk):
    minute = get_object_or_404(Minute, pk=pk)
    minute_details = MinuteDetails.objects.filter(minute_id=pk).all()
    return render(request,'minute/minute_detail_view.html',
                  {'minute' : minute, 'minute_details': minute_details})

def load_cities(request):

    political_partis = PoliticalParty.objects.all.order_by('name')
    return render(request, 'minute/political_dropdown_list_options.html', {'political_partis': political_partis})


class MinuteCreate(CreateView):
    model = Minute
    template_name = 'minute/create.html'
    form_class = MinuteForm
    success_url = 'None'

    def get_form_kwargs(self):
        kwargs = super(MinuteCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        self.initial.update({'user': self.request.user})
        return self.initial

    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        minute_details = MinuteDetailsFormset()
        form.fields['election'].initial =  get_object_or_404(Election, pk=1)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  minute_details=minute_details))

    def post(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        minute_details = MinuteDetailsFormset(self.request.POST, self.request.FILES)

        if (form.is_valid() and minute_details.is_valid()):
            return self.form_valid(form, minute_details)
        else:
            return self.form_invalid(form, minute_details)

    def form_valid(self, form, minute_details):

        print(minute_details)
        self.object = form.save(commit=False)
        self.object.nbr_votes_cast = self.object.nbr_voters - self.object.nbr_invalids_ballots
        self.object.save()

        minute_details_table = minute_details.save(commit=False)
        for td in minute_details_table:
            td.minute = self.object
            td.save()

        ps = PollingStation.objects.get(id=self.object.polling_id)
        ps.is_active = False
        ps.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, minute_details):
        print("invalid")
        return self.render_to_response(
            self.get_context_data(form=form,
                                  minute_details=minute_details
                                  )
        )
    def get_success_url(self):
        return reverse_lazy('minute_detail', kwargs={'pk': self.object.pk})

class MinuteUpdate(UpdateView):

    model = Minute
    template_name = 'minute/create.html'
    #template_name = 'minute/minute_detail_edit.html'
    form_class = MinuteUpdateForm
    success_url = 'None'

    # def get_form_kwargs(self):
    #     kwargs = super(MinuteUpdate, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank version of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Get detail attention
        minute_details = MinuteDetailsFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  minute_details=minute_details))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and them checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        minute_details = MinuteDetailsFormset(self.request.POST,instance=self.object)
        if (form.is_valid() and minute_details.is_valid()):
            return self.form_valid(form, minute_details)
        else:
            return self.form_invalid(form, minute_details)

    def form_valid(self, form, minute_details):

        self.object = form.save(commit=False)
        self.object.save()

        minute_details_table = minute_details.save(commit=False)
        for td in minute_details_table:
            td.minute = self.object
            td.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, minute_details):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  minute_details=minute_details
                                  )
        )
    def get_success_url(self):
        return reverse_lazy('minute_detail', kwargs={'pk': self.object.pk})