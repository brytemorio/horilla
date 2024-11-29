from django.contrib import admin

from ems_views.models import ActiveGroup, ActiveTab, ToggleColumn

admin.site.register([ToggleColumn, ActiveTab, ActiveGroup])
