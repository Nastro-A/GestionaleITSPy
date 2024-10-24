
# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
import csv
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import bad_request

from ..forms import Bundle, CSVUpdateForm
from ..models import Computer, Accessory, Student, Course, Record, Ticket

from django.contrib.auth.decorators import user_passes_test, login_required


# Create your views here.

@login_required
def index(request):
    if request.user.is_superuser or request.user.is_staff:
        computers_available_count = Computer.objects.filter(status="in_stock").count()
        accessories_available_count = Accessory.objects.filter(status="in_stock").count()
        if request.method == "GET":
            return render(request, "gestionale/index.html",{
                "computers_available_count": computers_available_count,
                "accessories_available_count": accessories_available_count
            })
        else:
            return bad_request
    else:
        return redirect("studentview")

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def import_students(request):
    if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/students.html", {
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "students"
                record.product_detail = csv_file
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    course = get_object_or_404(Course, course_code=row[""])
                    birth_date = datetime.strptime(row["DataNascita"], "%m/%d/%Y")
                    student = Student()
                    student.codice_fiscale = row["CodiceFiscale"]
                    student.course_acronym = row[""]
                    student.last_name = row["Cognome"]
                    student.first_name = row["Nome"]
                    student.email_user = row["EmailGSuite"]
                    student.phone_number = row["Tel"]
                    student.municipality_residence = row["ComuneRes"]
                    student.province_residence = row["ProvRes"]
                    student.student_status = row["StatoAllievo"]
                    student.birth_date = birth_date
                    student.municipality_birth = row["ComuneNascita"]
                    student.province_birth = row["ProvNascita"]
                    student.resignation_date = None if row["DataDimissioni"]=="" else row["DataDimissioni"]
                    student.gender = row["Sex"]
                    student.nation_birth = row["NazioneNasc"]
                    student.course_id = course
                    student.save()
            except Exception as e:
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/students.html", {
                    "err": err, "form": form, "e": e
                })
            return redirect('import_students')
        else:
            form = CSVUpdateForm()
            err = True
            return render(request, "gestionale/import/students.html", {
                 "err": err, "form": form
            })
    else:
        form = CSVUpdateForm()
        return render(request, "gestionale/import/students.html", {
            "form": form
        })

def import_courses(request):
     if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/courses.html",{
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "courses"
                record.product_detail = csv_file
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    course = Course()
                    course.course_name = row["Nome"]
                    course.course_name_extended = row["Nome Esteso"]
                    course.course_code = row["Codice"]
                    course.course_year = row["Anno"]
                    course.course_location = row["Posizione"]
                    course.student_number = row["Numero Studenti"]
                    if row["Status"] == 0:
                        course.course_status = False
                    else:
                        course.course_status = True
                        
                    course.save()
                    
                return redirect("courses")
            except Exception as e:
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/courses.html", {
                    "err": err, "form": form, "e": e})

        else:
            form = CSVUpdateForm()
            err = True
            return render(request, "gestionale/import/courses.html", {
                 "err": err, "form": form
            })
     else:
        form = CSVUpdateForm()
        return render(request, "gestionale/import/courses.html", {
            "form": form
        })
          

def import_serials(request):
    if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/serials.html",{
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "computers"
                record.product_detail = csv_file
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    bundle = get_object_or_404(Bundle, id = row["Id Bundle"])
                    computer = Computer()
                    computer.id_bundle = bundle
                    computer.status = "in_stock"
                    computer.serial = row["Seriale"]
                    computer.is_deleted = False
                    computer.eol = False
                    computer.eol_date = None
                    computer.save()

                return redirect("storage")
            except Exception as e:
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/serials.html", {
                    "err": err, "form": form, "e": e})

        else:
            form = CSVUpdateForm()
            err = True
            return render(request, "gestionale/import/serials.html", {
                 "err": err, "form": form
            })
    else:
        form = CSVUpdateForm()
        return render(request, "gestionale/import/serials.html", {
            "form": form
        })
            

@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def toggle_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == "POST":
        course.course_status = not course.course_status
        course.save()
        return redirect("courses")
    else:
        return bad_request
        
@user_passes_test(lambda u: u.is_superuser or u.is_staff )
def take_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == "POST":
        record = Record()
        ticket_copy = copy.deepcopy(ticket)
        ticket.id_user_in_charge = request.user
        ticket.save()

        record.date = datetime.now().date()
        record.action = "take"
        record.product = "ticket"
        record.product_detail = ticket
        record.prev_product_detail = ticket_copy
        record.user = request.user

        record.save()
        
        return redirect("tickets")
    else:
       return bad_request
