from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        import json

        geodata = []

        with open(settings.BASE_DIR / 'geojson.json', encoding="utf8") as file:
            for row in file.readlines():
                data = json.loads(row)
                new_data = {
                    'type': data['type'],
                    'properties': {
                        'area_id': data['properties']['t_id_2']
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': data['geometry']['coordinates'][0]
                    }
                }
                geodata.append(new_data)

        with open(settings.BASE_DIR / 'geojson.json', 'w') as file:
            json.dump(geodata, file, indent=4)
