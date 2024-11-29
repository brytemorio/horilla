from django.urls import include, path

urlpatterns = [
    path("auth/", include("ems_api.api_urls.auth.urls")),
    path("asset/", include("ems_api.api_urls.asset.urls")),
    path("base/", include("ems_api.api_urls.base.urls")),
    path("employee/", include("ems_api.api_urls.employee.urls")),
    path("notifications/", include("ems_api.api_urls.notifications.urls")),
    path("payroll/", include("ems_api.api_urls.payroll.urls")),
    path("attendance/", include("ems_api.api_urls.attendance.urls")),
    path("leave/", include("ems_api.api_urls.leave.urls")),
]
