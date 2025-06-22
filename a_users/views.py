from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from a_users.models import Profile

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'a_users/profile.html', {'profile':profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)  
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False
      
    return render(request, 'a_users/profile_edit.html', { 'form':form, 'onboarding':onboarding })


@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            send_email_confirmation(request, request.user)
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
        
    return redirect('home')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'a_users/profile_delete.html')

from a_rtchat.models import ChatGroup

@login_required
def welcome_page(request):
    user = request.user
    user_groups = list(user.chat_groups.filter(is_private=False))
    try:
        public_chat = ChatGroup.objects.get(group_name='public-chat')
        if public_chat not in user_groups:
            user_groups = [public_chat] + user_groups
    except ChatGroup.DoesNotExist:
        pass
    user_private_chats = user.chat_groups.filter(is_private=True)
    return render(request, 'a_users/welcome_page.html', {
        'user': user,
        'user_groups': user_groups,
        'user_private_chats': user_private_chats,
    })

@login_required
def user_list_view(request):
    current_profile = request.user.profile
    users = User.objects.exclude(id=request.user.id).filter(
        profile__isnull=False,
        profile__department=current_profile.department,
        profile__batch=current_profile.batch
    ).select_related('profile')
    online_users = []  # Placeholder, update with your online user logic if needed
    return render(request, 'a_users/user_list.html', {
        'users': users,
        'online_users': online_users,
    })