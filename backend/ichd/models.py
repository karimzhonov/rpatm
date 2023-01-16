from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Sector(models.Model):
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{_('Sector')} - {self.number}"

    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')
        ordering = ['number']


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ['name']


class Area(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, models.CASCADE)
    sector = models.ForeignKey(Sector, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')
        ordering = ['name']


class Criteria(models.Model):
    order = models.IntegerField(blank=True, null=True)
    main = models.BooleanField(default=False)
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f'{self.name}{f" ({self.parent})" if self.parent else ""}'

    class Meta:
        verbose_name = _('Criteria')
        verbose_name_plural = _('Criteria')
        ordering = ['order']


class Uploads(models.Model):
    STATUS = (
        ('progres', _("In progres")),
        ('finished', _("Finished")),
        ('error', _("Error"))
    )
    file = models.FileField(upload_to='xlsx')
    name = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=100, default='progres', choices=STATUS)
    create_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    message = models.TextField(editable=False, blank=True, null=True)

    class Meta:
        verbose_name = _('Upload')
        verbose_name_plural = _('Uploads')
        ordering = ['-date']

    def __str__(self):
        return self.name

    def set_finished(self):
        self.status = 'finished'
        self.finish_date = timezone.now()
        self.save()

    def set_progres(self):
        self.status = 'progres'
        self.create_date = timezone.now()
        self.finish_date = None
        self.save()

    def set_error(self, text=None):
        self.status = 'error'
        self.message = text
        self.save()


class SectorTable(models.Model):
    order = models.IntegerField(blank=True, null=True)
    delta_order = models.IntegerField(blank=True, null=True)
    sector = models.ForeignKey(Sector, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)

    def __str__(self):
        return f'Sector - {self.sector.number}, {self.order} ({self.delta_order})'

    class Meta:
        verbose_name = _('Sector Table')
        verbose_name_plural = _('Sector Tables')
        ordering = ['order']


class SectorTableCriteria(models.Model):
    table = models.ForeignKey(SectorTable, models.CASCADE)
    index = models.FloatField()
    delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    class Meta:
        verbose_name = _('Sector Table Criteria')
        verbose_name_plural = _('Sector Table Criteria')
        ordering = ['criteria__order', 'criteria__name']


class RegionTable(models.Model):
    order = models.IntegerField(blank=True, null=True)
    delta_order = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)

    def __str__(self):
        return f'{self.region} {self.order} ({self.delta_order})'

    class Meta:
        verbose_name = _('Region Table')
        verbose_name_plural = _('Region Tables')
        ordering = ['order']


class RegionTableCriteria(models.Model):
    table = models.ForeignKey(RegionTable, models.CASCADE)
    index = models.FloatField()
    delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    class Meta:
        verbose_name = _('Region Table Criteria')
        verbose_name_plural = _('Region Table Criteria')
        ordering = ['criteria__order', 'criteria__name']


class RegionSectorTable(models.Model):
    order = models.IntegerField(blank=True, null=True)
    delta_order = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, models.PROTECT)
    sector = models.ForeignKey(Sector, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)

    class Meta:
        verbose_name = _('Region Sector Table')
        verbose_name_plural = _('Region Sector Tables')
        ordering = ['order']


class RegionSectorTableCriteria(models.Model):
    table = models.ForeignKey(RegionSectorTable, models.CASCADE)
    index = models.FloatField()
    delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    class Meta:
        verbose_name = _('Region Sector Table Criteria')
        verbose_name_plural = _('Region Sector Table Criteria')
        ordering = ['criteria__order', 'criteria__name']


class AreaTable(models.Model):
    order = models.IntegerField(blank=True, null=True)
    delta_order = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Region, models.PROTECT)
    sector = models.ForeignKey(Sector, models.PROTECT)
    area = models.ForeignKey(Area, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)

    class Meta:
        verbose_name = _('Area Table')
        verbose_name_plural = _('Area Tables')
        ordering = ['order']


class AreaTableCriteria(models.Model):
    table = models.ForeignKey(AreaTable, models.CASCADE)
    index = models.FloatField()
    delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    class Meta:
        verbose_name = _('Area Table Criteria')
        verbose_name_plural = _('Area Table Criteria')
        ordering = ['criteria__order', 'criteria__name']


class RegionDataTable(models.Model):
    region = models.ForeignKey(Region, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)
    index = models.FloatField()
    index_delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    def __str__(self):
        return f'{self.region} ({self.sector}), {self.area} {self.index} ({self.index_delta}) - {self.criteria}'

    class Meta:
        verbose_name = _('Region Data Table')
        verbose_name_plural = _('Region Data Tables')


class DataTable(models.Model):
    region = models.ForeignKey(Region, models.PROTECT)
    sector = models.ForeignKey(Sector, models.PROTECT)
    area = models.ForeignKey(Area, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)
    index = models.FloatField()
    index_delta = models.FloatField(blank=True, null=True)
    criteria = models.ForeignKey(Criteria, models.PROTECT)

    def __str__(self):
        return f'{self.region} ({self.sector}), {self.area} {self.index} ({self.index_delta}) - {self.criteria}'

    class Meta:
        verbose_name = _('Data Table')
        verbose_name_plural = _('Data Tables')
