# Generated by Django 5.0.6 on 2025-02-02 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0002_alter_grade_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ['-date_graded']},
        ),
    ]
