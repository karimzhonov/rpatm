import copy
from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from celery import shared_task
from django.db import router
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django.contrib.admin.utils import NestedObjects, quote
from .admin_filters import CriteriaParentFilter, SectorFilter, RegionFilter, AreaFilter, \
    ModelCriteriaParentFilter
from .models import (
    Region, Sector, Uploads,
    Area, Criteria, RegionTable,
    SectorTable, RegionSectorTable, AreaTable, DataTable
)
from . import tabulers, xlsx_upload


@admin.register(Uploads)
class UploadsAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'finish_date']
    list_display = ['name', 'status', 'date', 'create_date', 'finish_date']
    inlines = [
        tabulers.UploadSectorTableTabularAdmin, tabulers.UploadRegionTableTabularAdmin,
        tabulers.UploadRegionSectorTabularAdmin, tabulers.UploadAreaTableTabularAdmin,
    ]
    list_filter = ['status', 'date']
    search_fields = ['name']

    def response_post_save_add(self, request, obj):
        response = super().response_post_save_add(request, obj)
        messages.add_message(request, messages.INFO, 'Upload xlsx started')
        self.upload_xlsx_database.delay(obj.id)
        return response

    @staticmethod
    @shared_task
    def upload_xlsx_database(instance_id):
        instance = Uploads.objects.get(id=instance_id)
        try:
            xlsx_upload.parse_data(copy.deepcopy(instance))
            xlsx_upload.parse_sector(copy.deepcopy(instance))
            xlsx_upload.parse_region(copy.deepcopy(instance))
            xlsx_upload.parse_region_sector(copy.deepcopy(instance))
            xlsx_upload.parse_area(copy.deepcopy(instance))
            instance.set_finished()
        except Exception as _exp:
            instance.set_error()
            raise _exp

    def get_deleted_objects(self, objs, request):
        try:
            obj = objs[0]
        except IndexError:
            return [], {}, set(), []
        else:
            using = router.db_for_write(obj._meta.model)
        collector = NestedObjects(using=using, origin=objs)
        collector.collect(objs)
        perms_needed = set()

        def format_callback(obj):
            model = obj.__class__
            has_admin = model in admin.site._registry
            opts = obj._meta

            no_edit_link = "%s: %s" % (capfirst(opts.verbose_name), obj)

            if has_admin:
                if not admin.site._registry[model].has_delete_permission(request, obj):
                    perms_needed.add(opts.verbose_name)
                try:
                    admin_url = reverse(
                        "%s:%s_%s_change"
                        % (admin.site.name, opts.app_label, opts.model_name),
                        None,
                        (quote(obj.pk),),
                    )
                except NoReverseMatch:
                    # Change url doesn't exist -- don't display link to edit
                    return no_edit_link

                # Display a link to the admin page.
                return format_html(
                    '{}: <a href="{}">{}</a>', capfirst(opts.verbose_name), admin_url, obj
                )
            else:
                # Don't display link to edit, because it either has no
                # admin or is edited inline.
                return no_edit_link

        protected = [format_callback(obj) for obj in collector.protected]
        model_count = {
            model._meta.verbose_name_plural: len(objs)
            for model, objs in collector.model_objs.items()
        }

        return [], model_count, perms_needed, protected


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    ordering = ['number']
    search_fields = ['number']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'region', 'sector']
    search_fields = ['name']
    list_filter = ['region', 'sector']


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    ordering = ['order']
    list_display = ['order', 'name', 'parent']
    list_display_links = ['name']
    list_filter = [CriteriaParentFilter, ]
    search_fields = ['name']


@admin.register(SectorTable)
class SectorTableAdmin(admin.ModelAdmin):
    inlines = [tabulers.SectorTableTabularAdmin]
    list_display = ['order', 'get_delta_order', 'sector', 'get_file_name']
    list_display_links = ['sector']
    ordering = ['order']
    list_filter = ("file",)
    search_fields = ['sector__number']

    def get_delta_order(self, instance):
        html = instance.delta_order
        if html > 0:
            html = f'<p style="color: green">+{html}</p>'
        elif html < 0:
            html = f'<p style="color: red">{html}</p>'
        return mark_safe(html)

    def get_file_name(self, instance):
        return instance.file.name

    get_file_name.short_description = _('Upload File')
    get_delta_order.short_description = _('Delta order')


@admin.register(RegionTable)
class RegionTableAdmin(admin.ModelAdmin):
    inlines = [tabulers.RegionTableTabularAdmin]
    list_display = ['order', 'get_delta_order', 'region', 'get_file_name']
    list_display_links = ['region']
    list_filter = ('file',)
    search_fields = ['region__name']
    ordering = ['order']

    def get_delta_order(self, instance):
        html = instance.delta_order
        if html > 0:
            html = f'<p style="color: green">+{html}</p>'
        elif html < 0:
            html = f'<p style="color: red">{html}</p>'
        return mark_safe(html)

    def get_file_name(self, instance):
        return instance.file.name

    get_file_name.short_description = _('Upload File')
    get_delta_order.short_description = _('Delta order')


@admin.register(RegionSectorTable)
class RegionSectorTableAdmin(admin.ModelAdmin):
    inlines = [tabulers.RegionSectorTableTabularAdmin]
    list_display = ['order', 'get_delta_order', 'region', 'sector', 'get_file_name']
    list_display_links = ['region']
    list_filter = ['sector', 'region', 'file']

    def get_delta_order(self, instance):
        html = instance.delta_order
        if html > 0:
            html = f'<p style="color: green">+{html}</p>'
        elif html < 0:
            html = f'<p style="color: red">{html}</p>'
        return mark_safe(html)

    def get_file_name(self, instance):
        return instance.file.name

    get_file_name.short_description = _('Upload File')
    get_delta_order.short_description = _('Delta order')


@admin.register(AreaTable)
class AreaTableAdmin(admin.ModelAdmin):
    inlines = [tabulers.AreaTableTabularAdmin]
    list_display = ('order', 'get_delta_order', 'area', 'region', 'sector', 'get_file_name')
    list_display_links = ['area']
    ordering = ['order']
    list_filter = [RegionFilter, SectorFilter, 'area', 'file']
    search_fields = ['area__name']

    def get_delta_order(self, instance):
        html = instance.delta_order
        if html > 0:
            html = f'<p style="color: green">+{html}</p>'
        elif html < 0:
            html = f'<p style="color: red">{html}</p>'
        return mark_safe(html)

    def get_file_name(self, instance):
        return instance.file.date

    get_file_name.short_description = _('Upload File')
    get_delta_order.short_description = _('Delta order')


@admin.register(DataTable)
class DataTableAdmin(admin.ModelAdmin):
    list_display = ['criteria', 'index', 'index_delta', 'region', 'sector', 'area']
    list_display_links = ['criteria']
    list_filter = [ModelCriteriaParentFilter, RegionFilter, SectorFilter, AreaFilter, 'file']
