from django.core.management import BaseCommand

from ichd import models, xlsx_upload


class Command(BaseCommand):
    def handle(self, *args, **options):
        instance = models.Uploads.objects.get(id=6)
        xlsx_upload.parse_data(instance)
        xlsx_upload.parse_sector(instance)
        xlsx_upload.parse_region(instance)
        xlsx_upload.parse_area(instance)
        xlsx_upload.parse_region_sector(instance)
        instance.status = 'finished'
        instance.save()
