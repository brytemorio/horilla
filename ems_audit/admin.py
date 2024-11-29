"""
admin.py
"""

from django.contrib import admin

from ems_audit.models import AuditTag, EmsAuditInfo, EmsAuditLog

# Register your models here.

admin.site.register(AuditTag)
