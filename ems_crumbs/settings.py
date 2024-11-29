from horilla.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "ems_crumbs.context_processors.breadcrumbs",
)
