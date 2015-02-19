from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from polls.models import Question, Category, Choice

def myAccount(request):
    context = RequestContext(request)
    questionsList = Question.objects.filter(user=request.user)
    context_dict = {'questions': questionsList}

    # Render the response and send it back!
    return render_to_response('registration/dashboard.html', context_dict, context)