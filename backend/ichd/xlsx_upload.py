import io

import numpy as np
import pandas as pd

from . import models


def parse_data(instance):
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'data', engine='openpyxl')
    data = []
    for row in xlsx.iloc:
        region, _ = models.Region.objects.get_or_create(name=row['region'])
        sector, _ = models.Sector.objects.get_or_create(number=row['sector'])
        area, _ = models.Area.objects.get_or_create(name=row['area'], region_id=region.id, sector_id=sector.id)
        if not pd.isna(row['parent']):
            parent_criteria, _ = models.Criteria.objects.get_or_create(name=row['parent'])
        else:
            parent_criteria = None
        criteria, _ = models.Criteria.objects.get_or_create(name=row['type'], parent=parent_criteria)
        index = np.round(row["index"] * 1000) / 1000
        # if not pd.isna(row['index_delta']):
        #     delta_index = np.round(row['index_delta'] * 1000) / 1000
        # else:
        #     delta_index = None
        data_row = models.DataTable(
            region_id=region.id, sector_id=sector.id, area_id=area.id, file_id=instance.id,
            criteria_id=criteria.id, index=index, index_delta=None,
        )
        data.append(data_row)
    models.DataTable.objects.bulk_create(data)


def parse_region_data(instance):
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'region_data', engine='openpyxl')
    data = []
    for row in xlsx.iloc:
        region, _ = models.Region.objects.get_or_create(name=row['region'])
        if not pd.isna(row['parent']):
            parent_criteria, _ = models.Criteria.objects.get_or_create(name=row['parent'])
        else:
            parent_criteria = None
        criteria, _ = models.Criteria.objects.get_or_create(name=row['type'], parent=parent_criteria)
        index = np.round(row["index"] * 1000) / 1000
        # if not pd.isna(row['index_delta']):
        #     delta_index = np.round(row['index_delta'] * 1000) / 1000
        # else:
        #     delta_index = None
        data_row = models.RegionDataTable(
            region_id=region.id, file_id=instance.id,
            criteria_id=criteria.id, index=index, index_delta=None,
        )
        data.append(data_row)
    models.RegionDataTable.objects.bulk_create(data)


def parse_sector(instance):
    ignore_columns = ['Ўрин', 'Сектор', 'Ўрин ўзгариш']
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'sector', engine='openpyxl')
    for row in xlsx.iloc:
        order = int(row['Ўрин'])
        try:
            sector = str(int(row['Сектор']))
        except ValueError:
            sector = str(row['Сектор'])
        order_delta = int(row['Ўрин ўзгариш'])
        sector, _ = models.Sector.objects.get_or_create(number=sector)
        sector_table = models.SectorTable(
            order=order, delta_order=order_delta, sector_id=sector.id,
            file_id=instance.id
        )
        sector_table.save()
        is_delta = False
        sector_table_criteria = []
        for i, column in enumerate(xlsx.columns.values):
            if column not in ignore_columns and not is_delta:
                criteria, _ = models.Criteria.objects.get_or_create(name=column)
                table_criteria = models.SectorTableCriteria(
                    table=sector_table, index=np.round(row[column] * 1000) / 1000,
                    delta=np.round(row[xlsx.columns.values[i + 1]] * 1000) / 1000,
                    criteria=criteria
                )
                sector_table_criteria.append(table_criteria)
                is_delta = True
            else:
                is_delta = False
        models.SectorTableCriteria.objects.bulk_create(sector_table_criteria)


def parse_area(instance):
    ignore_columns = ['Ўрин', 'Туман', 'Сектор', 'Маҳалла', 'Ўрин ўзгариш', 'ID']
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'area', engine='openpyxl')
    for row in xlsx.iloc:
        order = int(row['Ўрин'])
        order_delta = int(row['Ўрин ўзгариш'])
        region, _ = models.Region.objects.get_or_create(name=str(row['Туман']))
        try:
            sector = str(int(row['Сектор']))
        except ValueError:
            sector = str(row['Сектор'])
        sector, _ = models.Sector.objects.get_or_create(number=sector)
        area, _ = models.Area.objects.get_or_create(name=row['Маҳалла'], region_id=region.id, sector_id=sector.id)
        if not area.global_id == row['ID']:
            area.global_id = row['ID']
            area.save()
        area_table = models.AreaTable(
            order=order, delta_order=order_delta, region_id=region.id,
            file_id=instance.id, sector_id=sector.id, area_id=area.id
        )
        area_table.save()
        is_delta = False
        area_table_criteria = []
        for i, column in enumerate(xlsx.columns.values):
            if column not in ignore_columns and not is_delta:
                criteria, _ = models.Criteria.objects.get_or_create(name=column)
                table_criteria = models.AreaTableCriteria(
                    table=area_table, index=np.round(row[column] * 1000) / 1000,
                    delta=np.round(row[xlsx.columns.values[i + 1]] * 1000) / 1000,
                    criteria=criteria
                )
                area_table_criteria.append(table_criteria)
                is_delta = True
            else:
                is_delta = False
        models.AreaTableCriteria.objects.bulk_create(area_table_criteria)


def parse_region(instance):
    ignore_columns = ['Ўрин', 'Туман', 'Ўрин ўзгариш']
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'region', engine='openpyxl')

    for row in xlsx.iloc:
        order = int(row['Ўрин'])
        region = str(row['Туман'])
        order_delta = int(row['Ўрин ўзгариш'])
        region, _ = models.Region.objects.get_or_create(name=region)
        region_table = models.RegionTable(
            order=order, delta_order=order_delta, region_id=region.id,
            file_id=instance.id
        )
        region_table.save()
        is_delta = False
        region_table_criteria = []
        for i, column in enumerate(xlsx.columns.values):
            if column not in ignore_columns and not is_delta:
                criteria, _ = models.Criteria.objects.get_or_create(name=column)
                table_criteria = models.RegionTableCriteria(
                    table=region_table, index=np.round(row[column] * 1000) / 1000,
                    delta=np.round(row[xlsx.columns.values[i + 1]] * 1000) / 1000,
                    criteria=criteria
                )
                region_table_criteria.append(table_criteria)
                is_delta = True
            else:
                is_delta = False
        models.RegionTableCriteria.objects.bulk_create(region_table_criteria)


def parse_region_sector(instance):
    ignore_columns = ['Ўрин', 'Туман', 'Сектор', 'Ўрин ўзгариш']
    xlsx = pd.read_excel(io.BytesIO(instance.file.read()), 'region-sector', engine='openpyxl')
    for row in xlsx.iloc:
        order = int(row['Ўрин'])
        order_delta = int(row['Ўрин ўзгариш'])
        region, _ = models.Region.objects.get_or_create(name=str(row['Туман']))
        try:
            sector = str(int(row['Сектор']))
        except ValueError:
            sector = str(row['Сектор'])
        sector, _ = models.Sector.objects.get_or_create(number=sector)
        region_sector_table = models.RegionSectorTable(
            order=order, delta_order=order_delta, region_id=region.id,
            file_id=instance.id, sector_id=sector.id
        )
        region_sector_table.save()
        is_delta = False
        region_sector_table_criteria = []
        for i, column in enumerate(xlsx.columns.values):
            if column not in ignore_columns and not is_delta:
                criteria, _ = models.Criteria.objects.get_or_create(name=column)
                table_criteria = models.RegionSectorTableCriteria(
                    table=region_sector_table, index=np.round(row[column] * 1000) / 1000,
                    delta=np.round(row[xlsx.columns.values[i + 1]] * 1000) / 1000,
                    criteria=criteria
                )
                region_sector_table_criteria.append(table_criteria)
                is_delta = True
            else:
                is_delta = False
        models.RegionSectorTableCriteria.objects.bulk_create(region_sector_table_criteria)
