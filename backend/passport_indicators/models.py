from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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
    message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('Upload Passport')
        verbose_name_plural = _('Uploads Passport')
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


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Criteria(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class DataTable(models.Model):
    criteria = models.ForeignKey(Criteria, models.PROTECT)
    file = models.ForeignKey(Uploads, models.CASCADE)
    value = models.CharField(max_length=255)
    region = models.ForeignKey(Region, models.PROTECT)
