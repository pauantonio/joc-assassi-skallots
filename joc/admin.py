from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms
import random
from .models import Player, GameSettings, AssassinationCircle
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime

# Form for CSV import
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

# Custom form for Player model
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

    def generate_unique_code(self):
        while True:
            code = str(random.randint(10000, 99999))
            if not Player.objects.filter(code=code).exists():
                return code

# Admin configuration for Player model
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    change_list_template = "admin/player_changelist.html"
    list_display = (
        'code_display', 'first_name_display', 'last_name_display', 
        'birth_date_display', 'territori_zona_display', 'esplai_display'
    )
    form = PlayerAdminForm

    # Display methods for list_display fields
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

    # Custom admin URLs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='player_import_csv'),
        ]
        return custom_urls + urls

    # CSV import view
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

    # Custom change view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        player = self.get_object(request, object_id)
        extra_context['title'] = f"Modificar Jugador"
        extra_context['subtitle'] = f'{player.first_name} {player.last_name}'
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    # Custom add view
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "Afegir Jugador"
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().add_view(request, form_url, extra_context=extra_context)

# Admin configuration for GameSettings model
@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    list_display = ('disable_until', 'game_status')
    list_editable = ('disable_until', 'game_status')
    list_display_links = None  # Disable links to avoid conflict with list_editable

    def has_add_permission(self, request):
        return not GameSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

# Admin configuration for AssassinationCircle model
@admin.register(AssassinationCircle)
class AssassinationCircleAdmin(admin.ModelAdmin):
    change_list_template = "admin/assassinationcircle_changelist.html"
    list_display = ('player', 'target')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-circle/', self.admin_site.admin_view(self.generate_circle), name='generate_circle'),
        ]
        return custom_urls + urls

    def generate_circle(self, request):
        if request.method == "POST":
            try:
                AssassinationCircle.create_circle()
                self.message_user(request, "Assassination circle generated successfully")
            except ValidationError as e:
                self.message_user(request, f"Error: {e}", level='error')
            return HttpResponseRedirect("../")
        return render(request, "admin/generate_circle.html")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_circle_url'] = 'admin:generate_circle'
        return super().changelist_view(request, extra_context=extra_context)