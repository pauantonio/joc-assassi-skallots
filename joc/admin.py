from django.contrib import admin
from .models import Player
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].input_formats = ['%d/%m/%Y']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    change_list_template = "admin/player_changelist.html"
    list_display = ('code', 'first_name', 'last_name', 'birth_date', 'esplai', 'territori_zona')
    form = PlayerAdminForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='player_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            Player.import_from_csv(decoded_file)
            self.message_user(request, "Players imported successfully")
            return HttpResponseRedirect("../")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)
