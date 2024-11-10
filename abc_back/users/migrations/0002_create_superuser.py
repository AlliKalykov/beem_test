from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, IntegrityError


def create_superuser(apps, schema_editor) -> None:
    User = apps.get_model("users", "User")
    try:
        User.objects.create_superuser(settings.SUPERUSER_LOGIN, settings.SUPERUSER_PASSWORD)
    except IntegrityError:
        User.objects.filter(
            email=settings.SUPERUSER_LOGIN,
        ).update(password=make_password(settings.SUPERUSER_PASSWORD))


def delete_superuser(apps, schema_editor) -> None:
    User = apps.get_model("users", "User")
    User.objects.filter(email=settings.SUPERUSER_LOGIN).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser),
    ]
