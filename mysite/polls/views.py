from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
import random
import string
#from django.core.mail import send_mail
#from django.conf import settings

from .models import Question
from .models import Choice

import sqlite3

con = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = con.cursor()



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        un = request.user.username
        print(un)
        context = {'latest_question_list': latest_question_list, 'username': un}
        return render(request, 'polls/index.html', context)
    else:
        return redirect('/polls/login')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            question = get_object_or_404(Question, pk=question_id)
            for x in cur.execute("SELECT * FROM sqlite_sequence").fetchall():
                print(x)
            sql = 'INSERT INTO polls_choice (question_id, user_id, votes, choice_text) VALUES ('+str(question_id)+','+str(request.user.id)+','+'0'+',"'+request.GET.get('answer')+'")'
            newChoice = cur.executescript(sql)
            #log(request, 'New choice', request.GET.get('answer'))
            con.commit()
            return redirect('/polls/profile')
    else:
        return redirect('/polls/login')
def add_question(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            #log(request, 'New question', request.Get.get('question'))
            Question.objects.create(question_text = request.GET.get('question'), user_id=request.user.id, pub_date = datetime.now())
        return redirect('/polls')
    return redirect('/polls/login')

def profile(request):
    if request.user.is_authenticated:
        questions = Question.objects.filter(user_id=request.user.id)
        choices = Choice.objects.filter(user_id=request.user.id)
        return render(request, 'polls/profile.html', {'questions' : questions, 'choices' : choices})
    else:
        return redirect('/polls/login')

@csrf_protect
def login(request, key=0):
    page = 'polls/login.html'
    if request.user.id is None:
        if request.method == 'POST':
            un = request.POST.get('username')
            pw = request.POST.get('password')
            user = authenticate(username=un, password=pw)
            if user is None:
                text = 'Invalid login'
                #log(request, 'Failed login', un)
                return render(request, 'polls/login.html', {'text' : text})
            else:
                auth_login(request, user)
                #log(request, 'login')
                return redirect('/polls/profile')
        else:
            text = 'Please login'
    else:
        text = 'Logout user '+request.user.username+'?'
        page = 'polls/logout.html'
    return render(request, page, {'text' : text})

@csrf_protect
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        #log(request, 'logout')
    return redirect('/polls/login')

@csrf_protect
def register(request, key=0):
    if request.method == 'POST':
        un = request.POST.get('username')
        pw = request.POST.get('password')
        #em = request.POST.get('email')
        #faults = pw_faults(pw)
        #if len(faults) > 0:
        #    return render(request, 'polls/login.html', {"faults" : faults, "text" : "Please login"})
            #log(request, 'failed registration', un)

        #user = User.objects.create_user(username=un, password=pw
        #, email=em
        )
        #log(request, 'registration')
        auth_login(request, user)
        return render(request, 'polls/profile.html')

def moderation(request):
    if request.user.is_authenticated:
        if 'admin' in request.user.username:
            return HttpResponse('You are looking at the moderation page')
        else:
            return HttpResponse('You are not authorized to access this page')
    else:
        return redirect('/polls/login')

#def log(request, rtype='Empty', input='Empty'):
#    log = open('request.log', 'a+')
#    user = 'Anon'
#    if request.user.is_authenticated:
#        user = request.user.username
#    log.write('Log: '+rtype+' Input: '+input+', '+user+', '+str(datetime.now()))
#    log.close()

#def reclaimaccount(request):
#    if request.method=="POST":
#        email=request.POST.get('email')
#        try:
#            user = User.objects.get(email__exact=email)
#        except User.DoesNotExist:
#            log(request, 'Failed account reclimation', email)
#            return HttpResponse('Your login details have been sent to: '+email)
#        if user is not None:
#            newPass = generate_key()
#            user.set_password(newPass)
#            user.save()
#            send_mail(subject='Account reclimation', message='Your username is: '+user.username+' and your password is: '+newPass, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
#        return HttpResponse('Your login details have been sent to: '+email)

#def generate_key():
#    length = 10
#    characters = string.ascii_letters + string.digits
#    key = ''.join(random.choice(characters) for i in range(length))
#    return key

#def pw_faults(pw):
#    faults=[]
#    if len(pw)<8:
#        faults.append("The password needs to be atleast 8 letters long.")
#
#    upper=0
#    lower=0
#    digit=0
#    special=0
#    for i in pw:
#        if i.isdigit():
#            digit+=1
#        elif i.isalpha():
#            if i.isupper():
#                upper+=1
#            else:
#                lower+=1
#        elif not i.isalnum():
#            special+=1
#    if digit==0 or (upper+lower)==0:
#        faults.append("The password need to contain both letters and numbers.")
#    if upper==0 or lower==0:
#        faults.append("The password needs to contain both upper- and lowercase letters.")
#    if special==0:
#        faults.append("The password needs to contain atleast one special character.")
#    return faults
