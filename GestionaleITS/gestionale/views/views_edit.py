# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import BundleForm, SupplierForm, ComputerForm, EditAccessoryForm, CourseForm, StudentForm, TicketCompleteForm, TicketForm
from ..models import Bundle, Supplier, Computer, Accessory, Student, Course, Record, Ticket

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_bundle(request, id):
    bundle = get_object_or_404(Bundle, id=id)
    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            record = Record()
            bundle_copy = copy.deepcopy(bundle)
            record.prev_product_detail = bundle_copy
            form = form.cleaned_data
            #verificare se si può usare form.save()
            bundle.product_type = form["product_type"]
            bundle.product_name = form["product_name"]
            bundle.qt = form["qt"]
            bundle.qt_available = form["qt_available"]
            bundle.notes = form["notes"]
            bundle.brand = form["brand"]
            bundle.line = form["line"]
            if form["product_type"] == "Computer":
                bundle.cpu = form["cpu"]
                bundle.ram = form["ram"]
                bundle.storage_size = form["storage_size"]
            bundle.price = form["price"]
            bundle.delivery_date = form["delivery_date"]
            bundle.supplier_id = form["supplier_id"]
            bundle.is_deleted = form["is_deleted"]
            bundle.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "bundle"
            record.product_detail = bundle
            record.user = request.user
            record.save()
        else:
            err = True
            return render(request, "gestionale/edit/editbundle.html", {
            "err": err, "id": id, "form": form
            })
        return redirect('storage')
    else:
        form = BundleForm(instance=bundle)
        return render(request, "gestionale/edit/editbundle.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            record = Record()
            supplier_copy = copy.deepcopy(supplier)
            record.prev_product_detail = supplier_copy
            form.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "supplier"
            record.product_detail = supplier
            record.user = request.user
            record.save()

        else:
            err = True
            return render(request, "gestionale/edit/editsupplier.html", {
                "err": err, "id": id, "form": form
            })
        return redirect('suppliers')
    else:
        form = SupplierForm(instance=supplier)
        return render(request, "gestionale/edit/editsupplier.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_computer(request, id):
    computer = get_object_or_404(Computer, id = id)
    bundle_id = computer.id_bundle.id
    if request.method == "POST":
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            record = Record()
            computer_copy = copy.deepcopy(computer)
            record.prev_product_detail = computer_copy
            form.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "computer"
            record.product_detail = computer
            record.user = request.user
            record.save()
        else:
            err = True
            return render(request, "gestionale/edit/editcomputer.html", {
                "err": err, "form": form, "id": id
            })
        return redirect(f'/details/bundle/{bundle_id}')
    else:
        form = ComputerForm(instance=computer)
        return render(request, "gestionale/edit/editcomputer.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_accessory(request, id):
    accessory = get_object_or_404(Accessory, id=id)
    bundle_id = accessory.id_bundle.id
    if request.method == "POST":
        form = EditAccessoryForm(request.POST, instance=accessory)
        if form.is_valid():
            record = Record()
            accessory_copy = copy.deepcopy(accessory)
            record.prev_product_detail = accessory_copy
            form.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "accessory"
            record.product_detail = accessory
            record.user = request.user
            record.save()

        else:
            err = True
            return render(request, "gestionale/edit/editaccessory.html", {
                "err": err, "form": form, "id": id
            })
        return redirect(f'/details/bundle/{bundle_id}')
    else:
        form = EditAccessoryForm(instance=accessory)
        return render(request, "gestionale/edit/editaccessory.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            record = Record()
            course_copy = copy.deepcopy(course)
            record.prev_product_detail = course_copy
            form.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "course"
            record.product_detail = course
            record.user = request.user
            record.save()

        else:
            form = CourseForm(instance=course)
            err = True
            return render(request, "gestionale/edit/edutcourse.html", {
                "form": form, "err": err, "id": id
            })
        return redirect("courses")
    else:
        form = CourseForm(instance=course)
        return render(request, "gestionale/edit/editcourse.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        try:
            if form.is_valid():
                record = Record()
                student_copy = copy.deepcopy(student)
                record.prev_product_detail = student_copy
                form.save()

                record.date = datetime.now().date()
                record.action = "edit"
                record.product = "student"
                record.product_detail = student
                record.user = request.user
                record.save()

        except ValidationError as e:
            form = StudentForm(instance=student)
            err = True
            err_str = e
            return render(request, "gestionale/editstudent.html", {
                "form": form, "err": err, "err_str": err_str
            })
        return redirect(f"/details/course/{student.course_id.id}")
    else:
        form = StudentForm(instance=student)
        return render(request, "gestionale/edit/editstudent.html", {
            "form": form, "id": id
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def edit_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        form = TicketCompleteForm(request.POST, instance=ticket)
        if form.is_valid():
            record = Record()
            ticket_copy = copy.deepcopy(ticket) 
            record.prev_product_detail = ticket_copy
            form.save()

            record.date = datetime.now().date()
            record.action = "edit"
            record.product = "ticket"
            record.product_detail = ticket
            record.user = request.user
            record.save()

            return redirect("tickets")
    else:
        form = TicketCompleteForm(instance=ticket, initial={"id_user_in_charge": request.user})
        return render(request, "gestionale/edit/editticket.html", {
            "form": form, "id": id})
