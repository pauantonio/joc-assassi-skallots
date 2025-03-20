from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django import forms
import random
from django.db.models import Count
from .models import Player, GameConfig, AssassinationCircle, Assassination
from django.core.exceptions import ValidationError

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
            'name': 'Nom i Cognoms',
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
        'code_display', 'name_display', 'birth_date_display', 'territori_zona_display', 'esplai_display', 'status'
    )
    search_fields = ('code', 'name', 'esplai', 'territori_zona')
    list_filter = ('status', 'territori_zona', 'esplai')
    form = PlayerAdminForm

    # Display methods for list_display fields
    def code_display(self, obj):
        return obj.code
    code_display.short_description = 'Codi'

    def name_display(self, obj):
        return obj.name
    name_display.short_description = 'Nom i Cognoms'

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
            path('player-stats/', self.admin_site.admin_view(self.player_stats), name='player_stats'),
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

    def player_stats(self, request):
        total_players = Player.objects.count()
        logged_in_players = Player.objects.filter(last_login__isnull=False).count()
        status_counts = Player.objects.values('status').annotate(count=Count('status'))
        status_dict = {status: 0 for status, _ in Player.PLAYER_STATUS_CHOICES}
        for status in status_counts:
            status_dict[status['status']] = status['count']

        status_counts = [(dict(Player.PLAYER_STATUS_CHOICES)[status], count, (count / total_players) * 100) for status, count in status_dict.items()]
        registered_players = total_players - status_dict['pending_registration'] - status_dict['not_playing']

        context = {
            'total_players': total_players,
            'logged_in_players': logged_in_players,
            'logged_in_percentage': (logged_in_players / total_players) * 100,
            'status_counts': status_counts,
            'registered_players': registered_players,
            'registered_percentage': (registered_players / total_players) * 100,
        }
        return render(request, 'admin/player_stats.html', context)

    # Custom change view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        player = self.get_object(request, object_id)
        extra_context['title'] = f"Modificar Jugador"
        extra_context['subtitle'] = f'{player.name}'
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

# Admin configuration for GameConfig model
@admin.register(GameConfig)
class GameConfigAdmin(admin.ModelAdmin):
    list_display = ('disable_until', 'game_status')
    list_editable = ('disable_until', 'game_status')
    list_display_links = None  # Disable links to avoid conflict with list_editable

    def has_add_permission(self, request):
        return not GameConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

# Admin configuration for AssassinationCircle model
@admin.register(AssassinationCircle)
class AssassinationCircleAdmin(admin.ModelAdmin):
    change_list_template = "admin/assassinationcircle_changelist.html"
    list_display = ('player', 'target', 'target_status')
    search_fields = ('player', 'player__code' , 'player__name', 'target', 'target__code', 'target__name')
    actions = ['request_kill_action', 'confirm_death_action', 'cancel_death_action']

    def target_status(self, obj):
        return obj.target.status
    target_status.short_description = 'Victim Status'

    def has_add_permission(self, request):
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
                GameConfig.objects.update(game_status='playing')
                self.message_user(request, "Assassination circle generated successfully")
            except ValidationError as e:
                self.message_user(request, f"Error: {e}", level='error')
            return HttpResponseRedirect("../")
        return render(request, "admin/generate_circle.html")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_circle_url'] = 'admin:generate_circle'
        return super().changelist_view(request, extra_context=extra_context)

    def request_kill_action(self, request, queryset):
        for circle in queryset:
            try:
                AssassinationCircle.request_kill(circle.player)
                self.message_user(request, f"Kill requested for {circle.player}")
            except ValidationError as e:
                self.message_user(request, f"Error: {e}", level='error')

    request_kill_action.short_description = "Request Kill"

    def confirm_death_action(self, request, queryset):
        for circle in queryset:
            try:
                AssassinationCircle.confirm_death(circle.target)
                self.message_user(request, f"Death confirmed for {circle.target}")
            except ValidationError as e:
                self.message_user(request, f"Error: {e}", level='error')

    confirm_death_action.short_description = "Confirm Death"

    def cancel_death_action(self, request, queryset):
        for circle in queryset:
            try:
                AssassinationCircle.discard_death(circle.target)
                self.message_user(request, f"Death canceled for {circle.target}")
            except ValidationError as e:
                self.message_user(request, f"Error: {e}", level='error')

    cancel_death_action.short_description = "Cancel Death"

@admin.register(Assassination)
class AssassinationAdmin(admin.ModelAdmin):
    list_display = ('killer', 'victim', 'timestamp', 'points')
    search_fields = ('killer', 'killer__code', 'killer__name', 'victim', 'victim__code', 'victim__name')
    readonly_fields = ('timestamp',)
    list_filter = ('points',) 

    def has_add_permission(self, request):
        return False
