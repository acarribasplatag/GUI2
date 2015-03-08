from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from polls.models import Poll, Category, Choice
from forms import UserProfileEditForm
from django.contrib.auth import login, authenticate
from registration.forms import UserProfilePicUploadForm, PollPortalUserCreationForm
from registration.models import UserProfile, User
def myAccount(request):
    context = RequestContext(request)
    polls_list = Poll.objects.filter(user=request.user)
    context_dict = {'polls': polls_list}

    # Render the response and send it back!
    return render_to_response('registration/dashboard.html', context_dict, context)

def public_profile(request, user_id):
    context = RequestContext(request)
    u = User.objects.get(pk=user_id)
    prof = UserProfile.objects.get(user=u)
    context_dict = {'profile': prof}

    # Render the response and send it back!
    return render_to_response('registration/user_public.html', context_dict, context)

def public_profile_edit(request, user_id):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new poll to the database.
            form.save(request)
            

            # Now call the index() view.
            # The user will be shown the homepage
            
    # Render the response and send it back!
            return public_profile(request, user_id)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = UserProfileEditForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('registration/user_profile_edit.html', {'form': form}, context)

def register_user(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        form = PollPortalUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            print form.errors
    else:
        form = PollPortalUserCreationForm()

    return render_to_response("registration/register.html", {'form': form}, context)
    
def upload_pic(request):
    if request.method == 'POST':
        form = UserProfilePicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')
