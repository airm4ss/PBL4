# Generated by Django 5.1 on 2024-08-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=255)),
                ('effective_date', models.DateField()),
                ('privacy_manager', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.CharField(max_length=255)),
                ('has_privacy_department', models.BooleanField(default=False)),
                ('privacy_department', models.CharField(blank=True, max_length=255, null=True)),
                ('department_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('department_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('department_fax', models.CharField(blank=True, max_length=20, null=True)),
                ('cctv', models.BooleanField(default=False)),
                ('delegate', models.CharField(choices=[('no_delegate', 'No Delegate'), ('delegate', 'Delegate')], default='no_delegate', max_length=50)),
                ('no_delegate_details', models.CharField(blank=True, max_length=255, null=True)),
                ('sections', models.JSONField(blank=True, null=True)),
                ('feature_data', models.JSONField(blank=True, null=True)),
                ('consent_info', models.JSONField(blank=True, null=True)),
                ('extra_rows', models.JSONField(blank=True, null=True)),
                ('previous_policy_links', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
