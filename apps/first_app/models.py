# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bcrypt
from django.db import models
from django.contrib import messages


class UserManager(models.Manager):
    def validate_user(self,post):
        isValid = True
        if len(post.get('first_name')) < 2 :
            isValid = False

        if len(post.get('last_name')) < 2:
            isValid = False
            #add a flash message
        if len(post.get('password')) == 0 :
            isValid = False
            #add a flash message
        if post.get('password') != post.get('confPass'):
            isValid = False
            #add a flash message
        return isValid
    def log_in(self,post):
        user = self.filter(employee_number=post.get('employee_number'))
        if user[0] and bcrypt.hashpw(post.get('password').encode(), user[0].password.encode()) == user[0].password:
            return (True, user[0])
        return (False, 'notuser')

class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length=38)
    division = models.CharField(max_length=20)
    employee_number = models.IntegerField()
    age = models.IntegerField()
    payrate = models.IntegerField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)
    objects = UserManager()

class Location(models.Model):
    street = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)

class Job(models.Model):
    title = models.CharField(max_length=30)

class Clock_inManager(models.Manager):
    def validate_clockin(self, post):
        isValid = True
        if len(post.get('notes')) < 3:
            isValid = False
        return isValid

class Clock_in(models.Model):
    user = models.ForeignKey(User, related_name="clock_ins")
    location = models.ForeignKey(Location, related_name="location_in")
    job = models.ForeignKey(Job, related_name="job_in")
    time = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255)
    objects = Clock_inManager()

class Clock_outManager(models.Manager):
    def validate_clockout(self, post):
        isValid = True
        if len(post.get('notes')) < 3:
            isValid = False
        return isValid

class Clock_out(models.Model):
    user = models.ForeignKey(User, related_name="clock_outs")
    location = models.ForeignKey(Location, related_name="location_out")
    job = models.ForeignKey(Job, related_name="job_out")
    time = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255)
    lunch = models.BooleanField(default=False)
    objects = Clock_outManager()

class Company_notices(models.Model):
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
