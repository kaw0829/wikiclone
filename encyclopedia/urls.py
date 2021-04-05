from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("create_entry.html",views.add_entry, name="add_entry"),
    path("<str:title>",views.get_entry, name="entrys"),
    path("edit.html/<title>", views.edit, name="edit")
]
