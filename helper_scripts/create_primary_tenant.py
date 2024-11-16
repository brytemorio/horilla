from tenancy.models import PrimaryTenant, Domain

if __name__ == "__main__":
    tenant = PrimaryTenant(schema_name="primary_tenant", tenant_name="primary_tenant")
    try:
        tenant.save()
    except Exception as e:
        print(f"error creating primary schema: {e}")
        exit(-1)

    domain = Domain()
    domain.domain = "localhost"
    domain.tenant = tenant
    domain.is_primary = True
    domain.save()
