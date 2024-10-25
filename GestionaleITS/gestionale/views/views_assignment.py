# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import AssignmentComputerForm, AssignmentAccessoryForm, CespiteForm
from ..models import Computer, Accessory, Student, Course, Record

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def assignment(request):
    if request.method == "GET":
        return render(request, "gestionale/assignment/assignment.html")
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def assignment_computer(request):
    if request.method == "POST":
        form = AssignmentComputerForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            try:
                course = get_object_or_404(Course, course_code=form["course_code"])
                student = get_object_or_404(Student, codice_fiscale=form["codice_fiscale"], course_id=course)
                computer = get_object_or_404(Computer, serial=form["serial"])
                record = Record()
                computer_copy = copy.deepcopy(computer)
                record.prev_product_detail = computer_copy
                eol_date = (form["assignment_date"] + timedelta(days=1460))
                computer.status = "assigned"
                computer.id_student = student
                computer.assignment_date = form["assignment_date"]
                computer.eol_date = eol_date
                computer.assignment_motivation = form["assignment_motivation"]
                computer.save()

                record.date = datetime.now().date()
                record.action = "assignment"
                record.product = "computer"
                record.product_detail = computer
                record.user = request.user
                record.save()

            except Http404:
                form = AssignmentComputerForm()
                err = True
                err_str = "Uno o più dei valori inseriti non é stato trovato"
                return render(request, "gestionale/assignment/assignment_computer.html", {
                    "err": err, "err_str": err_str, "form": form
                })
        else:
            form = AssignmentComputerForm()
            err = True
            err_str = "L'inserimento è incompleto o errato!"
            return render(request, "gestionale/assignment/assignment_computer.html", {
                "err": err, "err_str": err_str, "form": form
            })
        return redirect("assignment_computer")
    else:
        form = AssignmentComputerForm()
        err = False
        err_str = ""
        return render(request, "gestionale/assignment/assignment_computer.html", {
            "form": form, "err": err, "err_str": err_str
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def assignment_accessory(request):
    if request.method == "POST":
        form = AssignmentAccessoryForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            try:
                course = get_object_or_404(Course, course_code=form["course_code"])
                student = get_object_or_404(Student, codice_fiscale=form["codice_fiscale"], course_id=course)
                accessory = get_object_or_404(Accessory, id=form["id"])
                record = Record()
                accessory_copy = copy.deepcopy(accessory)
                record.prev_product_detail = accessory_copy
                accessory.id_student = student
                accessory.status = "assigned"
                accessory.assignment_date = form["assignment_date"]
                accessory.assignment_motivation = form["assignment_motivation"]
                accessory.save()

                record.date = datetime.now().date()
                record.action = "assignment"
                record.product = "accessory"
                record.product_detail = accessory
                record.user = request.user
                record.save()

            except Http404:
                form = AssignmentAccessoryForm()
                err = True
                err_str = "Uno o più dei valori inseriti non é stato trovato"
                return render(request, "gestionale/assignment/assignment_accessory.html", {
                    "err": err, "err_str": err_str, "form": form
                })
        else:
            form = AssignmentAccessoryForm()
            err = True
            err_str = "L'inserimento è incompleto o errato!"
            return render(request, "gestionale/assignment/assignment_accessory.html", {
                "err": err, "err_str": err_str, "form": form
            })
        return redirect("assignment_accessory")
    else:
        form = AssignmentAccessoryForm()
        err = False
        err_str = ""
        return render(request, "gestionale/assignment/assignment_accessory.html", {
            "form": form, "err": err, "err_str": err_str
        })
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def assignment_cespite(request):
    if request.method == "POST":
        form = CespiteForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            try:
                record = Record()
                computer = get_object_or_404(Computer, serial=form["serial"])
                computer_copy = copy.deepcopy(computer)
                computer.cespite = form["cespite"]
                computer.save()
                
                record.date = datetime.now().date()
                record.action = "assignment"
                record.product = "cespite"
                record.product_detail = computer
                record.prev_product_detail = computer_copy
                record.user = request.user
                record.save()
            except Http404:
                form = CespiteForm()
                err = True
                err_str = "Uno o più dei valori inseriti non é stato trovato"
                return render(request, "gestionale/assignment/cespite.html", {
                    "err": err, "err_str": err_str, "form": form
                })
            return redirect("assignment_cespite")
        else:
            form = CespiteForm()
            err = True
            err_str = "L'inserimento é incompleto o errato!"
            return render(request, "gestionale/assignment/cespite.html", {
                "form": form, "err": err, "err_str": err_str})
        
    else:
        form = CespiteForm()
        return render(request, "gestionale/assignment/cespite.html", {
            "form": form})
        
