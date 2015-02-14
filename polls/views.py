from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from polls.forms import CreateTopicForm
from django.shortcuts import render_to_response

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
    latest_category_list = Category.objects.order_by('-pub_date')
    items = []
    items2 = {}
    for bar in latest_category_list:
        items.append({'name': bar['category_text']},)
    items2['items'] = items
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

def myAccount(request):
    template = loader.get_template('polls/dashboard.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def createTopic(request):
    template = loader.get_template('polls/create_topic_form.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def create_topic(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new topic to the database.
            form.save(request)

            # Now call the index() view.
            # The user will be shown the homepage.
            return myAccount(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CreateTopicForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('polls/create_topic_form.html', {'form': form}, context)
