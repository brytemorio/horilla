"""
context_processor.py

This module is used to register context processor`
"""

from django.http import JsonResponse
from django.urls import include, path

from ems.urls import urlpatterns
from ems_audit.forms import HistoryForm
from ems_audit.models import AuditTag


def history_form(request):
    """
    This method will return the history additional field form
    """
    form = HistoryForm()
    return {"history_form": form}


def dynamic_tag(request):
    """
    This method is used to dynamically create history tags
    """

    title = request.POST["title"]
    title = AuditTag.objects.get_or_create(title=title)
    return JsonResponse({"id": title[0].id})


urlpatterns.append(path("ems-audit-log", dynamic_tag, name="ems-audit-log"))
