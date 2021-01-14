from django.http import JsonResponse, HttpResponseForbidden
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm,UserUpdateForm, UserProfileForm,AddCode
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from ide.models import savecode
from datetime import date

RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '6f56cbccb8ada4be47e38ff056b33cdef265b838'

@csrf_exempt
def index(request):
	return render(request, 'index.html', {})



@login_required
def code_save(request):
    form = AddCode(request.POST or None)
    if form.is_valid():
        code = form.save(commit=False)
        code.user = request.user
        code.save()
        return render(request, 'index.html', {'code': code})

    context = {
        "form": form,
    }
    return render(request, 'code_save.html', context)

@login_required
def code(request):
    codes = savecode.objects.filter(user=request.user)
    return render(request, 'code.html', {'codes': codes})

def delete_code(request,code_id):
    codes = savecode.objects.filter(user=request.user)
    code = get_object_or_404(savecode, pk=code_id)
    code.delete()
    return render(request, 'code.html',{'codes':codes})


@csrf_exempt
def runCode(request):
	if request.is_ajax():
		source = request.POST['source']
		lang = request.POST['lang']
		data = {
			'client_secret': CLIENT_SECRET ,
			'async': 0,
			'source': source,
			'lang': lang,
			'time_limit': 5,
			'memory_limit': 262144,
		}
		if 'input' in request.POST:
			data['input'] = request.POST['input']
		r = requests.post(RUN_URL, data=data)
		return JsonResponse(r.json(), safe=False)

	else:
		return HttpResponseForbidden()


def Signup(request):
    form = UserForm(request.POST or None)
    profile_form = UserProfileForm(request.POST, request.FILES)
    
    if form.is_valid() and profile_form.is_valid():
        user = form.save(commit=False)
        profile = profile_form.save(commit= False)
        profile.user = user

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index.html')
    context = {
        "form": form,
        "profile_form":profile_form,
    }
    return render(request, 'signup.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'login.html' , context)


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    dob = user.userprofile.date_of_birth
    today = date.today()

    if ((today.month == dob.month) and (today.day == dob.day)):
        birthday = 'Wissing You a Very Very Happy Birthday.'
    else:
        birthday = ''

    return render(request, 'profile.html', {'user': user,'birthday':birthday ,'today':today})

@login_required
def edit_names(request):
    if request.method == "POST":
        form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance= request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_photo' in request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
            profile.save()
            url = reverse('ide:index')
            return HttpResponseRedirect(url)
        else:
            print(form.errors, profile_form.errors)
    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm( instance= request.user.userprofile)

    return render(request, "update_user.html",{"form":form, "profile_form":profile_form})


def PasswordChangeComplete(request):
    return render(request, 'commons/change_password_complete.html', {})