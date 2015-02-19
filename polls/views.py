from django.http import HttpResponse
from django.template import RequestContext, loader
from polls.forms import CreateTopicForm
from django.shortcuts import render_to_response

from django.core import serializers

from polls.models import Question, Category, Choice
import json


def categories(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/categories.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))

def get_all_categories(request):
    latest_category_list = Category.objects.order_by('category_text')[:5]

    serialized_obj = serializers.serialize('json', [ latest_category_list, ])

    return HttpResponse(serialized_obj, content_type="application/json")

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
    context = RequestContext(request)
    q = Question.objects.filter(pk=question_id)
    listL = Choice.objects.filter(question = q)
    context_dict = {'question': q, 'choices': listL}

    # Render the response and send it back!
    return render_to_response('polls/question.html', context_dict, context)

def get_question_chart(request, question_id):
    q = Question.objects.get(pk=question_id)
    clist = Choice.objects.filter(question = q)
    choices = {'question': serializers.serialize('json', [ q, ]), 'choices': []}
    for c in clist:
        choices['choices'].append(serializers.serialize('json', [ c, ]))


    return HttpResponse(json.dumps(choices), content_type="application/json")

def delete_new(request, question_id):
    # does nothing right now
   print 'Herro Worrd!'

def about(request):
    template = loader.get_template('polls/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def freezeVoting(request, question_id):
    q = Question.objects.get(pk=question_id)
    if q.frozen:
        q.frozen = False
    else:
        q.frozen = True
    return myAccount(request);

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
