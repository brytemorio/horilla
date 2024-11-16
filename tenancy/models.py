from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.admin import TenantAdminMixin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django_tenants.models import TenantMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from marshmallow import ValidationError
import re

# Create your models here.


def validate_tenant_name(value):
    """
    Validator to ensure tenant_name only contains ASCII letters (a-z) and no whitespace or special characters.
    """
    if not re.fullmatch(r"^[a-z]{6,15}$", value):
        raise ValidationError(
            _(
                "Tenant name must only contain ASCII letters (a-z), "
                "with no spaces or special characters, and be between "
                "6 and 15 characters long."
            )
        )


class BaseTenantModel(TenantMixin):
    """
    Abstract base model for tenant-related information.
    Includes fields common to all tenants.
    """

    tenant_name = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_tenant_name],
        verbose_name=_("Tenant Name"),
        help_text=_(
            "Enter a unique tenant name with only ASCII letters (a-z), "
            "no spaces or special characters, and a minimum of 6 characters or "
            "a  maximum of 15 characters."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    # class Meta:
    #     abstract = True
    #     verbose_name = _("Tenant")
    #     verbose_name_plural = _("Tenants")


class PrimaryTenant(BaseTenantModel):
    pass


class BusinessTenant(BaseTenantModel):
    """
    Concrete model for tenant-specific information.
    """

    # Business Information
    business_name = models.CharField(max_length=255, verbose_name=_("Business Name"))
    business_type = models.CharField(max_length=100, verbose_name=_("Business Type"))
    industry = models.CharField(max_length=100, verbose_name=_("Industry"))
    registration_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Company Registration Number")
    )

    # Contact Information
    primary_email = models.EmailField(unique=True, verbose_name=_("Primary Email"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    address = models.TextField(verbose_name=_("Business Address"))

    # Administrator Information
    admin_name = models.CharField(max_length=100, verbose_name=_("Administrator Name"))
    admin_email = models.EmailField(verbose_name=_("Administrator Email"))
    admin_phone = models.CharField(max_length=20, verbose_name=_("Administrator Phone"))

    # Subscription Information
    subscription_plan = models.CharField(
        max_length=50,
        choices=[
            ("basic", _("Basic")),
            ("standard", _("Standard")),
            ("premium", _("Premium")),
        ],
        default="basic",
        verbose_name=_("Subscription Plan"),
    )

    # Optional Customization Settings
    company_logo = models.ImageField(
        upload_to="tenant_logos/", null=True, blank=True, verbose_name=_("Company Logo")
    )
    timezone = models.CharField(
        max_length=50, default="UTC", verbose_name=_("Timezone")
    )
    default_language = models.CharField(
        max_length=10, default="en", verbose_name=_("Default Language")
    )

    def __str__(self):
        return self.business_name


class Domain(DomainMixin):
    pass


@admin.register(BaseTenantModel)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("tenant_name",)
