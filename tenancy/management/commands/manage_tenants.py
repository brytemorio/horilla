from django.core.management.base import BaseCommand, CommandError
from tenancy.models import BaseTenantModel, PrimaryTenant, Domain


class Command(BaseCommand):
    help = "Manage tenants (list, create_primary_tenant, delete)"

    def add_arguments(self, parser):
        # Add subcommands
        parser.add_argument(
            "action",
            type=str,
            choices=["list", "create_primary_tenant", "delete"],
            help="Action to perform: list, create, delete",
        )
        parser.add_argument(
            "--tenant_name",
            type=str,
            help="Name of the tenant (required for create and delete)",
        )
        parser.add_argument(
            "--schema_name",
            type=str,
            help="Schema name of the tenant (required for create)",
        )

        parser.add_argument(
            "--domain_name",
            type=str,
            help=" domain name of the tenant (required for create)",
        )

    def handle(self, *args, **options):
        action = options["action"]
        tenant_name = options.get("tenant_name")
        schema_name = options.get("schema_name")
        _domain_name = options.get("domain_name")

        domain_name = _domain_name if _domain_name else "localhost"

        if action == "list":
            self.list_tenants()
        elif action == "create_primary_tenant":
            if not tenant_name or not schema_name:
                raise CommandError(
                    "Both --tenant_name, --schema_name and optionally "
                    "--domain_name are required for creating a primary tenant."
                )
            self.create_primary_tenant(tenant_name, schema_name, domain_name)
        elif action == "delete":
            if not tenant_name:
                raise CommandError("--tenant_name is required for delete.")
            self.delete_tenant(tenant_name)
        else:
            raise CommandError(f"Unknown action: {action}")

    def list_tenants(self):
        tenants = BaseTenantModel.objects.all()
        if tenants.exists():
            self.stdout.write("List of tenants:")
            for tenant in tenants:
                self.stdout.write(
                    f"- {tenant.tenant_name} (schema: {tenant.schema_name})"
                )
        else:
            self.stdout.write("No tenants found.")

    def create_primary_tenant(self, tenant_name, schema_name, domain_name):
        if Domain.objects.filter(domain=domain_name).exists():
            self.stderr.write(f"Error: The domain '{domain_name}' is already in use.")
            exit(-1)
        try:
            tenant = PrimaryTenant(tenant_name=tenant_name, schema_name=schema_name)
            tenant.save()
            domain = Domain()
            domain.domain = domain_name
            domain.is_primary = True
            domain.save()
        except Exception as e:
            self.stderr.write(f"error creating primary tenant: {e}")
            exit(-1)
        self.stdout.write(
            f"Tenant '{tenant_name}' created with schema '{schema_name}'."
        )

    def delete_tenant(self, tenant_name):
        try:
            tenant = BaseTenantModel.objects.get(tenant_name=tenant_name)
            tenant.delete()
            self.stdout.write(f"Tenant '{tenant_name}' deleted.")
        except BaseTenantModel.DoesNotExist:
            self.stdout.write(f"Tenant '{tenant_name}' does not exist.")
