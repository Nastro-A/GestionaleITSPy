# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

# Create your models here.

class Record(models.Model):
    date = models.DateField()
    action = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    product_detail = models.TextField(null=True)
    prev_product_detail = models.TextField(null=True)

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    supplier_address = models.CharField(max_length=255)
    supplier_phone = models.CharField(max_length=255)
    supplier_email = models.EmailField(max_length=255)
    partita_iva = models.CharField(max_length=255)
    codice_societa = models.CharField(max_length=255)


    def __str__(self):
        return f"Nome: {self.supplier_name}, Indirizzo: {self.supplier_address}, Telefono: {self.supplier_phone}, Email: {self.supplier_email}, Partita IVA: {self.partita_iva}, Codice Societá: {self.codice_societa}"


class Bundle(models.Model):
    product_type = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    qt = models.IntegerField()
    qt_available = models.IntegerField()
    notes = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    cpu = models.CharField(max_length=255, blank=True)
    ram = models.CharField(max_length=255, blank=True)
    storage_size = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    supplier_id = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"Tipo Prodotto: {self.product_type}, Nome Prodotto: {self.product_name}, Qt: {self.qt}, Qt. Disponibile: {self.qt_available}, Note: {self.notes}, Brand: {self.brand}, Linea: {self.line}, Cpu: {self.cpu}, Ram: {self.ram}, Storage: {self.storage_size}, Prezzo: {self.price}, Data di consegna: {self.delivery_date}, Fornitore: {self.supplier_id.supplier_name} È cancellato?: {self.is_deleted}"


class Course(models.Model):
    course_name = models.CharField(max_length=255, blank= True)
    course_name_extended = models.CharField(max_length=255, blank= True)
    course_code = models.CharField(max_length=255)
    course_year = models.IntegerField(blank= True)
    student_number = models.IntegerField(blank= True, null= True)
    course_location = models.CharField(max_length=255)
    course_status = models.BooleanField(default= True)

    def __str__(self):
        return f"Id Corso: {self.id}, Nome Corso: {self.course_name}, Anno Corso: {self.course_year}"

def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Il file è troppo grande. La dimensione massima è 2 MB.")

    img = Image.open(image)
    width = img.width
    height = img.height
    max_width = 200
    max_height = 200
    if width > max_width or height > max_height:
        raise ValidationError(f"Le dimensioni dell'immagine devono essere al massimo {max_width}x{max_height} pixel.")
    else:
        return image

class Student(models.Model):
    profile_image = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, validators=[validate_image])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    codice_fiscale = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    id_student_course = models.IntegerField(blank= True, null=True)
    course_acronym = models.CharField(max_length=255)
    email_user = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    municipality_residence = models.CharField(max_length=255)
    province_residence = models.CharField(max_length=255)
    municipality_birth = models.CharField(max_length=255)
    province_birth = models.CharField(max_length=255)
    nation_birth = models.CharField(max_length=255)
    resignation_date = models.DateField(null=True, blank=True)
    student_status = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, related_name="students",  on_delete=models.PROTECT)

    def __str__(self):
        return f"Nome: {self.first_name}, Cognome: {self.last_name}, Sesso: {self.gender}, Data di nascita: {self.birth_date},  Corso: {self.course_id.course_name}, Anno corso {self.course_id.course_year}"


class Computer(models.Model):
    id_student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.PROTECT)
    id_bundle = models.ForeignKey(Bundle, related_name="bundles" ,  on_delete=models.PROTECT)
    # deve essere una choice
    status = models.CharField(max_length=255)
    assignment_date = models.DateField(blank=True, null=True)
    #deve essere una choice
    assignment_motivation = models.CharField(max_length=255, blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    return_motivation = models.CharField(max_length=255, blank=True, null=True)
    eol = models.BooleanField(default=False)
    eol_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    cespite = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=255, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Id Studente: {self.id_student}, Id Bundle: {self.id_bundle}, Status: {self.status}, Data di assegnazione: {self.assignment_date}, Motivazione di Assegnazione: {self.assignment_motivation}, Data di restituzione: {self.return_date}, Motivazione di restituzione: {self.return_motivation}, Eol: {self.eol}, Data di Eol: {self.eol_date}, Note: {self.notes}, Cespite: {self.cespite}, Seriale: {self.serial}"


class Accessory(models.Model):
    id_student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.PROTECT)
    id_bundle = models.ForeignKey(Bundle, related_name="bundles_accessory" ,  on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assignment_date = models.DateField(blank=True, null=True)
    assignment_motivation = models.CharField(max_length=255, blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    return_motivation = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Id Studente: {self.id_student}, Id Bundle: {self.id_bundle}, Name: {self.name}, Status: {self.status}, Data di assegnazione: {self.assignment_date}, Motivazione di Assegnazione: {self.assignment_motivation}, Data di restituzione: {self.return_date}, Motivazione di restituzione: {self.return_motivation}, Note: {self.notes}"

class StudentViewEditModel(models.Model):
    profile_image = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, validators=[validate_image])

class Ticket(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    id_student = models.ForeignKey(Student, on_delete=models.PROTECT)
    submit_date = models.DateField()
    closing_date = models.DateField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    id_user_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,limit_choices_to={'is_staff': True}, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"title: {self.title} content: {self.content} student: {self.id_student} submit_date:{self.submit_date} closing_date:{self.closing_date} is_closed:{self.is_closed}"
        
