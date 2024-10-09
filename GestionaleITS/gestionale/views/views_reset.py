# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from copy import deepcopy
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import ReturnComputerDateForm, ReturnAccessoryDateForm
from ..models import Bundle, Computer, Accessory, Record

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def reset_computer(request, id):
    computer = get_object_or_404(Computer, id=id)
    bundle = get_object_or_404(Bundle, id=computer.id_bundle.id)
    if request.method == "POST":
        form = ReturnComputerDateForm(request.POST)
        if form.is_valid():
            record = Record()
            computer_copy = copy.deepcopy(computer)
            record.prev_product_detail = computer_copy
            form = form.cleaned_data
            computer.assignment_date = None
            computer.assignment_motivation = None
            computer.id_student = None
            computer.status = "in_stock"
            computer.return_date = form["return_date"]
            computer.return_motivation = form["return_motivation"]
            computer.save()

            record.date = datetime.now().date()
            record.action = "reset"
            record.product = "computer"
            record.product_detail = computer
            record.user = request.user
            record.save()
        return redirect(f"/details/bundle/{computer.id_bundle.id}")
    elif request.method == "GET":
        form = ReturnComputerDateForm()
        return render(request, "gestionale/reset/resetcomputer.html",{
            "computer": computer, "bundle": bundle, "form": form
        })

    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def reset_accessory(request, id):
    accessory = get_object_or_404(Accessory, id=id)
    bundle = get_object_or_404(Bundle, id=accessory.id_bundle.id)
    if request.method == "POST":
        form = ReturnAccessoryDateForm(request.POST)
        if form.is_valid():
            record = Record()
            accessory_copy = copy.deepcopy(accessory)
            record.prev_product_detail = accessory_copy
            form = form.cleaned_data
            accessory.assignment_date = None
            accessory.assignment_motivation = None
            accessory.id_student = None
            accessory.status = "in_stock"
            accessory.return_date = form["return_date"]
            accessory.return_motivation = form["return_motivation"]
            accessory.save()

            record.date = datetime.now().date()
            record.action = "reset"
            record.product = "computer"
            record.product_detail = accessory
            record.user = request.user
            record.save()
        return redirect(f"/details/bundle/{accessory.id_bundle.id}")
    elif request.method == "GET":
        form = ReturnAccessoryDateForm()
        return render(request, "gestionale/reset/resetaccessory.html", {
            "accessory": accessory, "bundle": bundle, "form": form
        })
    else:
        return bad_request
