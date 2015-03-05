from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from polls.models import Poll, Category, Choice
from forms import PollPortalUserCreationForm
from django.contrib.auth import login, authenticate

def myAccount(request):
    context = RequestContext(request)
    polls_list = Poll.objects.filter(user=request.user)
    context_dict = {'polls': polls_list}

    # Render the response and send it back!
    return render_to_response('registration/dashboard.html', context_dict, context)

def register_user(request):
	if request.method == 'POST':
		form = PollPortalUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password2')
			user = authenticate(username=username, password=password)
			login(request, user)
  			return HttpResponseRedirect("/")

	args = {}
	args.update(csrf(request))

	args['form'] = PollPortalUserCreationForm()

	return render_to_response("registration/register.html", args)