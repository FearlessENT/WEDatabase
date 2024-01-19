import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WEData.settings")
django.setup()

from django.contrib.auth.models import Group

def create_default_groups():
    group_names = ["machinist", "assembler"]  # Add your group names here
    for name in group_names:
        Group.objects.get_or_create(name=name)
    print("Default groups created.")

if __name__ == "__main__":
    create_default_groups()
