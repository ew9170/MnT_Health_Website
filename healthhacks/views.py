from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User, CalorieCalc, FitnessPlan
from forms.forms import EditProfileForm


# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required(login_url='/healthhacks/login')
def dashboard_view(request):
    user = list(User.objects.filter(username__exact=request.user.username))[0]

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'calorie_count': user.calorie_count,
        'fitness_plan': user.fitness_plan,
    }

    return render(request, 'dashboard.html', context=context)


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            User(username=data['username']).save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/healthhacks/login')
def edit_profile(request):
    user = list(User.objects.filter(username__exact=request.user.username))[0]

    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.save_base()
            return redirect('dashboard')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'edit_profile.html', context=context)