# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime, timedelta
from django import forms
from django.forms import SelectDateWidget, ModelForm, formset_factory, BaseFormSet
from .models import Supplier, Bundle, Computer, Accessory, Course, Student, Record, validate_image, StudentViewEditModel, Ticket


class BundleForm(forms.ModelForm):
    type_choices = (
        ("", "Selezionare il tipo di prodotto"),
        ("Accessory", "Accessorio"),
        ("Computer", "Computer")
    )
    product_type = forms.ChoiceField(choices=type_choices, initial="")
    delivery_date = forms.DateField(widget=SelectDateWidget(), initial=datetime.now().date() )
    class Meta:
        model = Bundle
        fields = "__all__"

        labels = {
            "product_type": "Tipo Prodotto",
            "product_name": "Nome Prodotto",
            "qt": "Qt",
            "qt_available": "Qt. Disponibile",
            "notes": "Note",
            "brand": "Brand",
            "line": "Linea",
            "cpu": "Cpu",
            "ram": "Ram",
            "storage_size": "Dimensione Storage",
            "price": "Prezzo",
            "delivery_date": "Data di consegna",
            "supplier_id": "Fornitore",
            "is_deleted": "È cancellato?"
        }

        widgets = {
            "delivery_date": forms.SelectDateWidget()
        }


class BaseSerialFormSet(BaseFormSet):
    def clean(self):
        super().clean()

        values = []
        for form in self.forms:
            if form.is_valid():
                form_value = form.cleaned_data.get("serial")
                if form_value:
                    values.append(form_value)

        if len(values) != len(set(values)):
            raise forms.ValidationError("I valori devono essere univoci")
        else:
            return True

class SerialForm(forms.ModelForm):
    serial = forms.CharField(max_length=255)

    class Meta:
        model = Computer
        fields = ["serial"]
        labels = {
            "serial": "Seriale"
        }


SerialFormSet = formset_factory(SerialForm, formset=BaseSerialFormSet, extra=0)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        labels = {
            "supplier_name": "Nome",
            "supplier_address": "Indirizzo",
            "supplier_phone": "Telefono",
            "supplier_email": "Email",
            "partita_iva": "Partita IVA",
            "codice_societa": "Codice Società"
        }
        exclude = ["is_deleted"]


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = "__all__"
        labels = {
            "id_student": "Studente",
            "id_bundle": "Bundle",
            "status": "Status",
            "assignment_date": "Data di assegnazione",
            "assignment_motivation": "Motivazione di assegnazione",
            "return_date": "Data di restituzione",
            "return_motivation": "Motivazione di restituzione",
            "eol": "Eol",
            "eol_date": "Data di eol",
            "notes": "Note",
            "cespite": "Cespite",
            "serial": "Seriale"
        }


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ["name", "description", "notes"]
        labels = {
            "name": "Nome Prodotto",
            "description": "Descrizione",
            "notes": "Note"
        }


class EditAccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = "__all__"
        labels = {
            "name": "Nome Prodotto",
            "description": "Descrizione",
            "id_student": "Studente",
            "id_bundle": "Bundle",
            "status": "Status",
            "assignment_date": "Data di assegnazione",
            "assignment_motivation": "Motivazione di assegnazione",
            "return_date": "Data di restituzione",
            "return_motivation": "Motivazione di restituzione",
            "notes": "Note",
        }
        exclude = [
            "assignment_date",
            "assignment_motivation",
            "return_date",
            "return_motivation"
        ]


class CSVUpdateForm(forms.Form):
    file = forms.FileField(label="Seleziona un file CSV")

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        labels = {
            "course_name": "Nome Corso",
            "course_name_extended": "Nome Corso esteso",
            "course_code": "Codice Corso",
            "course_year": "Anno Corso",
            "student_number": "Numero Studenti",
            "course_location": "Posizione Corso",
            "course_status": "Status Corso"
        }


class ResignationForm(forms.ModelForm):

    resignation_date = forms.DateField(widget=SelectDateWidget(), label="Data di Dimissioni:", initial=datetime.now().date())
    class Meta:
        model = Student
        fields = ["resignation_date"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields= "__all__"
        labels= {
            "first_name": "Nome",
            "last_name": "Cognome",
            "course_name": "Nome Corso",
            "gender": "Sesso",
            "profile_image": "Immagine Profilo",
            "id_student_course": "Id Studente Corso",
            "codice_fiscale": "Codice Fiscale",
            "course_acronym": "Sigla Corso",
            "course_code": "Codice Corso",
            "email_user": "Email Studente",
            "phone_number": "Numero di Telefono",
            "municipality_residence": "Comune di Residenza",
            "province_residence": "Provincia di Residenza",
            "student_status": "Status Studente",
            "course_status": "Status Corso",
            "course_year": "Anno Corso",
            "birth_date": "Data di Nascita",
            "municipality_birth": "Comune di Nascita",
            "province_birth": "Provincia di Nascita",
            "resignation_date": "Data di Dimissioni",
            "nation_birth": "Nazione di Nascita",
            "course_id": "Corso"
        }
        exclude = ["course_acronym", "course_code", "course_status", "course_year", "course_name"]


class AssignmentComputerForm(forms.Form):
    choice= (
        ("", "Seleziona il motivo"),
        ("deposit_paid", "Pagamento Effettuato"),
        ("replacement", "Sostitutivo"),
        ("temporary", "Temporaneo")
    )
    course_code = forms.CharField(label="Codice Corso", max_length=255)
    codice_fiscale = forms.CharField(label="Codice Fiscale", max_length=255)
    cespite = forms.CharField(label="Cespite", max_length=255)
    serial = forms.CharField(label="Seriale", max_length=255)
    assignment_date = forms.DateField(widget=SelectDateWidget(), label="Data di assegnazione", initial=datetime.now().date)
    assignment_motivation = forms.ChoiceField(choices=choice)

class AssignmentAccessoryForm(forms.Form):
    choice= (
        ("", "Seleziona il motivo"),
        ("needed", "Necessario"),
        ("replacement", "Sostitutivo"),
        ("temporary", "Temporaneo")
    )
    course_code = forms.CharField(label="Codice Corso", max_length=255)
    codice_fiscale = forms.CharField(label="Codice Fiscale", max_length=255)
    id = forms.IntegerField()
    assignment_date = forms.DateField(widget=SelectDateWidget(), label="Data di assegnazione", initial=datetime.now().date)
    assignment_motivation = forms.ChoiceField(choices=choice)

class ReturnComputerDateForm(forms.Form):
    choice = (
        ("", "Seleziona il motivo"),
        ("student_resigned", "Studente Dimesso"),
        ("damaged", "Danneggiato"),
        ("not_necessary", "Non più necessario")
    )
    return_date = forms.DateField(widget=SelectDateWidget(), label="Data di ritorno", initial=datetime.now().date)
    return_motivation = forms.ChoiceField(choices=choice)

class ReturnAccessoryDateForm(forms.Form):
    choice = (
        ("", "Seleziona il motivo"),
        ("not_necessary", "Non più necessario"),
        ("damaged", "Danneggiato"),
    )
    return_date = forms.DateField(widget=SelectDateWidget(), label="Data di ritorno", initial=datetime.now().date)
    return_motivation = forms.ChoiceField(choices=choice)

class StudentViewEditForm(forms.ModelForm):
    class Meta:
        model = StudentViewEditModel
        fields = "__all__"
        labels = {
            "profile_image": "Immagine Profilo"
        }

class TicketForm(forms.ModelForm):
    submit_date = forms.DateField(widget=SelectDateWidget(), initial=datetime.now().date(), label="Data del Ticket")
    id_student = forms.ModelChoiceField(Student.objects.order_by("course_id_id"))
    class Meta:
        model = Ticket
        fields = "__all__"
        labels = {
            "title": "Titolo del Ticket",
            "content": "Contenuto del Ticket",
            "id_student": "Studente",
            "submit_date": "Data del Ticket",
            "id_user_in_charge" : "Utente Staff assegnato"
            }
        exclude = ["is_closed", "closing_date"]

class TicketCompleteForm(forms.ModelForm):
    submit_date = forms.DateField(widget=SelectDateWidget(), initial=datetime.now().date(), label="Data del Ticket")
    closing_date = forms.DateField(widget=SelectDateWidget(), initial=datetime.now().date(), label="Data di Chiusura")
    id_student = forms.ModelChoiceField(Student.objects.order_by("course_acronym"), label="Studente")
    class Meta:
        model = Ticket
        fields = "__all__"
        labels = {
            "title": "Titolo del Ticket",
            "content": "Contenuto del Ticket",
            "id_student": "Studente",
            "submit_date": "Data del Ticket",
            "closing_date": "Data di chiusura Ticket",
            "is_closed": "É Chiuso?",
            "id_user_in_charge": "Utente Staff assegnato"
        }

class StudentViewSubmitTicketForm(forms.ModelForm):
    submit_date = forms.DateField(widget=SelectDateWidget(), initial=datetime.now().date(), label="Data del Ticket", disabled=True)
    class Meta:
        model = Ticket
        fields = "__all__"
        labels = {
            "title": "Titolo del Ticket",
            "content": "Contenuto del Ticket",
            "id_student": "Studente",
            "submit_date": "Data del Ticket",
            "closing_date": "Data di Chiusura Ticket",
            "is_closed": "É Chiuso?"
        }
        exclude = ["is_closed","id_student", "closing_date", "id_user_in_charge"]
