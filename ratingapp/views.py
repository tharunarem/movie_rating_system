from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail,EmailMessage
from .models import *
from .forms import *
from movieratingsystem import settings
from .tokens import *
from django.http import HttpResponse

def movie_list(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'ratingpages/movie_list.html', {'movies': movies, 'query': query})

@login_required
def rate_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.user = request.user
            rating.save()
            return redirect('movie_list')
    else:
        form = RatingForm()
    return render(request, 'ratingpages/rate_movie.html', {'form': form, 'movie': movie})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            myuser = form.save(commit=False)
            myuser.is_active = False 
            myuser.save()

            current_site = get_current_site(request)
            email_subject = 'Confirm Your Email'
            message = render_to_string('email_verification.html', {
                'name': myuser.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })

            # Send email
            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = False  
            email.send()
            print("Email sent successfully, now redirecting to login page...")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('movie_list')
    else:
        return render(request,'email_verify_failed.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('movie_list')



def dummy_date_insert(request):
    name=input('enter name')
    age=int(input('enter age'))
    dobj=Dummy.objects.get_or_create(dummyname=name,age=age)
    if dobj[1]:
        return HttpResponse('user is created')
    else:
        return HttpResponse('user is not created')
