# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



from .views import views
from .views import views_delete, views_add, views_edit, views_list, views_assignment, views_reset, views_details, views_studentview

urlpatterns = [
    path("", views.index, name="index"),
    path("storage", views_list.storage, name="storage"),
    path("suppliers", views_list.suppliers, name="suppliers"),
    path("students", views_list.students, name="students"),
    path("courses", views_list.courses, name="courses"),
    path("tickets", views_list.tickets, name="tickets"),
    path("tickets/closed", views_list.tickets_closed, name="tickets_closed"),
    
    path("assignment", views_assignment.assignment, name="assignment"),
    path("assignment/computer", views_assignment.assignment_computer, name="assignment_computer"),
    path("assignment/accessory", views_assignment.assignment_accessory, name="assignment_accessory"),
    
    path("add/bundle", views_add.add_bundle, name="add_bundle"),
    path("add/supplier", views_add.add_supplier, name="add_supplier"),
    path("add/serial", views_add.add_serial, name="add_serial"),
    path("add/accessory", views_add.add_accessory, name="add_accessory"),
    path("add/course", views_add.add_course, name="add_course"),
    path("add/ticket", views_add.add_ticket, name="add_ticket"),
    
    path("edit/bundle/<int:id>", views_edit.edit_bundle, name="edit_bundle"),
    path("edit/supplier/<int:id>", views_edit.edit_supplier, name="edit_supplier"),
    path("edit/computer/<int:id>", views_edit.edit_computer, name="edit_computer"),
    path("edit/accessory/<int:id>", views_edit.edit_accessory, name="edit_accessory"),
    path("edit/course/<int:id>", views_edit.edit_course, name="edit_course"),
    path("edit/student/<int:id>", views_edit.edit_student, name="edit_student"),
    path("edit/ticket/<int:id>", views_edit.edit_ticket, name="edit_ticket"),
    
    path("delete/bundle/<int:id>", views_delete.delete_bundle, name="delete_bundle"),
    path("delete/supplier/<int:id>", views_delete.delete_supplier, name="delete_supplier"),
    path("delete/computer/<int:id>", views_delete.delete_computer, name="delete_computer"),
    path("delete/accessory/<int:id>", views_delete.delete_accessory, name="delete_accessory"),
    path("delete/course/<int:id>", views_delete.delete_course, name="delete_course"),
    path("delete/student/<int:id>", views_delete.delete_student, name="delete_student"),
    path("delete/ticket/<int:id>", views_delete.delete_ticket, name="delete_ticket"),
    
    path("details/bundle/<int:id>", views_details.details_bundle, name="details_bundle"),
    path("details/course/<int:id>", views_details.details_course, name="details_course"),
    path("details/student/<int:id>", views_details.details_student, name="details_student"),
    path("details/ticket/<int:id>", views_details.details_ticket, name="details_ticket"),
    
    path("reset/computer/<int:id>", views_reset.reset_computer, name="reset_computer"),
    path("reset/accessory/<int:id>", views_reset.reset_accessory, name="reset_accessory"),

    path("import/students", views.import_students, name="import_students"),
    
    path("toggle/course/<int:id>", views.toggle_course, name="toggle_course"),

    path("take/ticket/<int:id>", views.take_ticket, name="take_ticket"),
    
    path("studentview", views_studentview.studentview, name="studentview"),
    path("studentview/edit", views_studentview.studentview_edit, name="studentview_edit"),
    path("studentview/tickets", views_studentview.studentviewtickets, name="studentview_tickets"),
    path("studentview/submit/ticket", views_studentview.studentviewsubmitticket, name="studentview_submit_tickets"),
    path("studentview/close/ticket/<int:id>", views_studentview.studentviewcloseticket, name="studentview_close_ticket"),
    path("studentview/ticket/<int:id>", views_studentview.studentviewdetailsticket, name="studentview_details_ticket"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
