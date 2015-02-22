from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from polls.models import Poll, Category, Choice

def myAccount(request):
    context = RequestContext(request)
    polls_list = Poll.objects.filter(user=request.user)
    context_dict = {'polls': polls_list}

    # Render the response and send it back!
    return render_to_response('registration/dashboard.html', context_dict, context)