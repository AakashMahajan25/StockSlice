from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from PIL import Image
import io

def resizeImg(path,size):
    img = Image.open(path)
    width, height = img.size
    
    if width > 2 and height > 2:
        aspect_ratio = float(height) / float(width)
        if aspect_ratio != 1.0:
            # crop to square in the center
            if width > height:
                left = (width - height) / 2
                top = 0
                right = left + height
                bottom = height
            else:
                left = 0
                top = (height - width) / 2
                right = width
                bottom = top + width
            img = img.crop((left, top, right, bottom))
    
    if img.width > size:
        aspect_ratio = float(img.height) / float(img.width)
        height = int(size * aspect_ratio)
        img = img.resize((size, height), Image.ANTIALIAS)
    img.save(path)

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, 'Account not found')
            else:
                if user_obj.profile.is_email_verified:
                    user = authenticate(username=username, password=password)
                    if user:
                        auth_login(request, user)
                        return redirect('home')
                    else:
                        messages.error(request, 'Invalid credentials')
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, 'Please verify your email address')
        else:
           for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = LoginForm()

    context = {'form': form}

    return render(request , 'account/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            #checking
            user_obj = User.objects.filter(username = username)
            
            if user_obj.exists():
                messages.error(request, 'Username already taken')
            else:
                user_obj = User.objects.create(
                    first_name = first_name, last_name = last_name,
                    username = username, email = email
                )
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, 'Registration Successful! Please check your email for a verification link to activate your account.')
                return HttpResponseRedirect(request.path_info)

        else:
           for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegisterForm()

    context = {'form': form}

    return render(request , 'account/register.html', context)

def activate_email(request, token):
    try:
        user = Profile.objects.get(email_token = token)
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
            return render(request, 'account/activation.html')
        return HttpResponse('Account already verified')
        
    except Exception as e:
        print(e)
        return HttpResponse('Invalid Token')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = Profile.objects.get(user=request.user)
    orders = profile.order_set.all()

    WLCount= Wishlist.objects.filter(user=request.user).count()
    context = {'orders': orders,'WLCount':WLCount}
    return render(request, 'account/account.html', context)

@require_POST
def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.cleaned_data['profile_image']
            try:
                # Open the uploaded image using PIL
                image = Image.open(io.BytesIO(profile_image.read()))
                # Check that the image is not too large
                if image.width > 3000 or image.height > 3000:
                    raise ValueError('Image is too large')
                # Save the image to the profile
                profile = Profile.objects.get(user=request.user)
                profile.profile_image = profile_image
                profile.save()
                resizeImg(profile.profile_image.path,200)
                return JsonResponse('success', safe=False)
            except (OSError, ValueError) as e:
                return HttpResponseBadRequest('Not a valid image: ' + str(e))
        else:
            return HttpResponseBadRequest('Not a valid image')
    else:
        form = ProfileForm()
    return JsonResponse('success', safe=False)