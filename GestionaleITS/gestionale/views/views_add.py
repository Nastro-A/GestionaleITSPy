# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Bundle, Student, Supplier, Computer, Accessory, Record, Ticket
from ..forms import BundleForm, SupplierForm, SerialFormSet, AccessoryForm, CourseForm, TicketForm

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_bundle(request):
    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            record = Record()
            form = form.cleaned_data
            bundle = Bundle()
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
            record.action = "add"
            record.product = "bundle"
            record.product_detail = bundle
            record.user = request.user
            record.save()

            if form["product_type"] == "Computer":
                return redirect("/add/serial")
            if form["product_type"] == "Accessory":
                return redirect("/add/accessory")
        else:
            err = True
            return render(request, "gestionale/add/addbundle.html", {
                "err": err, "form": form
            })
        return redirect('storage')
    else:
        form = BundleForm()
        return render(request, "gestionale/add/addbundle.html", {
            "form": form
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            record = Record()
            form = form.cleaned_data
            supplier = Supplier()
            supplier.supplier_name = form["supplier_name"]
            supplier.supplier_address = form["supplier_address"]
            supplier.supplier_phone = form["supplier_phone"]
            supplier.supplier_email = form["supplier_email"]
            supplier.partita_iva = form["partita_iva"]
            supplier.codice_societa = form["codice_societa"]
            supplier.save()

            record.date = datetime.now().date()
            record.action = "add"
            record.product = "supplier"
            record.product_detail = supplier
            record.user = request.user
            record.save()

        else:
            err = True
            return render(request, "gestionale/add/addsupplier.html", {
                "form": form, "err": err
            })
        return redirect('storage')
    else:
        form = SupplierForm()
        return render(request, "gestionale/add/addsupplier.html", {
            "form": form
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_serial(request):
    bundle = Bundle.objects.last()
    qt = range(bundle.qt)
    if request.method == "POST":
        form_serial = SerialFormSet(request.POST, initial=[{} for _ in qt])
        try:
            if form_serial.clean():
                if form_serial.is_valid():
                    for form in form_serial:
                        form = form.cleaned_data
                        record = Record()

                        computer = Computer()
                        computer.id_bundle = bundle
                        computer.status = "in_stock"
                        computer.eol = False
                        computer.eol_date = None
                        computer.serial = form["serial"]
                        computer.save()

                        record.date = datetime.now().date()
                        record.action = "add"
                        record.product = "computer"
                        record.product_detail = computer
                        record.user = request.user
                        record.save()



                return redirect('storage')
        except ValidationError:
            err = True
            err_str = "L'inserimento é errato o incompleto!"
            return render(request, "gestionale/add/addserial.html", {
                "err": err, "form_serial": form_serial, "err_str": err_str
            })
    else:
        form_serial = SerialFormSet(initial=[{} for _ in qt])
        return render(request, "gestionale/add/addserial.html", {
            "form_serial": form_serial, "bundle_qt": qt
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_accessory(request):
    bundle = Bundle.objects.last()
    qt = range(bundle.qt)
    if request.method == "POST":
        form = AccessoryForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            for _ in qt:
                record = Record()
                accessory = Accessory()
                accessory.id_bundle = bundle
                accessory.name = form["name"]
                accessory.description = form["description"]
                accessory.status = "in_stock"
                accessory.notes = form["notes"]
                accessory.save()

                record.date = datetime.now().date()
                record.action = "add"
                record.product = "accessory"
                record.product_detail = accessory
                record.user = request.user
                record.save()
        else:
            err = True
            return render(request, "gestionale/add/addaccessory.html", {
                "err": err, "form": form
            })
        return redirect('storage')
    else:
        form = AccessoryForm()
        return render(request, "gestionale/add/addaccessory.html", {
           "form": form
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            record = Record()
            form.save()

            record.date = datetime.now().date()
            record.action = "add"
            record.product = "course"
            record.product_detail = form.cleaned_data
            record.user = request.user
            record.save()

        else:
            form = CourseForm()
            err = True
            return render(request, "gestionale/add/addcourse.html", {
                "form": form, "err": err
            })
        return redirect("courses")
    else:
        form = CourseForm()
        return render(request, "gestionale/add/addcourse.html",{
            "form": form
        })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            record = Record()
            form.save()
            
            record.date = datetime.now().date()
            record.action = "add"
            record.product = "ticket"
            record.product_detail = form.cleaned_data
            record.user = request.user
            record.save()
        else:
            form = TicketForm()
            err = True
            return render(request, "gestionale/add/addticket.html", {
                "form": form, "err": err})
        
        return redirect("tickets")
    
    else:
        form = TicketForm(initial={"id_user_in_charge": request.user})
        return render(request, "gestionale/add/addticket.html", {
            "form": form})
