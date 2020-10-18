from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm, UserUpdateForm


# Create your views here.

#
#
@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
    else:
        form = UserUpdateForm(instance=user)
    return save_election_form(request, form, 'users/update.html')

