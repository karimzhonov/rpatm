from django import forms

from . import models


class UploadSectorInlineForm(forms.ModelForm):
    class Meta:
        model = models.SectorTable
        fields = "__all__"

    def __init__(self):
        super().__init__()
        forms.CharField()
