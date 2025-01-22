from django.contrib import admin
from .models import Player
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    change_list_template = "admin/player_changelist.html"
    list_display = ('username', 'first_name', 'last_name', 'code')

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
