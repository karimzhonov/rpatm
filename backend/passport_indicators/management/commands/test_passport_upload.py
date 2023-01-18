from django.core.management import BaseCommand
from passport_indicators import models, xlsx_upload


class Command(BaseCommand):
    def handle(self, *args, **options):
        instance = models.Uploads.objects.get(id=1)
        xlsx_upload.parse_data(instance)
        instance.status = 'finished'
        instance.save()
