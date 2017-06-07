# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.db import models
from django.db.models import Count
from django.contrib import messages
from .models import *
import bcrypt


# Create your views here.
def index(request):
    # Clock_in.objects.all().delete()
    # Clock_out.objects.all().delete()
    # User.objects.all().delete()
    # Job.objects.create(
    #     title= "Designer"
    # )
    # Location.objects.create(
    #     street= "anything",
    #     city= "San Antonio",
    #     state= "TX"
    # )

    return render(request, "first_app/index.html")

def create_user(request):
    #validate and create UserManager
    if request.POST.get('admin') != True :
        admin = False
    else:
        admin = request.POST.get('admin')
    if User.objects.validate_user(request.POST):
        user =  User.objects.create(
                first_name= request.POST.get('first_name'),
                last_name= request.POST.get('last_name'),
                employee_number=request.POST.get('employee_number'),
                age= request.POST.get('age'),
                division= request.POST.get('division'),
                payrate= request.POST.get('payrate'),
                admin= admin,
                password= bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
            )

        request.session['ins'] = Clock_in.objects.filter(user_id=request.session['user_id']).count()
        request.session['outs'] = Clock_out.objects.filter(user_id=request.session['user_id']).count()
        return redirect('/dashboard')

    messages.add_message(request, messages.ERROR, 'Invalid User')
    return  redirect('/sudo')

def log_in(request):
    login = User.objects.log_in(request.POST)
    if login[0]:
        request.session['user_id'] = login[1].id
        request.session['ins'] = Clock_in.objects.filter(user_id=request.session['user_id']).count()
        request.session['outs'] = Clock_out.objects.filter(user_id=request.session['user_id']).count()
        return redirect('/dashboard')
    return redirect('/')

def log_out(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    memos = Company_notices.objects.all()
    clock_ins = request.session['ins']
    clock_outs = request.session['outs']
    user = User.objects.filter(id=request.session['user_id']).first()
    locations = Location.objects.all()
    jobs = Job.objects.all()
    context = {
        'clock_ins': clock_ins,
        'clock_outs': clock_outs,
        'user': user,
        'jobs': jobs,
        'locations': locations,
        'memos': memos
    }
    return render(request, "first_app/dashboard.html", context)

def clock_in(request):
    ins = request.session['ins']
    outs = request.session['outs']
    if ins > outs:
        # Flash message "Invalid Clock IN"
        print "invalid in"
        return redirect('/dashboard')
    if ins == outs and Clock_in.objects.validate_clockin(request.POST):
        clockin = Clock_in.objects.create(
        user= User.objects.filter(id=request.session['user_id']).first(),
        location= Location.objects.filter(id=request.POST.get('location')).first(),
        job= Job.objects.filter(id=request.POST.get('job')).first(),
        notes= request.POST.get('notes')
        )

        return redirect('/log_out')

def clock_out(request):
    ins = request.session['ins']
    outs = request.session['outs']
    if ins == outs :
        #Flash error "already clocked out"
        print "invalid out"
        return redirect('/dashboard')
    if (request.POST.get('lunch') != True):
        lunch= False
    else:
        lunch= request.POST.get('lunch')
    if Clock_out.objects.validate_clockout(request.POST):
        clockout = Clock_out.objects.create(
            user= User.objects.filter(id=request.session['user_id']).first(),
            location= Location.objects.filter(id=request.POST.get('location')).first(),
            job= Job.objects.filter(id=request.POST.get('job')).first(),
            notes= request.POST.get('notes'),
            lunch= lunch
        )
        return redirect('/log_out')
    return redirect('/dashboard')

def admin(request):
    context = {
        'ins': Clock_in.objects.all(),
        'outs': Clock_out.objects.all(),
        'memos': Company_notices.objects.all(),
        'employees': User.objects.all()
    }
    return render(request, "first_app/admin.html", context )

def create_message(request):
    if len(request.POST.get('memo')) < 10:
        messages.add_message(request, messages.ERROR, 'Memo not long enough')
        return redirect('/sudo')
    message = Company_notices.objects.create(
        message= request.POST.get('memo')
    )
    return redirect('/sudo')

def delete_message(request, id):
    message = Company_notices.objects.filter(id=id).delete()
    return redirect('/sudo')
