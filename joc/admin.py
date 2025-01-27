from django.contrib import admin
from .models import Player
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms
import random
import json

with open('joc/static/json/choices.json') as data:
    choices = json.load(data)

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['last_login']  # Hide last_login field
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        labels = {
            'code': 'Codi',
            'first_name': 'Nom',
            'last_name': 'Cognoms',
            'birth_date': 'Data de Naixement',
            'profile_picture': 'Foto de Perfil',
            'territori_zona': 'Territori/Zona',
            'esplai': 'Centre',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']
        if not self.instance.pk:
            self.fields['code'].initial = self.generate_unique_code()
        self.fields['territori_zona'].widget.attrs.update({'onchange': 'updateEsplaiChoices()'})
        self.fields['esplai'].widget = forms.Select(choices=self.get_esplai_choices())
        if not self.instance.territori_zona:
            self.fields['esplai'].widget.attrs.update({'disabled': 'disabled'})

    def generate_unique_code(self):
        while True:
            code = str(random.randint(10000, 99999))
            if not Player.objects.filter(code=code).exists():
                return code

    def get_esplai_choices(self):
        territori_zona = self.data.get('territori_zona') or self.instance.territori_zona
        for territori in choices['TERRITORIS']:
            if territori['zona'] == territori_zona:
                return [(esplai['id'], esplai['nom']) for esplai in territori['esplais']]
        return []

    class Media:
        js = ('admin/js/player_admin.js',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    change_list_template = "admin/player_changelist.html"
    list_display = ('code_display', 'first_name_display', 'last_name_display', 'birth_date_display', 'territori_zona_display', 'esplai_display')
    form = PlayerAdminForm

    def code_display(self, obj):
        return obj.code
    code_display.short_description = 'Codi'

    def first_name_display(self, obj):
        return obj.first_name
    first_name_display.short_description = 'Nom'

    def last_name_display(self, obj):
        return obj.last_name
    last_name_display.short_description = 'Cognoms'

    def birth_date_display(self, obj):
        return obj.birth_date.strftime('%d/%m/%Y')
    birth_date_display.short_description = 'Data de Naixement'

    def territori_zona_display(self, obj):
        return obj.territori_zona
    territori_zona_display.short_description = 'Territori/Zona'

    def esplai_display(self, obj):
        return obj.esplai
    esplai_display.short_description = 'Centre'

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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        player = self.get_object(request, object_id)
        extra_context['title'] = f"Modificar Jugador"
        extra_context['subtitle'] = f'{player.first_name} {player.last_name}'
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "Afegir Jugador"
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().add_view(request, form_url, extra_context=extra_context)
