
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
                return render(request, "gestionale/importstudents.html", {
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
                    course = get_object_or_404(Course, course_code=row["Codice Corso"])
                    birth_date = datetime.strptime(row["DataNascita"], "%d/%m/%Y")
                    student = Student()
                    student.id_student_course = row["IDAllievoCorso"]
                    student.codice_fiscale = row["CodiceFiscale"]
                    student.course_acronym = row["SiglaCorso"]
                    student.last_name = row["Cognome"]
                    student.first_name = row["Nome"]
                    student.email_user = row["EmailUser"]
                    student.phone_number = row["Tel"]
                    student.municipality_residence = row["ComuneRes"]
                    student.province_residence = row["ProvRes"]
                    student.student_status = row["StatoAllievo"]
                    student.birth_date = birth_date
                    student.municipality_birth = row["ComuneNascita"]
                    student.province_birth = row["ProvNascita"]
                    student.resignation_date = None if row["DataDimissioni"]=="" else row["DataDimissioni"]
                    student.gender = row["Genere"]
                    student.nation_birth = row["NazioneNasc"]
                    student.course_id = course
                    student.save()
            except Exception as e:
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/importstudents.html", {
                    "err": err, "form": form, "e": e
                })
            return redirect('import_students')
        else:
            form = CSVUpdateForm()
            err = True
            return render(request, "gestionale/importstudents.html", {
                 "err": err, "form": form
            })
    else:
        form = CSVUpdateForm()
        return render(request, "gestionale/importstudents.html", {
            "form": form
        })

def import_bundle(request):
    if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/bundle.html",{
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "bundle"
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    pass
            except:
                 if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/bundle.html",{
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "bundle"
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    pass
            except:
                pass
    passpass
    pass

def import_computers(request):
 if request.method == "POST":
        form = CSVUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.endswith(".csv"):
                form = CSVUpdateForm()
                err = True
                return render(request, "gestionale/import/computers.html",{
                    "err": err, "form": form
                })
            try:
                record = Record()
                record.date = datetime.now().date()
                record.action = "import"
                record.product = "computers"
                record.user = request.user
                record.save()

                csv_data = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(csv_data)
                for row in reader:
                    bundle= get_object_or_404(Bundle, id = row["Id Bundle"])
                    
                    pass
            except:
                pass

def import_accessories(request):
    pass

def import_courses(request):
    pass


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
