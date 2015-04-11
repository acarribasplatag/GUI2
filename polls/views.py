from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from polls.forms import CreatePollForm, ContactUsForm
from django.shortcuts import render_to_response
from registration.views import myAccount
from registration.models import UserProfile
import datetime
import time

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from polls.models import Poll, Category, Choice, Comment, Vote, Like, NegativeVote
import json


def home(request):
    template = loader.get_template('polls/home_page.html')

    context = RequestContext(request)
    category_list = Category.objects.all()

    context = RequestContext(request, {
        'categories': category_list,
    })
    return HttpResponse(template.render(context))

def sheet(request):
    template = loader.get_template('polls/bottom-sheet-grid-template.html')

    context = RequestContext(request)
    
    return HttpResponse(template.render(context))

def polls(request):
    context = RequestContext(request)
    category_list = Category.objects.all()
    catlists = []
    plists = []
    recent_list = []
    popular_list = []


    # Make  a list that contains polls, along with their choices, votes, and comments
    for cat in category_list:
        polls_list = Poll.objects.filter(category=cat)
        for p in polls_list:
            numchoices = 0
            numcomments = 0
            numvotes = 0
            choice_list = Choice.objects.filter(poll=p)
            for c in choice_list:
                numchoices = numchoices + 1
                numvotes = numvotes+c.votes
                colist = Comment.objects.filter(choice = c)
                for co in colist:
                    numcomments = numcomments+1
            plists.append({'poll': p, 'numChoices': numchoices, 'numComments': numcomments, 'numVotes': numvotes})
        catlists.append({'category': cat, 'polls': plists})

    # Make a list of all the polls by date they were created.
    polls_list = Poll.objects.order_by('-pub_date')
    for p in polls_list:
        category = Category.objects.get(poll=p)
        numchoices = 0
        numcomments = 0
        numvotes = 0
        choice_list = Choice.objects.filter(poll=p)
        for c in choice_list:
            numchoices = numchoices + 1
            numvotes = numvotes+c.votes
            colist = Comment.objects.filter(choice = c)
            for co in colist:
                numcomments = numcomments+1
        recent_list.append({'poll': p, 'numChoices': numchoices, 'numComments': numcomments,
         'numVotes': numvotes, 'categoryID': category.id})

    # Make a list of the most popular polls.
    polls_list = sorted(Poll.objects.all(), key = getTotalVotes, reverse=True)
    for p in polls_list:
        category = Category.objects.get(poll=p)
        numchoices = 0
        numcomments = 0
        numvotes = 0
        choice_list = Choice.objects.filter(poll=p)
        for c in choice_list:
            numchoices = numchoices + 1
            numvotes = numvotes+c.votes
            colist = Comment.objects.filter(choice = c)
            for co in colist:
                numcomments = numcomments+1
        popular_list.append({'poll': p, 'numChoices': numchoices, 'numComments': numcomments,
         'numVotes': numvotes, 'categoryID': category.id })

    context_dict = {'categories': catlists, 'recent':recent_list, 'popular':popular_list}
    return render_to_response('polls/polls.html', context_dict, context)

def getTotalVotes(p):
    choice_list = Choice.objects.filter(poll=p)
    numvotes = 0
    for c in choice_list:
        numvotes += c.votes
    return numvotes


def poll(request, category_id, poll_id):
    context = RequestContext(request)
    p = Poll.objects.filter(pk=poll_id)
    p = p[0]
    print p
    listL = Choice.objects.filter(poll = p)
    voted = 0
    if request.user.is_authenticated():
        v = Vote.objects.filter(poll=p, user=request.user)
        voted = False if len(v) == 0 else True
        for v_i in v:
            voted = False if v_i.old else True
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
            prof = UserProfile.objects.get(user=c.user)
            commentlists.append({'comment': c, 'likedByUser': likedByUser, 'userProfile': prof})
        votedFor = 1 if voted else 0
        if request.user.is_authenticated():
            for v_i in v:
                votedFor = 1 if voted and v_i.choice == l and not v_i.old else 0
        
        choicelists.append({'choice': l, 'comments': commentlists, 'votedFor': votedFor})
    votedInt = 1 if voted else 0
    context_dict = {'poll': p, 'choices': choicelists, 'voted': votedInt}

    # Render the response and send it back!
    return render_to_response('polls/poll.html', context_dict, context)

def get_poll_chart(request, poll_id):
    p = Poll.objects.get(pk=poll_id)
    clist = Choice.objects.filter(poll = p)
    choices = {'poll': serializers.serialize('json', [ p, ]), 'choices': []}
    for c in clist:
        choices['choices'].append(serializers.serialize('json', [ c, ]))
    return HttpResponse(json.dumps(choices), content_type="application/json")

def get_poll_timeline(request, poll_id):
    # Get Poll and Choices for poll
    p = Poll.objects.get(pk=poll_id)
    clist = Choice.objects.filter(poll = p)

    # Get a list of all the dates of all the votes
    date_list = Vote.objects.filter(poll=p).datetimes('pub_date', 'day')
    date_list2 = []
    for date in date_list:
        date2 = date.date()
        date_list2.append(date2)
    votes = {'votes': []}
    start_date = date_list2[0]
    end_date = datetime.date.today()

    num_days = (end_date+ datetime.timedelta(days=1) - start_date).days

    dates = []
    raw_dates = []
    for i in range(0, num_days):
        nd = start_date+datetime.timedelta(days=i)
        raw_dates.append(nd)
        d = time.mktime(nd.timetuple())
        dates.append(d)
    for c in clist:
        count_list = []
        for date in date_list2:
            tomorrow = date + datetime.timedelta( days=1 )
            vote_list = Vote.objects.filter(poll=p, choice=c, pub_date__range=(start_date, tomorrow), old=False)
            neg_vote_list = NegativeVote.objects.filter(poll=p, choice=c, pub_date__range=(start_date, tomorrow))
            total_choice = 0
            total_neg = 0
            total_choice = len(vote_list)
            total_neg = len(neg_vote_list)
            count_list.append([time.mktime(date.timetuple()), total_choice - total_neg])
        v_json = {'choice': serializers.serialize('json', [ c, ]),'count_list': count_list}
        votes['votes'].append(v_json)
    return HttpResponse(json.dumps(votes, cls=DjangoJSONEncoder), content_type="application/json")

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
    v = Vote.objects.filter(poll=p, user=request.user, old=False)
    v = v[0]
    c2 = v.choice
    if c.id == c2.id:
        return HttpResponseRedirect("/"+str(p.category.id)+"/"+request.POST['qid']+"/")
    v.old = True
    c2.votes = c2.votes - 1
    c2.save()
    c.votes = c.votes + 1
    c.save()
    v.save()
    v = Vote(poll=p, choice=c, user=request.user, pub_date=datetime.datetime.now())
    v.save()
    v2  = NegativeVote(poll=p, choice=c, user=request.user, pub_date=datetime.datetime.now())
    v2.save()
    clist = Comment.objects.filter(choice=c2, user=request.user)
    for co in clist:
        llist = Like.objects.filter(user=request.user, comment=co)
        for l in llist:
            l.delete()
        co.delete()

    return HttpResponseRedirect("/"+str(p.category.id)+"/"+request.POST['qid']+"/")

def delete_vote(request):
    c = Choice.objects.filter(pk=request.POST['cid'])
    c = c[0]
    p = Poll.objects.filter(pk=request.POST['qid'])
    p = p[0]
    v = Vote.objects.filter(poll=p, user=request.user, old=False)
    v = v[0]
    c.votes = c.votes - 1
    c.save()

    v.old = True
    v.save()

    v2  = NegativeVote(poll=p, choice=c, user=request.user, pub_date=datetime.datetime.now())
    v2.save()

    clist = Comment.objects.filter(choice=c, user=request.user)
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

def delete_poll(request, category_id, poll_id):
    p = Poll.objects.get(pk=poll_id)
    p.delete()
    return HttpResponseRedirect("/")

def about(request):
    template = loader.get_template('polls/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def freeze_voting(request, category_id, poll_id):
    p = Poll.objects.get(pk=poll_id)
    p.frozen = False if p.frozen else True
    p.save()
    return HttpResponseRedirect("/"+category_id+ "/"+poll_id+"/")

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
            return HttpResponseRedirect("/"+ str(p.category_id) + "/"+ str(p.id) +"/")
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
            form.save()

            return HttpResponseRedirect("/")
        else:
            print "invalid contact_us form"
            print form.errors

    args = {}

    args['form'] = ContactUsForm()

    return render_to_response("contact_form/contact_form.html", args, RequestContext(request))


