from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from polls.forms import CreatePollForm, ContactUsForm
from django.shortcuts import render_to_response
from registration.views import myAccount
import datetime

from django.core import serializers

from polls.models import Poll, Category, Choice, Comment, Vote, Like
import json


def home(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/home_page.html')
    context = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(template.render(context))

def polls(request):
    context = RequestContext(request)
    category_list = Category.objects.all()
    catlists = []
    plists = []
    for cat in category_list:
        polls_list = Poll.objects.filter(category=cat)
        for p in polls_list:
            numchoices = 0
            numcomments = 0
            numvotes = 0
            clist = Choice.objects.filter(poll=p)
            for c in clist:
                numchoices = numchoices + 1
                numvotes = numvotes+c.votes
                colist = Comment.objects.filter(choice = c)
                for co in colist:
                    numcomments = numcomments+1
            plists.append({'poll': p, 'numChoices': numchoices, 'numComments': numcomments, 'numVotes': numvotes})
        catlists.append({'category': cat, 'polls': plists})
    context_dict = {'categories': catlists}
    
    return render_to_response('polls/polls.html', context_dict, context)

# def category(request, category_id):
#     latest_category_list = Category.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/poll.html')
#     context = RequestContext(request, {
#                              'latest_category_list': latest_category_list,
#                              })
#     return HttpResponse(template.render(context))

def poll(request, category_id, poll_id):
    context = RequestContext(request)
    p = Poll.objects.filter(pk=poll_id)
    listL = Choice.objects.filter(poll = p)
    voted = 0
    if request.user.is_authenticated():
        v = Vote.objects.filter(poll=p, user=request.user)
        voted = False if len(v) == 0 else True
    else:
        voted = False
    choicelists = []
    for l in listL:
        commentlists = []
        listC = Comment.objects.filter(choice = l)
        for c in listC:
            likedByUser = 0
            if request.user.is_authenticated():
                li = Like.objects.filter(comment=c, user=request.user)
                likedByUser = 0 if len(li) == 0 else 1
            else:
                likedByUser = 0
            commentlists.append({'comment': c, 'likedByUser': likedByUser})
        votedFor = 1 if voted and v[0].choice == l else 0
        choicelists.append({'choice': l, 'comments': commentlists, 'votedFor': votedFor})
    votedInt = 1 if voted else 0
    context_dict = {'poll': p[0], 'choices': choicelists, 'voted': votedInt}

    # Render the response and send it back!
    return render_to_response('polls/poll.html', context_dict, context)

def get_poll_chart(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    clist = Choice.objects.filter(poll = p)
    choices = {'poll': serializers.serialize('json', [ p, ]), 'choices': []}
    for c in clist:
        choices['choices'].append(serializers.serialize('json', [ c, ]))
    return HttpResponse(json.dumps(choices), content_type="application/json")

def vote(request):
    c = Choice.objects.filter(pk=request.POST['cid'])
    c = c[0]
    c.votes = c.votes + 1
    c.save()
    p = Poll.objects.filter(pk=request.POST['qid'])
    p = p[0]
    v = Vote(poll=p, choice=c, user=request.user, pub_date=datetime.datetime.now())
    v.save()
    return HttpResponseRedirect("/"+str(p.category.id)+"/"+request.POST['qid']+"/")

def change_vote(request):
    c = Choice.objects.filter(pk=request.POST['cid'])
    c = c[0]
    p = Poll.objects.filter(pk=request.POST['qid'])
    p = p[0]
    v = Vote.objects.filter(poll=p, user=request.user)
    v = v[0]
    c2 = v.choice
    c2.votes = c2.votes - 1
    c2.save()
    c.votes = c.votes + 1
    c.save()
    v.choice = c
    v.save()
    clist = Comment.objects.filter(choice=c2, user=request.user)
    for co in clist:
        llist = Like.objects.filter(user=request.user, comment=co)
        for l in llist:
            l.delete()
        co.delete()
    
    return HttpResponseRedirect("/"+str(p.category.id)+"/"+request.POST['qid']+"/")

def writecomment(request):
    cp = request.POST['mycomment']
    p = Poll.objects.get(pk=request.POST['qid'])
    v = Vote.objects.filter(poll=p, user=request.user)
    v = v[0]
    c = Comment(comment_text=cp, choice=v.choice, user=request.user, pub_date=datetime.datetime.now())
    c.save()
    return HttpResponseRedirect("/"+str(p.category.id)+"/"+request.POST['qid']+"/")

def delete_comment(request, category_id, poll_id, comment_id):
    c = Comment.objects.get(pk=comment_id)
    c.delete()
    return HttpResponseRedirect("/"+category_id+'/'+poll_id+'/')

def like_comment(request, category_id, poll_id, comment_id):
    c = Comment.objects.get(pk=comment_id)
    c.likes = c.likes + 1;
    c.save()
    l = Like(user=request.user, comment=c, pub_date=datetime.datetime.now())
    l.save()
    return HttpResponseRedirect("/"+category_id+'/'+poll_id+'/')

def unlike_comment(request, category_id, poll_id, comment_id):
    c = Comment.objects.get(pk=comment_id)
    c.likes = c.likes - 1;
    c.save()
    l = Like.objects.get(comment=c)
    l.delete()
    return HttpResponseRedirect("/"+category_id+'/'+poll_id+'/')

def delete_poll(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    p.delete()
    return HttpResponseRedirect("/")

def about(request):
    template = loader.get_template('polls/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def freeze_voting(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    p.frozen = False if p.frozen else True
    p.save()
    return HttpResponseRedirect("/1/"+poll_id+"/")

def create_poll(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new poll to the database.
            p = form.save(request)
            

            # Now call the index() view.
            # The user will be shown the homepage
            
    # Render the response and send it back!
            return poll(request, p.category.id, p.id)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CreatePollForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('polls/create_poll.html', {'form': form}, context)

def get_all_categories(request):
    latest_category_list = Category.objects.order_by('category_text')[:5]

    serialized_obj = serializers.serialize('json', [ latest_category_list, ])

    return HttpResponse(serialized_obj, content_type="application/json")

def get_all_polls(request):
    latest_category_list = Category.objects.order_by('category_text')[:5]

    serialized_obj = serializers.serialize('json', [ latest_category_list, ])

    return HttpResponse(serialized_obj, content_type="application/json")

def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return HttpResponseRedirect("/")

    args = {}

    args['form'] = ContactUsForm()

    return render_to_response("contact_form/contact_form.html", args)
