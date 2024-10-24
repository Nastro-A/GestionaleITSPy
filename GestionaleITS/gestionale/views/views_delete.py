# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import ResignationForm
from ..models import Bundle, Supplier, Computer, Accessory, Student, Course, Record, Ticket

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_bundle(request, id):
    bundle = get_object_or_404(Bundle, id=id)
    computers = None
    accessories = None
    if bundle.product_type == "Computer":
        computers = Computer.objects.filter(id_bundle=bundle)
    if bundle.product_type == "Accessory":
        accessories = Accessory.objects.filter(id_bundle=bundle)
    if request.method == "POST":
        record = Record()
        bundle_copy = copy.deepcopy(bundle)
        record.prev_product_detail = bundle_copy
        if computers is not None:
            for computer in computers:
                computer.is_deleted = True
                computer.save()
                bundle.qt_available += -1
        if accessories is not None:
            for accessory in accessories:
                accessory.is_deleted = True
                accessory.save()
                bundle.qt_available += -1

        bundle.is_deleted = True
        bundle.save()

        record.date = datetime.now().date()
        record.action = "delete"
        record.product = "bundle"
        record.user = request.user
        record.save()

        return redirect('storage')
    elif request.method == "GET":
        return render(request, "gestionale/delete/deletebundle.html", {
            "id": id
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == "POST":
        record = Record()
        supplier_copy= copy.deepcopy(supplier)
        record.prev_product_detail = supplier_copy
        supplier.is_deleted = True

        record.date = datetime.now().date()
        record.action = "delete"
        record.product = "supplier"
        record.user = request.user
        record.save()

        return redirect('storage')
    elif request.method == "GET":
        return render(request, "gestionale/delete/deletesupplier.html", {
            "id": id
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_computer(request, id):
    computer = get_object_or_404(Computer, id=id)
    bundle = get_object_or_404(Bundle, id=computer.id_bundle.id)
    if request.method == "POST":
        record = Record()
        computer_copy = copy.deepcopy(computer)
        record.prev_product_detail = computer_copy
        bundle.qt = bundle.qt - 1
        bundle.qt_available = bundle.qt_available - 1
        bundle.save()
        computer.delete()

        record.date = datetime.now().date()
        record.action = "reset"
        record.product = "computer"
        record.user = request.user
        record.save()

        return redirect(f"/details/bundle/{computer.id_bundle.id}")
    elif request.method == "GET":
        return render(request, "gestionale/delete/deletecomputer.html", {
            "id": id, "id_bundle": computer.id_bundle.id
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_accessory(request, id):
    accessory = get_object_or_404(Accessory, id=id)
    bundle = get_object_or_404(Bundle, id=accessory.id_bundle.id)
    if request.method == "POST":
        record = Record()
        accessory_copy = copy.deepcopy(accessory)
        record.prev_product_detail = accessory_copy
        bundle.qt = bundle.qt - 1
        bundle.qt_available = bundle.qt_available - 1
        bundle.save()
        accessory.delete()

        record.date = datetime.now().date()
        record.action = "reset"
        record.product = "computer"
        record.user = request.user
        record.save()

        return redirect(f"/details/bundle/{accessory.id_bundle.id}")
    elif request.method == "GET":
        return render(request, "gestionale/delete/deleteaccessory.html", {
            "id": id, "id_bundle": accessory.id_bundle.id
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        record = Record()
        course_copy = copy.deepcopy(course)
        record.prev_product_detail = course_copy
        course.course_status = False
        course.save()

        record.date = datetime.now().date()
        record.action = "delete"
        record.product = "course"
        record.product_detail = course
        record.user = request.user
        record.save()

        return redirect("courses")
    elif request.method == "GET":
        return render(request, "gestionale/delete/deletecourse.html", {
            "id": id
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    course = get_object_or_404(Course, id=student.course_id.id)
    if request.method == "POST":
        form = ResignationForm(request.POST, instance=student)
        if form.is_valid():
            record = Record()
            student_copy = copy.deepcopy(student)
            record.prev_product_detail = student_copy
            student.resignation_date = datetime.strptime(form["resignation_date"].value(), "%d/%m/%Y")
            student.student_status = "resigned"
            student.save()

            record.date = datetime.now().date()
            record.action = "delete"
            record.product = "student"
            record.product_detail = student
            record.user = request.user
            record.save()
        else:
            form = ResignationForm()
            err = True
            return render(request, "gestionale/delete/deletestudent.html", {
                "err": err, "form": form, "id": id
            })
        return redirect(f"/details/course/{course.id}")
    else:
        form = ResignationForm()
        return render(request, "gestionale/delete/deletestudent.html", {
            "form": form, "id": id, "student": student, "course": course
        })
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def delete_ticket(request, id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=id)
        record = Record()

        ticket_copy = copy.deepcopy(ticket)
        record.prev_product_detail = ticket_copy
        ticket.closing_date = datetime.now().date()
        ticket.is_closed = True
        ticket.save()

        record.date = datetime.now().date()
        record.action = "close"
        record.product = "ticket"
        record.product_detail = ticket
        record.user = request.user
        record.save()

        return redirect("tickets")

    elif request.method == "GET":
        return render(request, "gestionale/delete/deleteticket.html", {
            "id": id})
    else:
        return bad_request
