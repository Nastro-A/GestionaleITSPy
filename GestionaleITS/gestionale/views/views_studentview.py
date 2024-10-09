# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import StudentViewEditForm, StudentViewSubmitTicketForm
from ..models import Computer, Accessory, Student, Record, Ticket

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentview(request):
    student = get_object_or_404(Student, email_user=request.user.email)
    computers = Computer.objects.filter(id_student=student)
    accessories = Accessory.objects.filter(id_student=student)
    if request.method == "GET":
        return render(request, "gestionale/studentview/studentview.html" ,{
            "student": student, "computers": computers, "accessories": accessories
        })
    else:
        return bad_request
        
@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentview_edit(request):
    student = get_object_or_404(Student, email_user=request.user.email)
    if request.method == "POST":
        form = StudentViewEditForm(request.POST, request.FILES, instance=student)
        try:
            if form.is_valid():
                form.save()
                
        except ValidationError as e:
                err = True
                err_str = e
                return render(request, "gestionale/studentview/studentviewedit.html",{
                   "student": student, "err": err, "err_str": err_str
                })
        return redirect("studentview")
    elif request.method == "GET":
        form = StudentViewEditForm(instance=student)
        return render(request, "gestionale/studentview/studentviewedit.html",{
            "student": student, "form": form
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentviewtickets(request):
    student = get_object_or_404(Student, email_user = request.user.email)
    tickets = Ticket.objects.filter(id_student = student).order_by("is_closed","-submit_date", "-id")
    if request.method == "GET":
        return render(request, "gestionale/studentview/studentviewtickets.html", {
            "tickets": tickets})
    else:
        return bad_request
    
@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentviewsubmitticket(request):
    student = get_object_or_404(Student, email_user = request.user.email)
    if request.method == "POST":
        form = StudentViewSubmitTicketForm(request.POST)
        if form.is_valid():
            record = Record()
            form = form.cleaned_data
            ticket = Ticket()

            ticket.title = form["title"]
            ticket.content = form["content"]
            ticket.id_student = student
            ticket.submit_date = form["submit_date"]
            
            ticket.save()
            
            record.date = datetime.now().date()
            record.action = "submit"
            record.product = "ticket"
            record.product_detail = ticket
            record.user = request.user
            record.save()
            
        else:
            err = True
            return render(request, "gestionale/studentview/studentviewsubmitticket.html",{
                "form": form, "err": err} )
        
        return redirect("studentview_tickets")
    
    else:
        form = StudentViewSubmitTicketForm();
        return render(request, "gestionale/studentview/studentviewsubmitticket.html", {
            "form": form})
    
@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentviewcloseticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        record = Record()
        ticket.is_closed = True
        ticket.closing_date = datetime.now().date()
        ticket_copy = copy.deepcopy(ticket)
        ticket.save()

        record.date = datetime.now().date()
        record.action = "close"
        record.product = "ticket"
        record.product_detail = ticket
        record.prev_product_detail = ticket_copy
        record.user = request.user

        record.save()

        return redirect("studentview_tickets")
    elif request.method == "GET":
        return render(request, "gestionale/studentview/studentviewcloseticket.html", {
            "ticket": ticket})
    else:
        return bad_request

@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def studentviewdetailsticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "GET":
        return render(request, "gestionale/studentview/studentviewdetailsticket.html", {
            "ticket": ticket})
    else:
        return bad_request
