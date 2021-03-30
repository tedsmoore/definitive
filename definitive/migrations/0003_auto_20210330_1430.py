# Generated by Django 3.1.5 on 2021-03-30 18:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('definitive', '0002_rankresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankresponse',
            name='response_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='unique id for this respondent'),
        ),
        migrations.AlterUniqueTogether(
            name='rankresponse',
            unique_together={('response_id', 'left', 'right')},
        ),
    ]