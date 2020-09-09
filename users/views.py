from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from .forms import ProfileUpdateForm, UserUpdateForm


# Create your views here.

#
#
# @login_required
# def update_profile(request):
#     print(request)
#     if request.method == 'POST':
#         user = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if user.is_valid() and p_form.is_valid():
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#
#             user.save()
#             p = p_form.save()
#             messages.success(request, f'Your account has been updated')
#             print("=============================")
#             print(p.city)
#         #return redirect('index.html')
#     else:
#         print("=============================2")
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     return render(request, "profile.html", {
#         'user': user,
#         'profile': p_form
#     })

