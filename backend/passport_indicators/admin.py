import copy
from celery import shared_task
from django.contrib import admin, messages
from django.contrib.admin.utils import NestedObjects, quote
from django.db import router
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from .models import Uploads, Criteria, Region, DataTable
from . import xlsx_upload


@admin.register(Uploads)
class UploadsAdmin(admin.ModelAdmin):
    readonly_fields = ['status', 'finish_date']
    list_display = ['name', 'status', 'date', 'create_date', 'finish_date']
    inlines = []
    list_filter = ['status', 'date']
    search_fields = ['name']
    actions = ['passport_data_upload']

    @admin.action(description='Upload xlsx')
    def passport_data_upload(modeladmin, request, queryset):
        for obj in queryset:
            modeladmin.upload_xlsx_database.delay(obj.id)
        messages.add_message(request, messages.INFO, 'Upload xlsx started')

    @staticmethod
    @shared_task
    def upload_xlsx_database(instance_id):
        instance = Uploads.objects.get(id=instance_id)
        try:
            xlsx_upload.parse_data(copy.deepcopy(instance))
            instance.set_finished()
        except Exception as _exp:
            instance.set_error(str(_exp))
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


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    pass


@admin.register(DataTable)
class DataTableAdmin(admin.ModelAdmin):
    list_display = ['region', 'criteria', 'value']
    list_filter = ['file', 'region']
