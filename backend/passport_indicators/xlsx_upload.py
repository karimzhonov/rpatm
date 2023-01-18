import io
import numpy as np
import pandas as pd
from . import models


def parse_data(instance: models.Uploads):
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'main', engine='openpyxl')
    data = []
    for row in xlsx.iloc:
        region, _ = models.Region.objects.get_or_create(name=row['region'])
        criteria, _ = models.Criteria.objects.get_or_create(name=row['type'])
        value = row['value']
        data_row = models.DataTable(
            region_id=region.id, file_id=instance.id,
            criteria_id=criteria.id, value=value,
        )
        data.append(data_row)
    models.DataTable.objects.bulk_create(data)
