from django.http import HttpResponse
from django.template import RequestContext, loader

from polls.models import Question, Category

def categories(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/categories.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
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