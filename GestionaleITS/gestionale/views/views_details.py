# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.utils.autoreload import request_finished
from django.views.defaults import bad_request

from ..models import Bundle, Computer, Accessory, Student, Course, Ticket

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def details_bundle(request, id):
    bundle = get_object_or_404(Bundle, id=id)
    bundle_type = bundle.product_type
    supplier = bundle.supplier_id
    computers = None
    accessories = None
    if bundle.product_type == "Computer":
        computers = Computer.objects.filter(id_bundle_id=id).order_by("id")
    if bundle.product_type == "Accessory":
        accessories = Accessory.objects.filter(id_bundle_id=id).order_by("id")
    if request.method == "GET":
        return render(request, "gestionale/details/detailsbundle.html", {
            "bundle": bundle, "computers": computers, "accessories": accessories, "bundle_type": bundle_type,
            "supplier": supplier
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def details_course(request, id):
    course = get_object_or_404(Course, id=id)
    students = Student.objects.filter(course_id=id).order_by("id")
    if request.method == "GET":
        return render(request, "gestionale/details/detailscourse.html", {
            "course": course, "students": students
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def details_student(request, id):
    student = get_object_or_404(Student, id=id)
    computers = Computer.objects.filter(id_student_id=id).order_by("id")
    accessories = Accessory.objects.filter(id_student_id=id).order_by("id")
    if request.method == "GET":
        return render(request, "gestionale/details/detailsstudent.html", {
            "student": student, "computers": computers, "accessories": accessories
        })
    else:
        return bad_request
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def details_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "GET":
        return render(request, "gestionale/details/detailsticket.html", {
            "ticket": ticket})
    else:
        return bad_request
