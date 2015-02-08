from django.http import HttpResponse
from django.template import RequestContext, loader
from contact_us_frm import ContactUsForm
from django.shortcuts import render
from django.http import HttpResponseRedirect

from polls.models import Question, Category

import json

def categories(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/categories.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))

def get_all_categories(request):
    latest_category_list = [{'name': 'Politics'}, {'name': 'Fashion'}, {'name': 'Science'}, {'name': 'Technology'}]
    items = {}
    items['items'] = latest_category_list
    return HttpResponse(json.dumps(items), content_type="application/json")
    
    

def topic_select(request):
    latest_category_list = Category.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/questions.html')
    context = RequestContext(request, {
        'latest_category_list': latest_category_list,
    })
    return HttpResponse(template.render(context))


def questions(request, category_id):
    latest_category_list = Category.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/questions.html')
    context = RequestContext(request, {
                             'latest_category_list': latest_category_list,
                             })
    return HttpResponse(template.render(context))

def question(request, category_id, question_id):
    latest_topic_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/question.html')
    context = RequestContext(request, {
                             'latest_question_list': latest_topic_list,
                             })
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('polls/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def contactUs(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactUsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactUsForm()

    return render(request, 'contactus.html', {'form': form})
