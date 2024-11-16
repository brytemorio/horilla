import os
import glob

# Base directory of your Django project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get all migration files except `__init__.py` in the migrations folders
migration_files = glob.glob(os.path.join(BASE_DIR, '**', 'migrations', '*.py'), recursive=True)
migration_files = [f for f in migration_files if not f.endswith('__init__.py')]

# Delete each migration file found
for migration_file in migration_files:
    try:
        os.remove(migration_file)
        print(f"Deleted: {migration_file}")
    except Exception as e:
        print(f"Error deleting {migration_file}: {e}")

print("All migrations deleted.")

