"""
ems_automations/filters.py
"""

from ems.filters import EmsFilterSet, django_filters
from ems_automations.models import MailAutomation


class AutomationFilter(EmsFilterSet):
    """
    AutomationFilter
    """

    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = MailAutomation
        fields = "__all__"
