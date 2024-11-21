# Generated by Django 5.1.2 on 2024-11-21 22:01

import abc_back.users.models
import abc_back.validators
import django.core.validators
import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('email', models.EmailField(error_messages={'invalid': 'Пожалуйста, введите корректный email.', 'unique': 'Пользователь с таким email адресом уже зарегистрирован.'}, max_length=254, unique=True, validators=[abc_back.validators.validate_email], verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=36, validators=[abc_back.validators.NameValidator()], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=36, validators=[abc_back.validators.NameValidator()], verbose_name='last name')),
                ('middle_name', models.CharField(blank=True, max_length=36, null=True, validators=[abc_back.validators.NameValidator()], verbose_name='Отчество')),
                ('date_of_birth', models.DateField(blank=True, null=True, validators=[abc_back.validators.validate_date_of_birth], verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, verbose_name='Пол')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True, verbose_name='Телефон')),
                ('profile_image', models.ImageField(blank=True, max_length=512, null=True, upload_to=abc_back.users.models.user_avatar_upload_to, validators=[abc_back.validators.MaxFileSizeValidator(5242880), django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])], verbose_name='Изображение профиля')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', abc_back.users.models.UserManager()),
            ],
        ),
    ]
