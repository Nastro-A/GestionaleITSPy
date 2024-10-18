# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.defaults import bad_request

from ..models import Bundle, Supplier, Student, Course, Ticket

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def storage(request):
    bundles = Bundle.objects.all()
    if request.method == "GET":
        return render(request, "gestionale/list/storage.html", {
            "bundles": bundles
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def suppliers(request):
    suppliers = Supplier.objects.filter(is_deleted = False)
    if request.method == "GET":
        return render(request, "gestionale/list/suppliers.html", {
            "suppliers": suppliers
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def students(request):
    students = Student.objects.all().order_by("course_acronym")
    if request.method == "GET":
        return render(request, "gestionale/list/students.html", {
            "students": students
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def courses(request):
    courses = Course.objects.all()
    if request.method == "GET":
        return render(request, "gestionale/list/courses.html", {
            "courses": courses
        })
    else:
        return bad_request

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def tickets(request):
    tickets = Ticket.objects.filter(is_closed = False).order_by("-submit_date", "-id")
    if request.method == "GET":
        return render(request, "gestionale/list/tickets.html", {
            "tickets": tickets})
    else:
        return bad_request
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def tickets_closed(request):
    tickets = Ticket.objects.filter(is_closed = True).order_by("-closing_date", "-id")
    if request.method == "GET":
        return render(request, "gestionale/list/ticketsclosed.html", {
            "tickets": tickets})
    else:
        return bad_request
