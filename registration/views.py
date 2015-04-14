import datetime
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from polls.models import Poll, Category, Choice, Vote
from forms import UserProfileEditForm
from django.contrib.auth import login, authenticate
from registration.forms import UserProfilePicUploadForm, PollPortalUserCreationForm
from registration.models import UserProfile, User
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.platypus.flowables import Spacer
def myAccount(request):
    context = RequestContext(request)
    polls_list = Poll.objects.filter(user=request.user)
    votes_list = Vote.objects.filter(user=request.user, old=False)
    
    polls_voted_list = []
    for vote in votes_list:
        polls_voted_list.append(vote.poll)
    
    context_dict = {'polls': polls_list, 'polls_voted': polls_voted_list}
    # Render the response and send it back!
    return render_to_response('registration/dashboard.html', context_dict, context)

def public_profile(request, user_id):
    context = RequestContext(request)
    u = User.objects.get(pk=user_id)
    try: #try to get user profile
        prof = UserProfile.objects.get(user=u)
    except: # it didn't exist so create one
        prof = UserProfile(user=u)
        prof.save()

    context_dict = {'profile': prof}

    # Render the response and send it back!
    return render_to_response('registration/user_public.html', context_dict, context)

def public_profile_edit(request, user_id):
    # Get the context from the request.
    u = User.objects.get(pk=user_id)
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new poll to the database.
            prof = UserProfile.objects.get(user=request.user)
            try: #try to get user profile
                prof = UserProfile.objects.get(user=u)
                
            except: # it didn't exist so create one
                print "Here"
                prof = UserProfile(user=u)
            
            prof.aboutMe = request.POST['aboutMe']
            prof.interests = request.POST['interests']
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                prof.avatar = avatar

            prof.save()

            # Now call the index() view.
            # The user will be shown the homepage

    # Render the response and send it back!
            return HttpResponseRedirect('/user/'+ user_id)
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

def close_account(request, user_id):
    u = User.objects.get(pk=user_id)
    u.is_active = False
    u.save()
    logout(request)
    return HttpResponseRedirect("/")

    
def upload_pic(request):
    if request.method == 'POST':
        form = UserProfilePicUploadForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
            prof = UserProfile.objects.get(user=request.user)
            avatar = request.FILES['image']
            prof.avatar = avatar
            form.save()
            prof.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')

def view_pdf_report(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    response = HttpResponse(content_type='application/pdf')
    filename = 'report_' + poll_id + ".pdf"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    styleH2 = styles['Heading2']
    styleH4 = styles['Heading4']
    width, height = letter
    choices = Choice.objects.filter(poll=poll)
    # Create the PDF object, using the response object as its "file."
    c = canvas.Canvas(response)
    
    p = Paragraph('Poll Summary Report:', styleH)
    
    p.wrapOn(c, width, height)
    p.drawOn(c, 100, height - 50, mm)
    
    p = Paragraph('Owner: ' + poll.user.username, styleH4)
    
    p.wrapOn(c, width, height)
    p.drawOn(c, 100, height - 85, mm)
    
    p = Paragraph(poll.poll_text, styleH2)
    
    p.wrapOn(c, width, height)
    p.drawOn(c, 100, height - 75, mm)
    
    
    data = []
    labels = []
    v_t = 0
    for choice in choices:
        v_t += choice.votes
        data.append(choice.votes)
        labels.append(choice.choice_text)

    pie_chart = Drawing(200, 200)
    pc = Pie()
    pc.x = 0
    pc.y = 0
    pc.width = 200
    pc.height = 200
    pc.data = data
    pc.labels = labels
    
    rightMargin=inch/4
    leftMargin=inch/4
    topMargin=inch/2
    bottomMargin=inch/4

    pie_chart.add(pc)
    renderPDF.draw(pie_chart, c, 200, 475)
    
    dataT = [['Choice:', '# of votes:']]
    
    for choice in choices:
        dataT.append([choice.choice_text, choice.votes])
        
    t = Table(dataT, colWidths=200)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('ALIGN',(0,0),(-1,-1),'CENTER'),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                       ]))
    w, h = t.wrapOn(c, width, height)
    t.drawOn(c, 100, height - 400 - h, mm)
    
    footer = Paragraph(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), styleN)
    w, h = footer.wrap(width, bottomMargin)
    footer.drawOn(c, leftMargin, h)
    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()
    return response 